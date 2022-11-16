import Constants
from Utils import *


def main():
    instructions = read_bin("resource/sample.txt")  # 获取所有的指令集

    # 数据存储
    instructionNo = 0  # 记录当前第几条指令
    regValues = [0] * 32  # 32个寄存器的值
    memValues = [0] * 60  # 数据段的值

    # 输出文件
    outputFilename = "resource/sample"
    disOut = open(outputFilename + '_dis.txt', 'w')
    simOut = open(outputFilename + '_sim.txt', 'w')

    # 处理代码段
    for instruction in instructions:
        instructionName = getInstructionName(instruction)  # 获取指令名称
        curAddress = [beginAddress + instructionNo * instructionSize]  # 当前指令地址(引用传递)
        code = Instructions.switch[instructionName](instruction, curAddress, regValues, memValues)  # 解析指令
        lineStr = preProcess(instruction) + "\t" + str(beginAddress + instructionNo * instructionSize) + "\t" + code
        disOut.write(lineStr + "\n")
        instructionNo += 1
        if instructionName == "BREAK":
            Constants.dataSegBegin = beginAddress + instructionNo * instructionSize  # 记录数据段的起始地址
            break

    # 处理数据段
    memValues = [0] * 60  # 初始化数据段的值
    dataSegINoBegin = instructionNo
    for instruction in instructions[instructionNo:]:
        memValue = getData(instruction)
        memValues[instructionNo - dataSegINoBegin] = memValue
        lineStr = instruction + "\t\t" + str(beginAddress + instructionNo * instructionSize) + "\t" + memValue
        disOut.write(lineStr + "\n")
        instructionNo += 1

    # 输出simulation
    regValues = [0] * 32  # 32个寄存器的值
    outputSim(1, instructions, 0, regValues, memValues, simOut)


if __name__ == '__main__':
    main()
    # print(disassembler("00011100101000000000000000000100"))
