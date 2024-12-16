import re
from idlelib.debugobj_r import remote_object_tree_item
from idlelib.editor import keynames

abi_names = {'zero': 0, 'ra': 1, 'sp': 2, 'gp': 3, 'tp': 4, 't0': 5, 't1': 6, 't2': 7, 's0/fp': 8, 's1': 9, 'a0': 10, 'a1': 11, 'a2': 12, 'a3': 13, 'a4': 14, 'a5': 15, 'a6': 16, 'a7': 17, 's2': 18, 's3': 19, 's4': 20, 's5': 21, 's6': 22, 's7': 23, 's8': 24, 's9': 25, 's10': 26, 's11': 27, 't3': 28, 't4': 29, 't5': 30, 't6': 31}

def is_empty_string(s):
    return not any(c.isprintable() and not c.isspace() for c in s)
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
    _3127immediate = dec2bin_str(immediate_dec, 31, 0)

    register = params[0]
    register_index = abi_names[register]
    _117destinationRegister = dec2bin_str(register_index, 11, 7)

    _62opcode = opcode
    _10alignment = "11"

    return  bin2dec(_3127immediate[31:12-1:-1] + _117destinationRegister + _62opcode + _10alignment)

def _3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, function, opcode):
    # addi, slti, sltiu, xori, ori, andi
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
    print("imm",_3120immediate)
    return bin2dec(_3120immediate[::-1] + _1915source_register + _1412function + _117destination_register + _62opcode + _10alignment)

def _3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(params, function, opcode, _3127opcode, _2625control_bits):
    #slli, srli, srai
    shamt = params[2]
    shamt_dec = hex2dec(shamt)
    _2420shamt = dec2bin_str(shamt_dec, 24, 20)

    rs1_index = abi_names[params[1]]
    _1915source_register = dec2bin_str(rs1_index, 19, 15)

    _1412function = function

    rd_index = abi_names[params[0]]
    _117destination_register = dec2bin_str(rd_index, 11, 7)

    _62opcode = opcode
    _10alignment = "11"

    return bin2dec(_3127opcode + _2625control_bits + _2420shamt + _1915source_register + _1412function + _117destination_register + _62opcode + _10alignment)

def _3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _1412function, _62opcode, _3127opcode, _2625control_bits):
    #add sub
    rs2_index = abi_names[params[2]]
    _2420source_register = dec2bin_str(rs2_index, 24, 20)

    rs1_index = abi_names[params[1]]
    _1915source_register = dec2bin_str(rs1_index, 19, 15)

    rd_index = abi_names[params[0]]
    _117destination_register = dec2bin_str(rd_index, 11, 7)

    _10alignment = "11"

    return bin2dec(_3127opcode + _2625control_bits + _2420source_register + _1915source_register + _1412function + _117destination_register + _62opcode + _10alignment)

def _3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(labels, params, _1412function, _62opcode):
    offset = params[1]
    if offset in labels:
        return 1/0 # TODO :)
    _3120offset = dec2bin_str(hex2dec(offset), 31, 20)

    _1915source_register = dec2bin_str(abi_names[params[2]], 19, 15)
    _117destination_register = dec2bin_str(abi_names[params[0]], 11, 7)
    _10alignment = "11"

    return bin2dec(_3120offset[::-1] + _1915source_register + _1412function + _117destination_register + _62opcode + _10alignment)

def _3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function, _62opcode):

    offset = params[1]
    if offset in labels:
        return 1/0 # TODO :)
    offset_in_bin = dec2bin_str(hex2dec(offset), 31, 20)
    _3125offset = offset_in_bin[11:5 - 1 : -1]

    _2420source_register = dec2bin_str(abi_names[params[0]], 24, 20)
    _1915source_register = dec2bin_str(abi_names[params[2]], 19, 15)

    _117offset = offset_in_bin[4::-1]
    _10alignment = "11"

    return bin2dec(_3125offset + _2420source_register + _1915source_register + _1412function + _117offset + _62opcode + _10alignment)

