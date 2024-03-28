from emulator.instructions.general_functions import get_arg_bits
from emulator.instructions.run import get_arg_value
import emulator.memory
from compiler.instructions import I_SIZE, A_SIZE
from emulator.memory import MEMBANK


def comp(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_lhs = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    address_rhs = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 1)

    lhs_bits = memory_banks[MEMBANK.REG.value].get_value(address_lhs, A_SIZE)
    rhs_bits = memory_banks[MEMBANK.REG.value].get_value(address_rhs, A_SIZE)

    lhs = emulator.memory.bit_array_to_int(lhs_bits)
    rhs = emulator.memory.bit_array_to_int(rhs_bits)

    result = [False, lhs > rhs, lhs == rhs]
    CV = emulator.memory.mnemonic_to_adddress("CV")
    memory_banks[MEMBANK.REG.value].set_value(CV[0], result)


def jlt(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    CV = emulator.memory.mnemonic_to_adddress("CV")
    CV_bits = memory_banks[MEMBANK.REG.value].get_value(CV[0], 3)

    if CV_bits == [False, False, False]:
        jmp(memory_banks, instruction_address)


def jle(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    CV = emulator.memory.mnemonic_to_adddress("CV")
    CV_bits = memory_banks[MEMBANK.REG.value].get_value(CV[0], 3)

    if CV_bits == [False, False, False] or CV_bits == [False, False, True]:
        jmp(memory_banks, instruction_address)


def jeq(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    CV = emulator.memory.mnemonic_to_adddress("CV")
    CV_bits = memory_banks[MEMBANK.REG.value].get_value(CV[0], 3)

    if CV_bits == [False, False, True]:
        jmp(memory_banks, instruction_address)


def jge(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    CV = emulator.memory.mnemonic_to_adddress("CV")
    CV_bits = memory_banks[MEMBANK.REG.value].get_value(CV[0], 3)

    if CV_bits == [False, False, True] or CV_bits == [False, True, False]:
        jmp(memory_banks, instruction_address)


def jgt(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    CV = emulator.memory.mnemonic_to_adddress("CV")
    CV_bits = memory_banks[MEMBANK.REG.value].get_value(CV[0], 3)

    if CV_bits == [False, True, False]:
        jmp(memory_banks, instruction_address)


def jne(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    CV = emulator.memory.mnemonic_to_adddress("CV")
    CV_bits = memory_banks[MEMBANK.REG.value].get_value(CV[0], 3)

    if CV_bits != [False, False, True]:
        jmp(memory_banks, instruction_address)


def jmp(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_jump_to = get_arg_bits(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)

    PC = emulator.memory.mnemonic_to_adddress("PC")
    memory_banks[MEMBANK.REG.value].set_value(PC[0], address_to_jump_to)


def fnc(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_jump_to = get_arg_bits(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)

    stack_size = emulator.memory.bit_array_to_int(
        memory_banks[MEMBANK.STK.value].get_value(0, A_SIZE))
    stack_size += 1

    memory_banks[MEMBANK.STK.value].set_value(
        0, emulator.memory.int_to_bit_array(stack_size, A_SIZE))

    # Gets Program Counter
    PC = emulator.memory.mnemonic_to_adddress("PC")
    program_counter = memory_banks[MEMBANK.REG.value].get_value(PC[0], PC[1])

    # Appends Program Counter to Stack
    memory_banks[MEMBANK.STK.value].set_value(
        stack_size * A_SIZE, program_counter)

    # Sets Program Counter to Jump Address
    memory_banks[MEMBANK.REG.value].set_value(PC[0], address_to_jump_to)
