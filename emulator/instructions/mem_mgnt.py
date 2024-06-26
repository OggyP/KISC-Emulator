from emulator.instructions.general_functions import get_arg_value
import emulator.memory
from compiler.instructions import I_SIZE, A_SIZE, MAX_INT
from emulator.memory import MEMBANK, bit_array_to_int


def ldr(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    
    register_address = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 1)
    address_from = bit_array_to_int(
        memory_banks[MEMBANK.REG.value].get_value(register_address, A_SIZE)
        )
    
    memory_banks[MEMBANK.REG.value].set_value(
        address_to,
        memory_banks[MEMBANK.RAM.value].get_value(address_from, A_SIZE),
    )


def ldm(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    register_address = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    address_to = bit_array_to_int(
        memory_banks[MEMBANK.REG.value].get_value(register_address, A_SIZE)
        )
    
    address_from = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 1)
    
    memory_banks[MEMBANK.RAM.value].set_value(
        address_to,
        memory_banks[MEMBANK.REG.value].get_value(address_from, A_SIZE),
    )


def mvr(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    address_from = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 1)
    memory_banks[MEMBANK.REG.value].set_value(
        address_to,
        memory_banks[MEMBANK.REG.value].get_value(address_from, A_SIZE),
    )


def mvm(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    register_1 = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    register_2 = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 1)
    
    address_to = bit_array_to_int(memory_banks[MEMBANK.REG.value].get_value(register_1, A_SIZE))
    address_from = bit_array_to_int(memory_banks[MEMBANK.REG.value].get_value(register_2, A_SIZE))

    memory_banks[MEMBANK.RAM.value].set_value(
        address_to,
        memory_banks[MEMBANK.RAM.value].get_value(address_from, A_SIZE),
    )


def ser(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    address_to_load = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    memory_banks[MEMBANK.REG.value].set_value(
        address_to_load,
        memory_banks[MEMBANK.ROM.value].get_value(
            instruction_address + I_SIZE + A_SIZE, A_SIZE
        ),
    )


def sem(memory_banks: list[emulator.memory.Memory], instruction_address: int):
    register_address = get_arg_value(
        memory_banks[MEMBANK.ROM.value], instruction_address, 0)
    address_to_load = memory_banks[MEMBANK.REG.value].get_value(register_address, A_SIZE)
    memory_banks[MEMBANK.RAM.value].set_value(
        bit_array_to_int(address_to_load),
        memory_banks[MEMBANK.ROM.value].get_value(
            instruction_address + I_SIZE + A_SIZE, A_SIZE
        ),
    )
