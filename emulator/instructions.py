import emulator.memory
from compiler.instructions import I_SIZE, A_SIZE
from emulator.memory import MEMBANK

def run_instruction(memory_banks: list[emulator.memory.Memory], instruction: int, instruction_address: int):
    FUNCTIONS = {
        0: nop,
        6: ser,
        12: bsr,
        13: add,
        26: jmp,
        27: fnc
    }

    if instruction in FUNCTIONS:
        FUNCTIONS[instruction](memory_banks, instruction_address)


def get_arg_bits(memory: emulator.memory.Memory, instruction_address: int, arg_num: int):
    return memory.get_value(instruction_address + I_SIZE + A_SIZE * arg_num, A_SIZE)

def get_arg_value(memory: emulator.memory.Memory, instruction_address: int, arg_num: int):
    return emulator.memory.bit_array_to_int(get_arg_bits(memory, instruction_address, arg_num))


def nop(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    pass

def ser(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_load = get_arg_value(memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    memory_banks[MEMBANK.REG.value].set_value(address_to_load, memory_banks[MEMBANK.ROM.value].get_value(instruction_address + I_SIZE + A_SIZE, A_SIZE))

def bsr(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_shift = get_arg_value(memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    bits = memory_banks[MEMBANK.REG.value].get_value(address_to_shift, A_SIZE)
    bits.pop()
    bits.insert(0, 0)
    memory_banks[MEMBANK.REG.value].set_value(address_to_shift, bits)

def add(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_add_to = get_arg_value(memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    address_to_add_from = get_arg_value(memory_banks[MEMBANK.ROM.value], instruction_address, 1)

    arr1 = memory_banks[MEMBANK.REG.value].get_value(address_to_add_to, A_SIZE)
    arr2 = memory_banks[MEMBANK.REG.value].get_value(address_to_add_from, A_SIZE)
    
    result = []
    carry = False

    for bit1, bit2 in zip(reversed(arr1), reversed(arr2)):
        # Perform binary addition considering the carry
        sum_bits = bit1 + bit2 + carry

        # Calculate the result bit and the carry for the next iteration
        result_bit = sum_bits % 2
        carry = sum_bits // 2

        # Add the result bit to the beginning of the result list
        result.insert(0, result_bit == 1)

    FC = emulator.memory.mnemonic_to_adddress('FC')
    memory_banks[MEMBANK.REG.value].set_value(FC[0], [carry])

    memory_banks[MEMBANK.REG.value].set_value(address_to_add_to, result)

def jmp(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_jump_to = get_arg_bits(memory_banks[MEMBANK.ROM.value], instruction_address, 0)

    PC = emulator.memory.mnemonic_to_adddress('PC')
    memory_banks[MEMBANK.REG.value].set_value(PC[0], address_to_jump_to)

def fnc(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_jump_to = get_arg_bits(memory_banks[MEMBANK.ROM.value], instruction_address, 0)

    stack_size = emulator.memory.bit_array_to_int(memory_banks[MEMBANK.STK.value].get_value(0, A_SIZE))
    stack_size += 1

    memory_banks[MEMBANK.STK.value].set_value(0, emulator.memory.int_to_bit_array(stack_size, A_SIZE))

    # Gets Program Counter
    PC = emulator.memory.mnemonic_to_adddress('PC')
    program_counter = memory_banks[MEMBANK.REG.value].get_value(PC[0], PC[1])

    # Appends Program Counter to Stack
    memory_banks[MEMBANK.STK.value].set_value(stack_size * A_SIZE, program_counter)

    # Sets Program Counter to Jump Address
    memory_banks[MEMBANK.REG.value].set_value(PC[0], address_to_jump_to)
