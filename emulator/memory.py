from enum import Enum

def hex_to_int(hex_value: str):
    try:
        hex_value = hex_value.lstrip("#")
        integer_value = int(hex_value, 16)
        return integer_value
    except ValueError:
        print("Invalid hexadecimal value.")
        return None


def int_to_hex(integer_value: int):
    try:
        hex_string = hex(integer_value)
        return hex_string
    except ValueError:
        print("Invalid integer value.")
        return None


def int_to_bit_array(num, bits):
    # Convert the number to binary string
    binary_str = bin(num)[2:]  # Remove '0b' prefix

    # Pad the binary string with leading zeros to make it 12 bits long
    padded_binary_str = binary_str.zfill(bits)

    # Convert the padded binary string to a list of booleans
    binary_array = [bit == "1" for bit in padded_binary_str]

    return binary_array


def bit_array_to_int(binary_array):
    # Convert the binary array to a binary string
    binary_str = "".join("1" if bit else "0" for bit in binary_array)

    # Convert the binary string to an integer
    num = int(binary_str, 2)

    return num


def display_binary_array(binary_array):
    # Convert each boolean value to '1' if True, '0' if False
    binary_str = "".join("1" if bit else "0" for bit in binary_array)
    return binary_str


def mnemonic_to_adddress(mnemonic):
    RESERVED_ADDRESSES = {
        "PC": ("#000", 12),
        "RI": ("#00c", 12),
        "RA": ("#018", 12),
        "RB": ("#024", 12),
        "RC": ("#030", 12),
        "R0": ("#03c", 12),
        "R1": ("#048", 12),
        "R2": ("#054", 12),
        "R3": ("#060", 12),
        "FC": ("#06c", 1),
        "FI": ("#06d", 1),
        "CV": ("#075", 3),
    }

    if not mnemonic in RESERVED_ADDRESSES:
        raise MemoryError(f"Reserved Address {mnemonic} does not exist")

    return (
        hex_to_int(RESERVED_ADDRESSES[mnemonic][0]),
        RESERVED_ADDRESSES[mnemonic][1],
    )

class MEMBANK(Enum):
    REG = 0
    RAM = 1
    STK = 2
    ROM = 3


class Memory:
    def __init__(self, max_address: int):
        self.memory = [False] * max_address
        print(f"Initialised memory up to {int_to_hex(max_address)}")

    def get_value(self, address: int, length: int):
        return self.memory[address : address + length]

    def set_value(self, address: int, bits: list[bool]):
        self.memory[address : address + len(bits)] = bits

    def copy_bits(self, from_address, to_address, length):
        self.set_value(to_address, self.get_value(from_address, length))

    def add_value(self, address, value, length):
        current_value = bit_array_to_int(self.get_value(address, length))
        current_value += value
        self.set_value(address, int_to_bit_array(current_value, length))
