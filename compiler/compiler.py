import struct
import compiler.instructions
import emulator.memory

def compile(file_path: str):

    # Open the file and read its contents
    with open(file_path, "r") as file:
        lines = [line.rstrip("\n") for line in file.readlines()]

    instructions_binary = []

    for line in lines:
        instructions_binary += compiler.instructions.line_to_binary(line)

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