import logging
import sys
import emulator.memory
import emulator.cpu
import compiler.instructions
import compiler.compiler
from compiler.instructions import I_SIZE, A_SIZE
from emulator.memory import MEMBANK

logger = logging.getLogger(__name__)


def main(file_path: str):
    if __debug__:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    STARTING_ADDRESS = 0

    if file_path.endswith("kln"):
        instructions_binary = compiler.compiler.compile(
            file_path, STARTING_ADDRESS)

        # Save compiled program
        compiler.compiler.save_bool_list_to_binary(
            instructions_binary, "program.kbin")
    else:
        instructions_binary = compiler.compiler.load_bool_list_from_binary(
            file_path)

    compiler.compiler.save_punch_card_to_file(
        instructions_binary, "program.kcard")

    # Initialise Memory

    ROM = emulator.memory.Memory(len(instructions_binary))
    RAM = emulator.memory.Memory(128)
    REG = emulator.memory.Memory(128)
    STK = emulator.memory.Memory(128)

    ROM.set_value(STARTING_ADDRESS, instructions_binary)
    REG.set_value(
        emulator.memory.mnemonic_to_adddress("PC")[0],
        emulator.memory.int_to_bit_array(STARTING_ADDRESS, A_SIZE),
    )

    # RAM = emulator.memory.Memory(128)

    # Run Program
    cpu = emulator.cpu.CPU([REG, RAM, STK, ROM])
    while cpu.running:
        cpu.tick()

    logger.info("Program Haulted")


if len(sys.argv) != 2:
    print("Usage: python main.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

main(file_path)
