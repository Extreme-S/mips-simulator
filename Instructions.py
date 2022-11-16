from Utils import *


# 获取 寄存器 或 立即数 名称
def getName(op):
    if len(op) == 5:
        return 'R' + str(int(op, 2))
    return "#" + str(int(op, 2))


# Category-2
def case_ADD(instruction, curAddress, regValues, memValues):
    args = getCat2Args(instruction)
    res, op1, op2 = int(args[0], 2), int(args[1], 2), int(args[2], 2)
    regValues[res] = int(regValues[op1]) + int(regValues[op2] if instruction[0] == '0' else op2)
    curAddress[0] += instructionSize
    return "ADD" + " " + getName(args[0]) + ', ' + getName(args[1]) + ', ' + getName(args[2])


# 000000 00110 00101 00101 00000 100010	108	SUB R5, R6, R5
def case_SUB(instruction, curAddress, regValues, memValues):
    args = getCat2Args(instruction)
    res, op1, op2 = int(args[0], 2), int(args[1], 2), int(args[2], 2)
    regValues[res] = int(regValues[op1]) - int(regValues[op2] if instruction[0] == '0' else op2)
    curAddress[0] += instructionSize
    return "SUB" + " " + getName(args[0]) + ', ' + getName(args[1]) + ', ' + getName(args[2])


# 011100 00011 00100 00101 00000 000010	92	MUL R5, R3, R4
def case_MUL(instruction, curAddress, regValues, memValues):
    args = getCat2Args(instruction)
    res, op1, op2 = int(args[0], 2), int(args[1], 2), int(args[2], 2)
    # print(curAddress, regValues[res], regValues[op1], (regValues[op2] if instruction[0] == '0' else op2))
    regValues[res] = int(regValues[op1]) * int(regValues[op2] if instruction[0] == '0' else op2)
    curAddress[0] += instructionSize
    return "MUL" + " " + getName(args[0]) + ', ' + getName(args[1]) + ', ' + getName(args[2])


def case_AND(instruction):
    argList = getCat2Args(instruction)
    return "AND" + " " + getName(argList[0]) + ', ' + getName(argList[1]) + ', ' + getName(argList[2])


def case_NOR(instruction):
    argList = getCat2Args(instruction)
    return "NOR" + " " + getName(argList[0]) + ', ' + getName(argList[1]) + ', ' + getName(argList[2])


def case_SLT(instruction):
    argList = getCat2Args(instruction)
    return "SLT" + " " + getName(argList[0]) + ', ' + getName(argList[1]) + ', ' + getName(argList[2])


# Category-1
# 000010 00000 00000 00000 00000 010010	140
# J target
def case_J(instruction, curAddress, regValues, memValues):
    target = instruction[6:32]
    curAddress[0] = int(target, 2) << 2
    return "J" + " #" + str(int(target, 2) << 2)


def case_JR(instruction):
    return "JR" + " " + getName(instruction[6:11])


def case_BEQ(instruction, curAddress, regValues, memValues):
    rs, rt, offset = instruction[6:11], instruction[11:16], instruction[16:32]
    targetOffset = offset + "00"
    if regValues[int(rs, 2)] == regValues[int(rt, 2)]:
        curAddress[0] = curAddress[0] + int(targetOffset, 2) + instructionSize
    else:
        curAddress[0] = curAddress[0] + instructionSize
    return "BEQ " + getName(rs) + ", " + getName(rt) + ", #" + str(int(offset, 2) << 2)


# BLTZ rs, offset
def case_BLTZ(instruction, curAddress, regValues, memValues):
    rs, offset = instruction[6:11], instruction[16:32]
    curAddress[0] += (int(offset, 2) << 2 if regValues[int(rs, 2)] < 0 else instructionSize)
    return "BLTZ " + getName(rs) + ", #" + str(int(offset, 2) << 2)


# BGTZ rs, offset
def case_BGTZ(instruction, curAddress, regValues, memValues):
    rs, offset = instruction[6:11], instruction[16:32]
    # print(offset, regValues[int(rs, 2)], curAddress[0], (int(offset, 2) << 2))
    if regValues[int(rs, 2)] > 0:
        curAddress[0] = curAddress[0] + (int(offset, 2) << 2) + instructionSize
    else:
        curAddress[0] = int(curAddress[0]) + instructionSize
    return "BGTZ " + getName(rs) + ", #" + str(int(offset, 2) << 2)


def case_BREAK(instruction, curAddress, regValues, memValues):
    return "BREAK"


# SW rt, offset(base)
def case_SW(instruction, curAddress, regValues, memValues):
    rt, offset, base = instruction[11:16], instruction[16:32], instruction[6:11]
    memValues[int((regValues[int(base, 2)] + int(offset, 2)) / 4 - dataSegBegin / 4)] = regValues[int(rt, 2)]
    curAddress[0] += instructionSize
    return "SW " + getName(rt) + ", " + str(int(offset, 2)) + "(" + getName(base) + ")"


# LW rt, offset(base)
def case_LW(instruction, curAddress, regValues, memValues):
    rt, offset, base = instruction[11:16], instruction[16:32], instruction[6:11]
    regValues[int(rt, 2)] = memValues[int((regValues[int(base, 2)] + int(offset, 2)) / 4 - dataSegBegin / 4)]
    curAddress[0] += instructionSize
    return "LW " + getName(rt) + ", " + str(int(offset, 2)) + "(" + getName(base) + ")"


# SLL rd, rt, sa
def case_SLL(instruction, curAddress, regValues, memValues):
    rd, rt, sa = instruction[16:21], instruction[11:16], instruction[21:26]
    mask = (2 ** 32) - 1  # 左移会有溢出
    regValues[int(rd, 2)] = (regValues[int(rt, 2)] << int(sa, 2)) & mask
    curAddress[0] += instructionSize
    return "SLL " + getName(rd) + ", " + getName(rt) + ", #" + str(int(sa, 2))


# SRL rd, rt, sa
def case_SRL(instruction):
    return "SRL " + getName(instruction[16:21]) + ", " + getName(instruction[11:16]) \
           + ", #" + str(int(instruction[21:26], base=2))


# SRA rd, rt, sa
def case_SRA(instruction):
    return "SRA " + getName(instruction[16:21]) + ", " + getName(instruction[11:16]) \
           + ", #" + str(int(instruction[21:26], base=2))


def case_NOP(instruction):
    return "NOP "


switch = {
    'ADD': case_ADD,
    'SUB': case_SUB,
    'MUL': case_MUL,
    'AND': case_AND,
    'NOR': case_NOR,
    'SLT': case_SLT,
    'J': case_J,
    'JR': case_JR,
    'BEQ': case_BEQ,
    'BLTZ': case_BLTZ,
    'BGTZ': case_BGTZ,
    'BREAK': case_BREAK,
    'SW': case_SW,
    'LW': case_LW,
    'SLL': case_SLL,
    'SRL': case_SRL,
    'SRA': case_SRA,
    'NOP': case_NOP
}
