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
    # Convert boolean values to bytes
    bytes_data = struct.pack('?' * len(bool_list), *bool_list)
    
    # Write bytes to file
    with open(filename, 'wb') as file:
        file.write(bytes_data)

def load_bool_list_from_binary(filename):
    with open(filename, 'rb') as file:
        # Read bytes from file
        bytes_data = file.read()
        
        # Unpack bytes into boolean values
        bool_list = struct.unpack('?' * (len(bytes_data) // struct.calcsize('?')), bytes_data)
    
    return bool_list