def _jal(labels, params):
    offset = params[1]
    if offset in labels:
        offset_in_bin = dec2bin_str(labels.index(offset), 20, 0)
    else:
        offset_in_bin = dec2bin_str(hex2dec(offset), 20, 0)

    rd_index = abi_names[params[0]]
    rd = dec2bin_str(rd_index, 11, 7)

    return bin2dec(offset_in_bin[20]+ offset_in_bin[10:1-1:-1] + offset_in_bin[11] + offset_in_bin[19:12-1:-1] + rd + "11011" + "11")

def _jalr(labels, params):
    offset = params[2]
    if offset in labels:
        offset_in_bin = dec2bin_str(labels.index(offset), 31, 20)
    else:
        offset_in_bin = dec2bin_str(hex2dec(offset), 31, 20)

    rs = dec2bin_str(abi_names[params[1]], 19, 15)
    rd = dec2bin_str(abi_names[params[0]], 11, 7)

    return bin2dec(offset_in_bin[::-1] + rs + "000" + rd + "11001" + "11")

def b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function, _62opcode):
    offset = params[2]
    if offset in labels:
        offset_in_bin = dec2bin_str(labels.index(offset), 12, 0)
    else:
        offset_in_bin = dec2bin_str(hex2dec(offset), 12, 0)

    rs2 = dec2bin_str(abi_names[params[1]], 24, 20)
    rs1 = dec2bin_str(abi_names[params[0]], 19, 15)
    _10alignment = "11"

    return bin2dec(offset_in_bin[12] + offset_in_bin[10: 5 -1: -1] + rs2 + rs1 + _1412function + offset_in_bin[4: 1 - 1:-1] + offset_in_bin[11] + _62opcode + _10alignment )

