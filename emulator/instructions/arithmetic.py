from emulator.instructions.general_functions import get_arg_value
import emulator.memory
from compiler.instructions import I_SIZE, A_SIZE, MAX_INT
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
    carry = [False for i in range(12)]

    for bit1, bit2 in zip(reversed(arr1), reversed(arr2)):
        # Perform binary addition considering the carry
        sum_bits = bit1 + bit2 + carry[11]

        # Calculate the result bit and the carry for the next iteration
        result_bit = sum_bits % 2
        carry[11] = (sum_bits // 2) == 1

        # Add the result bit to the beginning of the result list
        result.insert(0, result_bit == 1)

    FC = emulator.memory.mnemonic_to_adddress("FC")
    memory_banks[MEMBANK.REG.value].set_value(FC[0], carry)

    memory_banks[MEMBANK.REG.value].set_value(address_to_add_to, result)


def mpy(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_mpy_to = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    address_to_mpy_from = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 1)

    arr1 = memory_banks[MEMBANK.REG.value].get_value(address_to_mpy_to, A_SIZE)
    arr2 = memory_banks[MEMBANK.REG.value].get_value(
        address_to_mpy_from, A_SIZE)
    
    num1 = emulator.memory.bit_array_to_int(arr1)
    num2 = emulator.memory.bit_array_to_int(arr2)
    int_result = num1*num2

    carry = [False for i in range(12)]
    if int_result >= MAX_INT:
        carry[11] = True
        int_result = int_result % MAX_INT

    result = emulator.memory.int_to_bit_array(int_result, 12)
    
    FC = emulator.memory.mnemonic_to_adddress("FC")
    memory_banks[MEMBANK.REG.value].set_value(FC[0], carry)

    memory_banks[MEMBANK.REG.value].set_value(address_to_mpy_to, result)


def div(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_div_to = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    address_to_div_from = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 1)

    arr1 = memory_banks[MEMBANK.REG.value].get_value(address_to_div_to, A_SIZE)
    arr2 = memory_banks[MEMBANK.REG.value].get_value(
        address_to_div_from, A_SIZE)
    
    num1 = emulator.memory.bit_array_to_int(arr1)
    num2 = emulator.memory.bit_array_to_int(arr2)

    if num2 == 0:
        raise ArithmeticError("Division by 0 is undefined and disallowed")
    else:
        int_result = num1 // num2
        result = emulator.memory.int_to_bit_array(int_result, 12)
        memory_banks[MEMBANK.REG.value].set_value(address_to_div_to, result)


def inc(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_add_to = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)

    arr1 = memory_banks[MEMBANK.REG.value].get_value(address_to_add_to, A_SIZE)
    arr2 = emulator.memory.int_to_bit_array(1, A_SIZE)

    result = []
    carry = [False for i in range(12)]

    for bit1, bit2 in zip(reversed(arr1), reversed(arr2)):
        # Perform binary addition considering the carry
        sum_bits = bit1 + bit2 + carry[11]

        # Calculate the result bit and the carry for the next iteration
        result_bit = sum_bits % 2
        carry[11] = (sum_bits // 2) == 1

        # Add the result bit to the beginning of the result list
        result.insert(0, result_bit == 1)

    FC = emulator.memory.mnemonic_to_adddress("FC")
    memory_banks[MEMBANK.REG.value].set_value(FC[0], carry)

    memory_banks[MEMBANK.REG.value].set_value(address_to_add_to, result)


def dec(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_subtract_from = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    arr1 = memory_banks[MEMBANK.REG.value].get_value(
        address_to_subtract_from, A_SIZE)
    arr2 = [True for i in range(12)]

    result = []
    carry = [False for i in range(12)]

    for bit1, bit2 in zip(reversed(arr1), reversed(arr2)):
        # Perform binary addition considering the carry
        sum_bits = bit1 + bit2 + carry[11]

        # Calculate the result bit and the carry for the next iteration
        result_bit = sum_bits % 2
        carry[11] = (sum_bits // 2) == 1

        # Add the result bit to the beginning of the result list
        result.insert(0, result_bit == 1)

    FC = emulator.memory.mnemonic_to_adddress("FC")
    memory_banks[MEMBANK.REG.value].set_value(FC[0], carry)

    memory_banks[MEMBANK.REG.value].set_value(address_to_subtract_from, result)
