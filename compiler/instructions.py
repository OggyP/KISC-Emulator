import emulator.memory
import json
import logging

logger = logging.getLogger(__name__)

INSTRUCTION_SET_FILE = "compiler/instruction_set.json"

with open(INSTRUCTION_SET_FILE, 'r') as file:
    data = json.load(file)

INSTRUCTION_SET = {}
INSTRUCTION_NUM_TO_NAME = {}
INSTRUCTION_SIZE = {}
for key, value in data.items():
    instruction_num = emulator.memory.hex_to_int(value[0])
    INSTRUCTION_SET[key] = [instruction_num, value[1]]
    INSTRUCTION_SIZE[instruction_num] = value[1]
    INSTRUCTION_NUM_TO_NAME[instruction_num] = key

I_SIZE = 6 # instruction size
A_SIZE = 12 # address / number size
MAX_INT = 2**A_SIZE - 1

LABEL_SYMBOL = '.'

def line_to_binary(line: str, current_address: int):
    args = line.split(' ')
    instruction = args.pop(0)

    binary_array = []
    labels = []

    if instruction in INSTRUCTION_SET:
        binary_array += emulator.memory.int_to_bit_array(INSTRUCTION_SET[instruction][0], I_SIZE)
    else:
        raise SyntaxError(str(instruction) + " is not a valid instruction!")
    # Increment by instruction size
    current_address += I_SIZE

    for arg_num in range(INSTRUCTION_SET[instruction][1]):
        arg = args[arg_num]
        if arg.startswith('#'):
            value = emulator.memory.hex_to_int(arg)
        elif arg.startswith('$'):
            value = emulator.memory.bin_to_int(arg)
        elif arg.isdigit():
            value = int(arg)
        elif arg.startswith(LABEL_SYMBOL):
            value = 0
            labels.append({
                "label": arg.lstrip(LABEL_SYMBOL),
                "address": current_address
            })
        else:
            value = emulator.memory.mnemonic_to_adddress(arg)[0]

        # Increment by arguement size
        current_address += A_SIZE


        binary_array += emulator.memory.int_to_bit_array(value, A_SIZE)

    logger.debug(f"{instruction} | {args}")
    # logger.debug(emulator.memory.display_binary_array(binary_array))

    return {
        "bin": binary_array,
        "labels": labels
    }