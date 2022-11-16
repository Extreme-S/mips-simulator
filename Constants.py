instructionSize = 4  # 单条指令大小
beginAddress = 64  # 代码段起始地址
dataSegBegin = 148  # 数据段起始地址

functionMap = {
    "10000": "ADD",
    "10001": "SUB",
    "00001": "MUL",
    "10010": "AND",
    "10011": "NOR",
    "10101": "SLT"
}

category1_patterns = [
    {
        "name": "J",
        "pattern": "^000010[01]{26}$"
    },
    {
        "name": "JR",
        "pattern": "^000000[01]{5}0000000000[01]{5}001000$"
    },
    {
        "name": "BEQ",
        "pattern": "^000100[01]{26}$"
    },
    {
        "name": "BLTZ",
        "pattern": "^000001[01]{5}00000[01]{16}$"
    },
    {
        "name": "BGTZ",
        "pattern": "^000111[01]{5}00000[01]{16}$"
    },
    {
        "name": "BREAK",
        "pattern": "^000000[01]{20}001101$"
    },
    {
        "name": "SW",
        "pattern": "^101011[01]{26}$"
    },
    {
        "name": "LW",
        "pattern": "^100011[01]{26}$"
    },
    {
        "name": "SLL",
        "pattern": "^00000000000[01]{15}000000$"
    },
    {
        "name": "SRL",
        "pattern": "^00000000000[01]{15}000010$"
    },
    {
        "name": "SRA",
        "pattern": "^00000000000[01]{15}000011$"
    },
    {
        "name": "NOP",
        "pattern": "^[0]{32}$"
    }
]
