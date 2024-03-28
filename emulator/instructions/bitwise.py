from emulator.instructions.run import get_arg_value
import emulator.memory
from compiler.instructions import I_SIZE, A_SIZE
from emulator.memory import MEMBANK


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
