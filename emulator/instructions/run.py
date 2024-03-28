import emulator.memory

from emulator.instructions.mem_mgnt import ser
from emulator.instructions.bitwise import and_op, bsl, bsr, orr, xor
from emulator.instructions.arithmetic import add, inc, dec
from emulator.instructions.branches import comp, jlt, jle, jeq, jge, jgt, jne, jmp, fnc


def run_instruction(memory_banks: list[emulator.memory.Memory], instruction: int, instruction_address: int):
    FUNCTIONS = {
        0: nop,
        6: ser,
        8: and_op,
        9: orr,
        10: xor,
        11: bsl,
        12: bsr,
        13: add,
        17: inc,
        18: dec,
        19: comp,
        20: jlt,
        21: jle,
        22: jeq,
        23: jge,
        24: jgt,
        25: jne,
        26: jmp,
        27: fnc,
    }

    if instruction in FUNCTIONS:
        FUNCTIONS[instruction](memory_banks, instruction_address)


def nop(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    pass