functions = {
    "lui": lambda labels, params: _3112immediate_117destination_register_62opcode_10alignment(params, "01101"), # lui t2, 0x12345
    "auipc": lambda labels, params: _3112immediate_117destination_register_62opcode_10alignment(params, "00101"), # auipc x6, 0x12345

    "addi": lambda labels, params:_3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "000", "00100"), # addi rd, rs1, imm -> addi x3, x2, 0x10
    "slti": lambda labels, params:_3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "010", "00100"),#slti rd, rs1, imm -> slti x3, x2, 0x10
    "sltiu": lambda labels, params:_3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "011", "00100"),
    "xori": lambda labels, params:_3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "100", "00100"),
    "ori": lambda labels, params:_3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "110", "00100"),
    "andi": lambda labels, params:_3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "111", "00100"),

    "slli": lambda labels, params:_3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "001", "00100", "00000", "00"), # slli rd, rs1, shamt -> slli x2, x1, 0x2
    "srli": lambda labels, params:_3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "101", "00100", "00000", "00"),
    "srai": lambda labels, params:_3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "101", "00100", "01000", "00"),

    "add":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "000", "01100", "00000", "00"),
    "sub":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "000", "01100", "01000", "00"),
    "sll":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="001", _62opcode="01100"),
    "slt":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="010", _62opcode="01100"),
    "sltu":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="011", _62opcode="01100"),
    "xor":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="100", _62opcode="01100"),
    "srl":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="101", _62opcode="01100"),
    "sra":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="01000",_2625control_bits="00", _1412function="101", _62opcode="01100"),
    "or":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="110", _62opcode="01100"),
    "and":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="111", _62opcode="01100"),

    "ecall": lambda labels, params: bin2dec("00000" + "00" + "00000" + "00000" + "000" + "00000" + "11100" + "11"),
    "ebreak": lambda labels, params: bin2dec("00000" + "00" + "00001" + "00000" + "000" + "00000" + "11100" + "11"),
    "uret": lambda labels, params: bin2dec("00000" + "00" + "00010" + "00000" + "000" + "00000" + "11100" + "11"),
    "sret": lambda labels, params: bin2dec("00010" + "00" + "00010" + "00000" + "000" + "00000" + "11100" + "11"),
    "mret": lambda labels, params: bin2dec("00110" + "00" + "00010" + "00000" + "000" + "00000" + "11100" + "11"),
    "wfi": lambda labels, params: bin2dec("00010" + "00" + "00101" + "00000" + "000" + "00000" + "11100" + "11"),

    "lb" : lambda labels, params: _3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(labels, params, _1412function="000", _62opcode="00000"),
    "lh" : lambda labels, params: _3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(labels, params, _1412function="001", _62opcode="00000"),
    "lw" : lambda labels, params: _3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(labels, params, _1412function="010", _62opcode="00000"),
    "lbu" : lambda labels, params: _3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(labels, params, _1412function="100", _62opcode="00000"),
    "lhu" : lambda labels, params: _3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(labels, params, _1412function="101", _62opcode="00000"),

    "sb": lambda labels, params: _3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="000", _62opcode="01000"),
    "sh": lambda labels, params: _3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="001", _62opcode="01000"),
    "sw": lambda labels, params: _3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="010", _62opcode="01000"),

    "jal": lambda labels, params: _jal(labels, params),
    "jalr":lambda labels, params: _jalr(labels, params),

    "beq": lambda labels, params: b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="000", _62opcode="11000"),
    "bne": lambda labels, params: b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="001", _62opcode="11000"),
    "blt": lambda labels, params: b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="100", _62opcode="11000"),
    "bge": lambda labels, params: b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="101", _62opcode="11000"),
    "bltu": lambda labels, params: b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="110", _62opcode="11000"),
    "bgeu": lambda labels, params: b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="111", _62opcode="11000"),

    #TODO: fence
    "fence": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
    "fence.i": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
    "sfence.vma": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
    "csrrw": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
    "csrrs": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
    "csrrc": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
    "csrrwi": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
    "csrrsi": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
    "csrrci": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
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
        if is_empty_string(relevant):
            continue

        label, operation = extract_label_and_operation(relevant)

        operation = operation.lstrip(" \t\n")
        words =   re.split(r'[ ,()]+', operation)

        instruction =  words[0]
        params = words[1:]

        labels.append(label)
        parameters.append(params)
        instructions.append(instruction)

    not_found_instr = []

    for i, instruction in enumerate(instructions):
        try:
            reduced_to_number = functions[instruction](labels, parameters[i])
            print(reduced_to_number)
        except KeyError:
            # print(f"label:[{labels[i]}]", end="")
            # print(f"instruction:[{instruction}]", end="")
            # print( f"params:[{parameters[i]}]")
            not_found_instr.append(instruction)


    print("instructions not founded/erroed:",not_found_instr)


# print(functions["beq"]([], ["t1", "t2", "0x10"]))
mock_code = """
    .data
num1:   .word 0x5              ; First number (5)
num2:   .word 0x10             ; Second number (10)
result: .word 0x0              ; To store the result
    .text
    .globl _start
_start: ; Load num1 into register t0
    la t0, num1              ; Load address of num1 into t0 #la
    lw t1, 0x0(t0)             ; Load value of num1 into t1 ; Load num2 into register t2
    la t0, num2              ; Load address of num2 into t0
    lw t2, 0x0(t0)             ; Load value of num2 into t2 ; Add t1 and t2, store the result in t3
    add t3, t1, t2           ; t3 = t1 + t2 ; Store the result in memory (result)
    la t0, result            ; Load address of result into t0
    sw t3, 0x0(t0)             ; Store the value of t3 into result ; Example loop: decrement t3 until 0
loop:
    beq t3, a0, end          ; If t3 == 0, exit loop
    jal a0, loop             ; Jump back to loop
end: ; Exit program
    li a7, 0x10                ; Load ecall code for exit (10) into a7
    ecall                    ; Make the system call
"""
assemble_code(mock_code, 8)