import logging
import emulator.memory

from emulator.instructions.mem_mgnt import ser, sem
from emulator.instructions.bitwise import and_op, bsl, bsr, orr, xor
from emulator.instructions.arithmetic import add, mpy, div, inc, dec
from emulator.instructions.branches import comp, jlt, jle, jeq, jge, jgt, jne, jmp, fnc
from emulator.instructions.outputs import otm, otr

logger = logging.getLogger(__name__)

def run_instruction(memory_banks: list[emulator.memory.Memory], instruction: int, instruction_address: int):
    FUNCTIONS = {
        0: nop,
        6: ser,
        7: sem,
        8: and_op,
        9: orr,
        10: xor,
        11: bsl,
        12: bsr,
        13: add,
        15: mpy,
        16: div,
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
        28: otr,
        29: otm
    }

    if instruction in FUNCTIONS:
        FUNCTIONS[instruction](memory_banks, instruction_address)
    else:
        logger.warning(f"Unknown instruction {instruction}")


def nop(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    pass
