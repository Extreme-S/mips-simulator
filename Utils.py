from Constants import *
import Instructions
import re


# 输入二进制文件，返回指令列表
def read_bin(filename):
    instructions = []
    with open(filename, "r") as fin:
        for line in fin:
            instructions.append(line.strip())
    return instructions


# 获取数据段的值
def getData(instruction):
    if instruction[0] == '0':  # 正数
        res = str(int(instruction, 2))
    else:  # 负数
        res = str(int(instruction, 2) - (1 << 32))
    return res


# 处理指令空格
def preProcess(instruction):
    return instruction[0:6] + " " + instruction[6:11] + " " + instruction[11:16] + " " + instruction[16:21] + " " + \
           instruction[21:26] + " " + instruction[26:32]


# 获取指令的名称
def getInstructionName(instruction):
    # Category-1
    for obj in category1_patterns:
        ans = re.fullmatch(obj.get("pattern"), instruction.replace(' ', ''))
        if ans is not None:
            return obj.get("name")
    # Category-2
    if instruction[0] == '0':
        functionCode = instruction[26:31]  # 获取Function
    else:
        functionCode = instruction[1:6]  # 获取Function
    functionName = functionMap[functionCode]
    return functionName


# 获取Category-2的执行参数
def getCat2Args(instruction):
    if instruction[0] == '0':
        res, op1, op2 = instruction[16:21], instruction[6:11], instruction[11:16]
    else:
        res, op1, op2 = instruction[11:16], instruction[6:11], instruction[16:32]
    return [res, op1, op2]


# 输出sim文件，递归执行，遇到BREAK指令停止
def outputSim(cycle, instructions, instructionNo, regValues, memValues, simOut):
    curAddress = [beginAddress + instructionNo * instructionSize]
    tmpAddress = curAddress[0]
    instructionName = getInstructionName(instructions[instructionNo])
    code = Instructions.switch[instructionName](instructions[instructionNo], curAddress, regValues, memValues)
    simOut.write("--------------------" + '\n')
    simOut.write("Cycle:" + str(cycle) + '\t' + str(tmpAddress) + '\t' + code + '\n')
    simOut.write('Registers' + '\n')
    simOut.write('R00:' + '\t' +
                 str(regValues[0]) + '\t' + str(regValues[1]) + '\t' + str(regValues[2]) + '\t' +
                 str(regValues[3]) + '\t' + str(regValues[4]) + '\t' + str(regValues[5]) + '\t' +
                 str(regValues[6]) + '\t' + str(regValues[7]) + '\t' + str(regValues[8]) + '\t' +
                 str(regValues[9]) + '\t' + str(regValues[10]) + '\t' + str(regValues[11]) + '\t' +
                 str(regValues[12]) + '\t' + str(regValues[13]) + '\t' + str(regValues[14]) + '\t' +
                 str(regValues[15]) + '\n')
    simOut.write('R16:' + '\t' +
                 str(regValues[16]) + '\t' + str(regValues[17]) + '\t' + str(regValues[18]) + '\t' +
                 str(regValues[19]) + '\t' + str(regValues[20]) + '\t' + str(regValues[21]) + '\t' +
                 str(regValues[22]) + '\t' + str(regValues[23]) + '\t' + str(regValues[24]) + '\t' +
                 str(regValues[25]) + '\t' + str(regValues[26]) + '\t' + str(regValues[27]) + '\t' +
                 str(regValues[28]) + '\t' + str(regValues[29]) + '\t' + str(regValues[30]) + '\t' +
                 str(regValues[31]) + '\n\n')
    simOut.write('Data' + '\n')
    simOut.write(str(dataSegBegin) + ':\t' +
                 str(memValues[0]) + '\t' + str(memValues[1]) + '\t' + str(memValues[2]) + '\t' +
                 str(memValues[3]) + '\t' + str(memValues[4]) + '\t' + str(memValues[5]) + '\t' +
                 str(memValues[6]) + '\t' + str(memValues[7]) + '\n')
    simOut.write(str(dataSegBegin + 32) + ':\t' +
                 str(memValues[8]) + '\t' + str(memValues[9]) + '\t' + str(memValues[10]) + '\t' +
                 str(memValues[11]) + '\t' + str(memValues[12]) + '\t' + str(memValues[13]) + '\t' +
                 str(memValues[14]) + '\t' + str(memValues[15]) + '\n')
    simOut.write(str(dataSegBegin + 64) + ':\t' +
                 str(memValues[16]) + '\t' + str(memValues[17]) + '\t' + str(memValues[18]) + '\t' +
                 str(memValues[19]) + '\t' + str(memValues[20]) + '\t' + str(memValues[21]) + '\t' +
                 str(memValues[22]) + '\t' + str(memValues[23]) + '\n\n')
    if instructionName == "BREAK":
        return
    instructionNoNext = int((curAddress[0] - beginAddress) / instructionSize)  # 计算下一条执行的指令编号
    outputSim(cycle + 1, instructions, instructionNoNext, regValues, memValues, simOut)
