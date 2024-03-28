from emulator.instructions.general_functions import get_arg_value
import emulator.memory
from compiler.instructions import I_SIZE, A_SIZE
from emulator.memory import MEMBANK


def and_op(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    register_address_1 = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    register_address_2 = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 1)

    arr1 = memory_banks[MEMBANK.REG.value].get_value(
        register_address_1, A_SIZE)
    arr2 = memory_banks[MEMBANK.REG.value].get_value(
        register_address_2, A_SIZE)

    result = []

    for bit1, bit2 in zip(arr1, arr2):
        result.append(bit1 and bit2)

    memory_banks[MEMBANK.REG.value].set_value(register_address_1, result)


def orr(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    register_address_1 = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    register_address_2 = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 1)

    arr1 = memory_banks[MEMBANK.REG.value].get_value(
        register_address_1, A_SIZE)
    arr2 = memory_banks[MEMBANK.REG.value].get_value(
        register_address_2, A_SIZE)

    result = []

    for bit1, bit2 in zip(arr1, arr2):
        result.append(bit1 or bit2)

    memory_banks[MEMBANK.REG.value].set_value(register_address_1, result)


def xor(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    register_address_1 = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    register_address_2 = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 1)

    arr1 = memory_banks[MEMBANK.REG.value].get_value(
        register_address_1, A_SIZE)
    arr2 = memory_banks[MEMBANK.REG.value].get_value(
        register_address_2, A_SIZE)

    result = []

    for bit1, bit2 in zip(arr1, arr2):
        result.append(bit1 ^ bit2)

    memory_banks[MEMBANK.REG.value].set_value(register_address_1, result)


def bsr(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_shift = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)

    bits = memory_banks[MEMBANK.REG.value].get_value(address_to_shift, A_SIZE)
    bits.pop()
    bits.insert(0, False)
    memory_banks[MEMBANK.REG.value].set_value(address_to_shift, bits)


def bsl(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_shift = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)

    bits = memory_banks[MEMBANK.REG.value].get_value(address_to_shift, A_SIZE)
    bits.pop(0)
    bits.append(False)
    memory_banks[MEMBANK.REG.value].set_value(address_to_shift, bits)
