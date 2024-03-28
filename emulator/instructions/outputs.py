from emulator.instructions.general_functions import get_arg_value
import emulator.memory
from compiler.instructions import I_SIZE, A_SIZE, MAX_INT
from emulator.memory import MEMBANK, bit_array_to_int


def otr(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    print_address = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    value = memory_banks[MEMBANK.REG.value].get_value(print_address, A_SIZE)
    print(bit_array_to_int(value))


def otm(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    print_address = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    value = memory_banks[MEMBANK.RAM.value].get_value(print_address, A_SIZE)
    print(bit_array_to_int(value))
