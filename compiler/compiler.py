import struct
import compiler.instructions
import emulator.memory

def compile(file_path: str, start_address: int):
    # Open the file and read its contents
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n").split(';')[0].strip() for line in file.readlines()]

    instructions_binary = []
    label_addresses = {}
    label_refs = []

    lines.insert(0, 'jmp .start')

    for line in lines:
        if len(line):
            current_address = start_address + len(instructions_binary)
            if line.startswith(compiler.instructions.LABEL_SYMBOL):
                label_addresses[line.lstrip(compiler.instructions.LABEL_SYMBOL)] = current_address
            else:
                compiled_info = compiler.instructions.line_to_binary(line, current_address)
                instructions_binary += compiled_info["bin"]
                label_refs += compiled_info["labels"]

    for label_ref in label_refs:
        label = label_ref["label"]
        if not label in label_addresses:
            raise KeyError(f"Missing label \"{label}\"")
        label_address = label_addresses[label]
        insert_address = label_ref["address"]
        instructions_binary[insert_address : insert_address + compiler.instructions.A_SIZE] = emulator.memory.int_to_bit_array(label_address, compiler.instructions.A_SIZE)

    return instructions_binary

def save_bool_list_to_binary(bool_list, filename):
    # Calculate the number of bytes needed to store the boolean values
    num_bytes = (len(bool_list) + 7) // 8
    
    # Initialize an empty byte array to store packed boolean values
    packed_bytes = bytearray(num_bytes)
    
    # Pack boolean values into individual bits
    for i, value in enumerate(bool_list):
        byte_index = i // 8
        bit_index = i % 8
        if value:
            packed_bytes[byte_index] |= (1 << bit_index)
        # else: False is represented by 0, which is already the default value in the bytearray
        
    # Write bytes to file
    with open(filename, 'wb') as file:
        file.write(packed_bytes)

def load_bool_list_from_binary(filename):
    bool_list = []
    with open(filename, 'rb') as file:
        byte = file.read(1)
        while byte:
            for i in range(8):
                bool_list.append(bool(byte[0] & (1 << i)))
            byte = file.read(1)
    return bool_list

def save_punch_card_to_file(bits_list, filename):
    with open(filename, 'w') as f:
        for i in range(0, len(bits_list), 6):
            bits_line = ''.join('1' if bit else '0' for bit in bits_list[i:i+6])
            f.write(bits_line + '\n')