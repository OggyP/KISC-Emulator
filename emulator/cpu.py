import logging
import emulator.memory
import emulator.instructions.run
import compiler.instructions
from compiler.instructions import I_SIZE, A_SIZE, INSTRUCTION_NUM_TO_NAME
from emulator.memory import MEMBANK

logger = logging.getLogger(__name__)


class CPU:
    def __init__(self, memory_banks: list[emulator.memory.Memory]):
        self.memory_banks = memory_banks
        self.running = True

    def tick(self):
        PC = emulator.memory.mnemonic_to_adddress('PC')
        RI = emulator.memory.mnemonic_to_adddress('RI')

        self.memory_banks[MEMBANK.REG.value].copy_bits(PC[0], RI[0], PC[1])

        instruction_address = emulator.memory.bit_array_to_int(
            self.memory_banks[MEMBANK.REG.value].get_value(RI[0], RI[1]))
        instruction_bits = self.memory_banks[MEMBANK.ROM.value].get_value(
            instruction_address, I_SIZE)
        instruction = emulator.memory.bit_array_to_int(instruction_bits)

        if instruction == 1:  # hits return
            logger.debug("Hit ret")
            stack_size = emulator.memory.bit_array_to_int(
                self.memory_banks[MEMBANK.STK.value].get_value(0, A_SIZE))
            if stack_size == 0:
                self.running = False
            else:
                self.memory_banks[MEMBANK.REG.value].set_value(
                    PC[0], self.memory_banks[MEMBANK.STK.value].get_value(A_SIZE * stack_size, A_SIZE))
                self.memory_banks[MEMBANK.STK.value].set_value(
                    0, emulator.memory.int_to_bit_array(stack_size - 1, A_SIZE))
            return

        instruction_size = I_SIZE + A_SIZE * \
            compiler.instructions.INSTRUCTION_SIZE[instruction]

        self.memory_banks[MEMBANK.REG.value].add_value(
            PC[0], instruction_size, PC[1])

        logger.debug(f"executing {instruction} ({INSTRUCTION_NUM_TO_NAME[instruction]})")

        emulator.instructions.run.run_instruction(
            self.memory_banks, instruction, instruction_address)
