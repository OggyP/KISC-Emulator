import emulator.memory
from compiler.instructions import I_SIZE, A_SIZE, MAX_INT
from emulator.memory import MEMBANK


def get_arg_bits(memory: emulator.memory.Memory, instruction_address: int, arg_num: int):
    return memory.get_value(instruction_address + I_SIZE + A_SIZE * arg_num, A_SIZE)


def get_arg_value(memory: emulator.memory.Memory, instruction_address: int, arg_num: int):
    return emulator.memory.bit_array_to_int(get_arg_bits(memory, instruction_address, arg_num))
