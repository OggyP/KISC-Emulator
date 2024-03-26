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