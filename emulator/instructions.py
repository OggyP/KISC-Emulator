import emulator.memory
from compiler.instructions import I_SIZE, A_SIZE

def run_instruction(memory: emulator.memory.Memory, instruction: int, instruction_address: int):
    FUNCTIONS = {
        2: load,
        7: bsr,
        8: add,
    }

    FUNCTIONS[instruction](memory, instruction_address)


def load(memory: emulator.memory.Memory, instruction_address: int):
    address_to_load = emulator.memory.bit_array_to_int(memory.get_value(instruction_address + I_SIZE, A_SIZE))
    memory.set_value(address_to_load, memory.get_value(instruction_address + I_SIZE + A_SIZE, A_SIZE))

def bsr(memory: emulator.memory.Memory, instruction_address: int):
    address_to_shift = emulator.memory.bit_array_to_int(memory.get_value(instruction_address + I_SIZE, A_SIZE))
    bits = memory.get_value(address_to_shift, A_SIZE)
    bits.pop()
    bits.insert(0, 0)
    memory.set_value(address_to_shift, bits)

def add(memory: emulator.memory.Memory, instruction_address: int):
    address_to_add_to = emulator.memory.bit_array_to_int(memory.get_value(instruction_address + I_SIZE, A_SIZE))
    address_to_add_from = emulator.memory.bit_array_to_int(memory.get_value(instruction_address + I_SIZE + A_SIZE, A_SIZE))

    arr1 = memory.get_value(address_to_add_to, A_SIZE)
    arr2 = memory.get_value(address_to_add_from, A_SIZE)
    
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
    memory.set_value(FC[0], [carry])

    memory.set_value(address_to_add_to, result)
