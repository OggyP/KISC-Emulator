from emulator.instructions.general_functions import get_arg_value
import emulator.memory
from compiler.instructions import I_SIZE, A_SIZE
from emulator.memory import MEMBANK


def add(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_add_to = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    address_to_add_from = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 1)

    arr1 = memory_banks[MEMBANK.REG.value].get_value(address_to_add_to, A_SIZE)
    arr2 = memory_banks[MEMBANK.REG.value].get_value(
        address_to_add_from, A_SIZE)

    result = []
    carry = False

    for bit1, bit2 in zip(reversed(arr1), reversed(arr2)):
        # Perform binary addition considering the carry
        sum_bits = bit1 + bit2 + carry

        # Calculate the result bit and the carry for the next iteration
        result_bit = sum_bits % 2
        carry = (sum_bits // 2) == 1

        # Add the result bit to the beginning of the result list
        result.insert(0, result_bit == 1)

    FC = emulator.memory.mnemonic_to_adddress("FC")
    memory_banks[MEMBANK.REG.value].set_value(FC[0], [carry])

    memory_banks[MEMBANK.REG.value].set_value(address_to_add_to, result)


def inc(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_add_to = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)

    arr1 = memory_banks[MEMBANK.REG.value].get_value(address_to_add_to, A_SIZE)
    arr2 = emulator.memory.int_to_bit_array(1, A_SIZE)

    result = []
    carry = False

    for bit1, bit2 in zip(reversed(arr1), reversed(arr2)):
        # Perform binary addition considering the carry
        sum_bits = bit1 + bit2 + carry

        # Calculate the result bit and the carry for the next iteration
        result_bit = sum_bits % 2
        carry = (sum_bits // 2) == 1

        # Add the result bit to the beginning of the result list
        result.insert(0, result_bit == 1)

    FC = emulator.memory.mnemonic_to_adddress("FC")
    memory_banks[MEMBANK.REG.value].set_value(FC[0], [carry])

    memory_banks[MEMBANK.REG.value].set_value(address_to_add_to, result)


def dec(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_subtract_from = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    arr1 = memory_banks[MEMBANK.REG.value].get_value(
        address_to_subtract_from, A_SIZE)
    arr2 = [True for i in range(12)]

    result = []
    carry = False

    for bit1, bit2 in zip(reversed(arr1), reversed(arr2)):
        # Perform binary addition considering the carry
        sum_bits = bit1 + bit2 + carry

        # Calculate the result bit and the carry for the next iteration
        result_bit = sum_bits % 2
        carry = (sum_bits // 2) == 1

        # Add the result bit to the beginning of the result list
        result.insert(0, result_bit == 1)

    FC = emulator.memory.mnemonic_to_adddress("FC")
    memory_banks[MEMBANK.REG.value].set_value(FC[0], [carry])

    memory_banks[MEMBANK.REG.value].set_value(address_to_subtract_from, result)
