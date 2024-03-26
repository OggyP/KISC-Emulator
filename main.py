import sys
import emulator.memory
import emulator.cpu
import compiler.instructions
import compiler.compiler
from compiler.instructions import I_SIZE, A_SIZE


def main(file_path: str):
    if file_path.endswith("kln"):
        instructions_binary = compiler.compiler.compile(file_path)

        # Save compiled program
        compiler.compiler.save_bool_list_to_binary(instructions_binary, "program.kbin")
    else:
        instructions_binary = compiler.compiler.load_bool_list_from_binary(file_path)

    # Initialise Memory
    memory = emulator.memory.Memory(128 + len(instructions_binary))
    STARTING_ADDRESS = emulator.memory.hex_to_int("#080")
    memory.set_value(STARTING_ADDRESS, instructions_binary)
    memory.set_value(
        emulator.memory.mnemonic_to_adddress("PC")[0],
        emulator.memory.int_to_bit_array(STARTING_ADDRESS, A_SIZE),
    )

    # Run Program
    cpu = emulator.cpu.CPU(memory)
    while cpu.running:
        cpu.tick()

    print("Hit nop")

    RA = emulator.memory.mnemonic_to_adddress("RA")
    print("RA:", emulator.memory.bit_array_to_int(memory.get_value(RA[0], RA[1])))


if len(sys.argv) != 2:
    print("Usage: python main.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

main(file_path)
