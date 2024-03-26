import emulator.memory
import emulator.instructions
import compiler.instructions
from compiler.instructions import I_SIZE, A_SIZE

class CPU:
    def __init__(self, memory: emulator.memory.Memory):
        self.memory = memory
        self.running = True

    def tick(self):
        PC = emulator.memory.mnemonic_to_adddress('PC')
        RI = emulator.memory.mnemonic_to_adddress('RI')

        self.memory.copy_bits(PC[0], RI[0], PC[1])

        instruction_address = emulator.memory.bit_array_to_int(self.memory.get_value(RI[0], RI[1]))
        instruction_bits = self.memory.get_value(instruction_address, I_SIZE)
        instruction = emulator.memory.bit_array_to_int(instruction_bits)

        if instruction == 0:
            self.running = False
            return

        instruction_size = I_SIZE + A_SIZE * compiler.instructions.INSTRUCTION_SIZE[instruction]
        
        self.memory.add_value(PC[0], instruction_size, PC[1])

        print("EXECUTING: ", instruction)

        emulator.instructions.run_instruction(self.memory, instruction, instruction_address)
        