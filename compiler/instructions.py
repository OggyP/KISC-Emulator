import emulator.memory
import json

INSTRUCTION_SET_FILE = "compiler/instruction_set.json"

with open(INSTRUCTION_SET_FILE, 'r') as file:
    data = json.load(file)

INSTRUCTION_SET = {}
INSTRUCTION_SIZE = {}
for key, value in data.items():
    INSTRUCTION_SET[key] = [emulator.memory.hex_to_int(value[0]), value[1]]
    INSTRUCTION_SIZE[emulator.memory.hex_to_int(value[0])] = value[1]

I_SIZE = 6 # instruction size
A_SIZE = 12 # address / number size

def line_to_binary(line: str):
    args = line.split(' ')
    instruction = args.pop(0)

    binary_array = []

    binary_array += emulator.memory.int_to_bit_array(INSTRUCTION_SET[instruction][0], I_SIZE)

    for arg_num in range(INSTRUCTION_SET[instruction][1]):
        arg = args[arg_num]
        if arg.startswith('#'):
            value = emulator.memory.hex_to_int(arg)
        elif arg.isdigit():
            value = int(arg)
        else:
            value = emulator.memory.mnemonic_to_adddress(arg)[0]

        binary_array += emulator.memory.int_to_bit_array(value, A_SIZE)

    print(instruction, args)
    print(emulator.memory.display_binary_array(binary_array))

    return binary_array