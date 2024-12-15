import re

abi_names = {'zero': 0, 'ra': 1, 'sp': 2, 'gp': 3, 'tp': 4, 't0': 5, 't1': 6, 't2': 7, 's0/fp': 8, 's1': 9, 'a0': 10, 'a1': 11, 'a2': 12, 'a3': 13, 'a4': 14, 'a5': 15, 'a6': 16, 'a7': 17, 's2': 18, 's3': 19, 's4': 20, 's5': 21, 's6': 22, 's7': 23, 's8': 24, 's9': 25, 's10': 26, 's11': 27, 't3': 28, 't4': 29, 't5': 30, 't6': 31}

def hex2dec(hex_string):
    try:
        decimal_value = int(hex_string, 16)
        return decimal_value
    except ValueError:
        print(f"error in: hex2dec({hex_string})")
        return "Invalid hexadecimal input"

def dec2bin_str(nr, start_pos, end_pos):
    binary_str = bin(nr)[2:]
    binary_str = binary_str.zfill(start_pos + 1)
    rez_len = start_pos - end_pos + 1
    return binary_str[len(binary_str) - rez_len:]

def bin2dec(binary_str):
    if len(binary_str) != 32:
        print("n are 32 biti")

    decimal_value = int(binary_str, 2)
    return decimal_value

def _3112immediate_117destination_register_62opcode_10alignment(params, opcode):
    # lui, auipc,
    immediate = params[1]
    immediate_dec = hex2dec(immediate)
    _3127immediate = dec2bin_str(immediate_dec, 31, 12)

    register = params[0]
    register_index = abi_names[register]
    _117destinationRegister = dec2bin_str(register_index, 11, 7)

    _62opcode = opcode
    _10alignment = "11"

    return  bin2dec(_3127immediate + _117destinationRegister + _62opcode + _10alignment)

def _3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, function, opcode):
    # addi,
    imm = params[2]
    imm_dec = hex2dec(imm)
    _3120immediate = dec2bin_str(imm_dec, 31, 20)

    rs_index = abi_names[params[1]]
    _1915source_register = dec2bin_str(rs_index, 19, 15)

    _1412function = function

    rd_index = abi_names[params[0]]
    _117destination_register = dec2bin_str(rd_index, 11, 7)

    _62opcode = opcode
    _10alignment = "11"

    return bin2dec(_3120immediate + _1915source_register + _1412function + _117destination_register + _62opcode + _10alignment)

functions = {
    "lui": lambda label, params: _3112immediate_117destination_register_62opcode_10alignment(params, "01101"), # lui t2, 0x12345
    "auipc": lambda label, params: _3112immediate_117destination_register_62opcode_10alignment(params, "00101"), # auipc x6, 0x12345
    "addi": lambda label, params:_3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "000", "00100"), # addi rd, rs1, imm -> addi x3, x2, 0x10
    "slti": 4 #slti rd, rs1, imm -> slti x3, x2, 0x10

}

def extract_label_and_operation(text):
    if ":" in text:
        parts = text.split(":", 1)
        label = parts[0].strip()
        code = parts[1].strip()
        return label, code
    return "", text.strip()

def assemble_code(code, memory):
    labels = []
    parameters = []
    instructions = []

    for line in code.splitlines():
        relevant = line.split(";", 1)[0] if ";" in line else line
        label, operation = extract_label_and_operation(relevant)

        operation = operation.lstrip(" \t\n")
        words =   re.split(r'[ ,]+', operation)

        instruction = words[0]
        params = words[1:]

        labels.append(label)
        parameters.append(params)
        instructions.append(instruction)

    for i, instruction in enumerate(instructions):
        pass
        print(f"label:[{labels[i]}]", end="")
        print(f"instruction:[{instruction}]", end="")
        print( f"params:[{parameters[i]}]")
