import core as c

reg = {f"R{i}": 0 for i in range(32)}
mem = {(line, column): 0 for line in range(37) for column in range(10)}

gp = "gp" 

abi_names = {'zero': 0, 'ra': 1, 'sp': 2, 'gp': 3, 'tp': 4, 't0': 5, 't1': 6, 't2': 7, 's0/fp': 8, 's1': 9, 'a0': 10, 'a1': 11, 'a2': 12, 'a3': 13, 'a4': 14, 'a5': 15, 'a6': 16, 'a7': 17, 's2': 18, 's3': 19, 's4': 20, 's5': 21, 's6': 22, 's7': 23, 's8': 24, 's9': 25, 's10': 26, 's11': 27, 't3': 28, 't4': 29, 't5': 30, 't6': 31}
instruction_set = {
    "0110111": "lui",
    "0010111": "auipc",
    "0110011": {  
        "0000000_000": "add",
        "0100000_000": "sub",
        "0000000_111": "and_op", 
        "0000000_110": "or_op",
        "0000000_100": "xor_op",
        "0000000_010": "slt",
        "0000000_001": "sll", 
        "0000001_001": "srl",
        "0100000_001": "sra", 
    },
    "0010011": {  
        "000": "addi",
        "010": "slti",
        "011": "sltiu",
        "100": "xori",
        "111": "andi",
        "110": "ori"
    },
    "1110011": "csrrw",
}



def unpack_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode(mem, address):
    instruction = mem[address]


    _10alignment = instruction & 0b11  
    _62opcode = (instruction >> 2) & 0b111111  
    _117offset = (instruction >> 8) & 0b111  
    _1412function = (instruction >> 12) & 0b111  
    _1915source_register = (instruction >> 15) & 0b11111  
    _2420source_register = (instruction >> 20) & 0b11111  
    _3125offset = (instruction >> 25) & 0b1111111  



    offset_bin = f"{_3125offset:07b}{_117offset:05b}"
    offset = int(offset_bin, 2)

   
    rs1 = f"x{_2420source_register}"  
    rs2 = f"x{_1915source_register}" 
    
    
    decoded_instruction = {
        "offset": offset,
        "source_register_1": rs1,
        "source_register_2": rs2,
        "function": f"{_1412function:03b}",
        "opcode": f"{_62opcode:06b}",
        "alignment": f"{_10alignment:02b}"
    }

    return decoded_instruction


# exemplu adresa sub 1081282099 #

def unpack_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address):
    instruction = 1081282099

    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _117destination_register = (instruction >> 7) & 0b11111
    _1412function = (instruction >> 12) & 0b111
    _1915source_register = (instruction >> 15) & 0b11111
    _2420source_register = (instruction >> 20) & 0b11111
    _2625control_bits = (instruction >> 25) & 0b1111111 
    _3127opcode = (instruction >> 32) & 0b111 

    rs1 = [k for k, v in abi_names.items() if v == _2420source_register][0]
    rs2 = [k for k, v in abi_names.items() if v == _1915source_register][0]
    rd = [k for k, v in abi_names.items() if v == _117destination_register][0]

    opcode_bin = f"{_62opcode:05b}" + f"{_10alignment:02b}"
    print(opcode_bin)
    instruction_name = None

    if opcode_bin in instruction_set:
        if isinstance(instruction_set[opcode_bin], dict):
            func_bin = f"{_2625control_bits:07b}" + "_" + f"{_3127opcode:03b}"
            if func_bin in instruction_set[opcode_bin]:
                instruction_name = instruction_set[opcode_bin][func_bin]
            else:
                instruction_name = "Unknown function"
        else:
            instruction_name = instruction_set[opcode_bin]

    if instruction_name is None:
        instruction_name = "Unknown opcode"


    decoded_instruction = {
        "opcode": f"{_3127opcode:03b}",
        "control_bits": f"{_2625control_bits:07b}",
        "source_register_1": rs1,
        "source_register_2": rs2,
        "function": f"{_1412function:03b}",
        "destination_register": rd,
        "opcode": f"{_62opcode:05b}",
        "alignment": f"{_10alignment:02b}",
        "decoded_function": instruction_name
    }

    print(decoded_instruction)
    
    return decoded_instruction

def remove_trailing_zeros_and_revert(binary_value):
    binary_str = bin(binary_value)[2:]
    
    
    cleaned_binary = binary_str[::-1].lstrip('0')[::-1]
    reverted_binary = cleaned_binary[::-1]
    
    return int(reverted_binary, 2) if reverted_binary else 0

# addi t2, t1, 0x5 => 2684552083 #
# addi t2, t1, 0x27(39) => 3825402771 #
# addi t2, t1, 0x335(821) => 2898461587 #


def unpack__3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address):
    instruction = 2684552083

    print(f"{instruction:32b}")
    
    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _117destination_register = (instruction >> 7) & 0b11111
    _1412function = (instruction >> 12) & 0b111
    _1915source_register = (instruction >> 15) & 0b11111
    _3120immediate_value = (instruction >> 20) & 0b111111111111 
    
    value = remove_trailing_zeros_and_revert(_3120immediate_value)
    print(_3120immediate_value)
    rs1 = [k for k, v in abi_names.items() if v == _1915source_register][0]
    rd = [k for k, v in abi_names.items() if v == _117destination_register][0]

    opcode_bin = f"{_62opcode:05b}" + f"{_10alignment:02b}"
    instruction_name = None

    if opcode_bin in instruction_set:
        if isinstance(instruction_set[opcode_bin], dict):
            func_bin = f"{_1412function:03b}"
            if func_bin in instruction_set[opcode_bin]:
                instruction_name = instruction_set[opcode_bin][func_bin]
            else:
                instruction_name = "Unknown function"
        else:
            instruction_name = instruction_set[opcode_bin]

    if instruction_name is None:
        instruction_name = "Unknown opcode"


    decoded_instruction = {
        "immediate_value": f"{value}",
        "source_register_1": rs1,
        "function":f"{_1412function:03b}",
        "destination_register": rd,
        "opcode": f"{_62opcode:05b}",
        "alignment": f"{_10alignment:02b}",
        "decoded_function": instruction_name
    }

    print(decoded_instruction)
    
    return decoded_instruction


unpack__3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, 0)