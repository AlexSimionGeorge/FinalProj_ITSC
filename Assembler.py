import re

abi_names = {'zero': 0, 'ra': 1, 'sp': 2, 'pc': 3, 'tp': 4, 't0': 5, 't1': 6, 't2': 7, 's0': 8, 's1': 9, 'a0': 10, 'a1': 11, 'a2': 12, 'a3': 13, 'a4': 14, 'a5': 15, 'a6': 16, 'a7': 17, 's2': 18, 's3': 19, 's4': 20, 's5': 21, 's6': 22, 's7': 23, 's8': 24, 's9': 25, 's10': 26, 's11': 27, 't3': 28, 't4': 29, 't5': 30, 't6': 31}

def is_empty_string(s):
    return not any(c.isprintable() and not c.isspace() for c in s)

def hex2dec(hex_string):
    try:
        decimal_value = int(hex_string, 16)
        # print("hex:", hex_string, "dec:", decimal_value)
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

    print(_3127immediate[31:12-1:-1] + _117destinationRegister + _62opcode + _10alignment)

    return  bin2dec(_3127immediate[31:12-1:-1] + _117destinationRegister + _62opcode + _10alignment)

def _3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, function, opcode):
    # addi, slti, sltiu, xori, ori, andi
    imm = params[2]
    imm_dec = hex2dec(imm)

    _3120immediate = dec2bin_str(imm_dec, 31, 20)
    # print("ADI_________ IMM hex:", imm, "bin:", _3120immediate)

    rs_index = abi_names[params[1]]
    _1915source_register = dec2bin_str(rs_index, 19, 15)

    _1412function = function

    rd_index = abi_names[params[0]]
    _117destination_register = dec2bin_str(rd_index, 11, 7)

    _62opcode = opcode
    _10alignment = "11"

    # print("PLEACA___________",_3120immediate + _1915source_register + _1412function + _117destination_register + _62opcode + _10alignment)
    return bin2dec(_3120immediate + _1915source_register + _1412function + _117destination_register + _62opcode + _10alignment)

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

def _3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignmentV2(params, _1412function, _62opcode, _3127opcode, _2625control_bits):
    #amo
    rs2_index = abi_names[params[1]]
    _2420source_register = dec2bin_str(rs2_index, 24, 20)

    rs1_index = abi_names[params[2]]
    _1915source_register = dec2bin_str(rs1_index, 19, 15)

    rd_index = abi_names[params[0]]
    _117destination_register = dec2bin_str(rd_index, 11, 7)

    _10alignment = "11"

    return bin2dec(_3127opcode + _2625control_bits + _2420source_register + _1915source_register + _1412function + _117destination_register + _62opcode + _10alignment)

def _3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(labels, params, _1412function, _62opcode):
    offset = params[1]
    if offset in labels:
        return 1/0 # TODO :)
    print(offset)
    _3120offset = dec2bin_str(hex2dec(offset), 31, 20)

    # print("ASTA MA INTERESEAZA: ", _3120offset)

    _1915source_register = dec2bin_str(abi_names[params[2]], 19, 15)
    _117destination_register = dec2bin_str(abi_names[params[0]], 11, 7)
    _10alignment = "11"

    # print(_3120offset[::-1] + _1915source_register + _1412function + _117destination_register + _62opcode + _10alignment)

    return bin2dec(_3120offset[::-1] + _1915source_register + _1412function + _117destination_register + _62opcode + _10alignment)

def _3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function, _62opcode):
    offset = params[1]
    if offset in labels:
        return 1/0 # TODO :)
    offset_in_bin = dec2bin_str(hex2dec(offset), 31, 20)
    offset_in_bin = offset_in_bin[::-1]
    _3125offset = offset_in_bin[5:]


    _2420source_register = dec2bin_str(abi_names[params[0]], 24, 20)
    _1915source_register = dec2bin_str(abi_names[params[2]], 19, 15)

    _117offset = offset_in_bin[:5]
    _10alignment = "11"

    return bin2dec(_3125offset + _2420source_register + _1915source_register + _1412function + _117offset + _62opcode + _10alignment)

def _jal(labels, params):
    offset = params[1]
    if offset in labels:
        offset_in_bin = dec2bin_str(labels.index(offset), 31, 12)
    else:
        offset_in_bin = dec2bin_str(hex2dec(offset), 31,  12)

    print("\n\nJAL______________________ offset:", offset,  labels.index(offset),  offset_in_bin)

    rd_index = abi_names[params[0]]
    rd = dec2bin_str(rd_index, 11, 7)
    
    # print(offset_in_bin[19]+ offset_in_bin[9:0-1:-1] + offset_in_bin[10] + offset_in_bin[18:11-1:-1] + rd + "11011" + "11")
    # print("OFFSET IN BIN: " + offset_in_bin)
    # print("OFFSET IN BIN19: " + offset_in_bin[19])
    # print("OFFSET IN BIN9:0: " + offset_in_bin[9::-1])
    # print("OFFSET IN BIN10: " + offset_in_bin[10])
    # print("OFFSET IN BIN18:11: " + offset_in_bin[18:10:-1])
    # print("\n\n")
    
    # print(offset_in_bin[19]+ offset_in_bin[9::-1] + offset_in_bin[10] + offset_in_bin[18:10:-1] + rd + "11011" + "11")
    # a = bin2dec(offset_in_bin[19]+ offset_in_bin[9::-1] + offset_in_bin[10] + offset_in_bin[18:10:-1] + rd + "11011" + "11")
    # print(a)

    print("len", len(offset_in_bin+ rd + "11011" + "11"))
    return bin2dec(offset_in_bin+ rd + "11011" + "11")


def _jalr(labels, params):
    offset = params[2]
    if offset in labels:
        offset_in_bin = dec2bin_str(labels.index(offset), 31, 20)
        offset_in_bin = offset_in_bin[::-1]
    else:
        offset_in_bin = dec2bin_str(hex2dec(offset), 31, 20)

    rs = dec2bin_str(abi_names[params[1]], 19, 15)
    rd = dec2bin_str(abi_names[params[0]], 11, 7)

    #print(bin2dec(offset_in_bin[::-1] + rs + "000" + rd + "11001" + "11"))

    return bin2dec(offset_in_bin[::-1] + rs + "000" + rd + "11001" + "11")

def b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function, _62opcode):
    offset = params[2]
    if offset in labels:
        offset_in_bin = dec2bin_str(labels.index(offset), 11, 0)

    else:
        offset_in_bin = dec2bin_str(hex2dec(offset), 11, 0)
    # print("\n BEQ params", params)
    # print("BEQ nr to jump to:", labels.index(offset))
    # print("BEQ OFFSET____________________________________________________________________________", offset_in_bin)



    rs2 = dec2bin_str(abi_names[params[1]], 24, 20)
    rs1 = dec2bin_str(abi_names[params[0]], 19, 15)
    _10alignment = "11"

    # print(bin2dec(offset_in_bin[11] + offset_in_bin[9: 4 -1: -1] + rs2 + rs1 + _1412function + offset_in_bin[3::-1] + offset_in_bin[10] + _62opcode + _10alignment ))
    return bin2dec(offset_in_bin[:7] + rs2 + rs1 + _1412function + offset_in_bin[7:12] + _62opcode + _10alignment )


def pop_push(params, function:str):
    rd = dec2bin_str(abi_names[params[0]], 11, 7)

    return bin2dec("01000000000000000" + function + rd +  "0110011")

def dot_word(params):
    val = params[0]
    return hex2dec(str(val))

functions = {
    "lui": lambda labels, params: _3112immediate_117destination_register_62opcode_10alignment(params, "01101"), # lui t2, 0x12345
    "auipc": lambda labels, params: _3112immediate_117destination_register_62opcode_10alignment(params, "00101"), # auipc x6, 0x12345

    "addi": lambda labels, params:_3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "000", "00100"), # addi rd, rs1, imm -> addi x3, x2, 0x10
    "slti": lambda labels, params:_3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "010", "00100"),#slti rd, rs1, imm -> slti x3, x2, 0x10; tested
    "sltiu": lambda labels, params:_3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "011", "00100"), #tested
    "xori": lambda labels, params:_3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "100", "00100"),
    "ori": lambda labels, params:_3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "110", "00100"),
    "andi": lambda labels, params:_3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "111", "00100"),

    "slli": lambda labels, params:_3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "001", "00100", "00000", "00"), # slli rd, rs1, shamt -> slli x2, x1, 0x2, tested
    "srli": lambda labels, params:_3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "101", "00100", "00000", "00"), #tested
    "srai": lambda labels, params:_3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "101", "00100", "01000", "00"), #tested

    "add":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "000", "01100", "00000", "00"),
    "sub":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, "000", "01100", "01000", "00"),
    "sll":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="001", _62opcode="01100"), #tested
    "slt":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="010", _62opcode="01100"), #tested
    "sltu":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="011", _62opcode="01100"), #tested
    "xor":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="100", _62opcode="01100"),
    "srl":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="101", _62opcode="01100"), #tested
    "sra":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="01000",_2625control_bits="00", _1412function="101", _62opcode="01100"), #tested
    "or":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="110", _62opcode="01100"),
    "and":  lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000",_2625control_bits="00", _1412function="111", _62opcode="01100"),
    "mul": lambda labels,params: _3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000", _2625control_bits="01", _1412function="000", _62opcode="01100"),
    "mulh": lambda labels,params: _3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000", _2625control_bits="01", _1412function="001", _62opcode="01100"),
    "mulhsu": lambda labels,params: _3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000", _2625control_bits="01", _1412function="010", _62opcode="01100"),
    "mulhu": lambda labels,params: _3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000", _2625control_bits="01", _1412function="011", _62opcode="01100"),
    "div": lambda labels,params: _3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000", _2625control_bits="01", _1412function="100", _62opcode="01100"),
    "divu": lambda labels,params: _3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000", _2625control_bits="01", _1412function="101", _62opcode="01100"),
    "rem": lambda labels,params: _3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000", _2625control_bits="01", _1412function="110", _62opcode="01100"),
    "remu": lambda labels,params: _3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(params, _3127opcode="00000", _2625control_bits="01", _1412function="111", _62opcode="01100"),

    "push": lambda labels, params:pop_push(params, "110"),
    "pop" : lambda labels, params:pop_push(params, "111"),

    "ecall": lambda labels, params: bin2dec("00000" + "00" + "00000" + "00000" + "000" + "00000" + "11100" + "11"),
    "ebreak": lambda labels, params: bin2dec("00000" + "00" + "00001" + "00000" + "000" + "00000" + "11100" + "11"),
    "uret": lambda labels, params: bin2dec("00000" + "00" + "00010" + "00000" + "000" + "00000" + "11100" + "11"),
    "sret": lambda labels, params: bin2dec("00010" + "00" + "00010" + "00000" + "000" + "00000" + "11100" + "11"),
    "mret": lambda labels, params: bin2dec("00110" + "00" + "00010" + "00000" + "000" + "00000" + "11100" + "11"),
    "wfi": lambda labels, params: bin2dec("00101" + "00" + "00010" + "00000" + "000" + "00000" + "11100" + "11"),
    "ret": lambda labels, params: bin2dec("10000" + "00" + "00010" + "00000" + "000" + "00000" + "11100" + "11"),

    "lb" : lambda labels, params: _3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(labels, params, _1412function="000", _62opcode="00000"),
    "lh" : lambda labels, params: _3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(labels, params, _1412function="001", _62opcode="00000"),
    "lw" : lambda labels, params: _3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(labels, params, _1412function="010", _62opcode="00000"),
    "lbu" : lambda labels, params: _3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(labels, params, _1412function="100", _62opcode="00000"),
    "lhu" : lambda labels, params: _3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(labels, params, _1412function="101", _62opcode="00000"),

    "sb": lambda labels, params: _3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="000", _62opcode="01000"), #tested
    "sh": lambda labels, params: _3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="001", _62opcode="01000"), #tested
    "sw": lambda labels, params: _3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="010", _62opcode="01000"), #tested

    "jal": lambda labels, params: _jal(labels, params),
    "jalr":lambda labels, params: _jalr(labels, params),

    "beq": lambda labels, params: b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="000", _62opcode="11000"),
    "bne": lambda labels, params: b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="001", _62opcode="11000"),
    "blt": lambda labels, params: b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="100", _62opcode="11000"),
    "bge": lambda labels, params: b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="101", _62opcode="11000"),
    "bltu": lambda labels, params: b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="110", _62opcode="11000"),
    "bgeu": lambda labels, params: b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(labels, params, _1412function="111", _62opcode="11000"),

    #TODO: fence
    "csrrw": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
    "csrrs": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
    "csrrc": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
    "csrrwi": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
    "csrrsi": lambda labels, params: (print("well .. nu-i :)"), 0)[1],
    "csrrci": lambda labels, params: (print("well .. nu-i :)"), 0)[1],

    "amoswap.w": lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignmentV2(params, _3127opcode="00001",_2625control_bits="00", _1412function="010", _62opcode="01011"),
    "amoadd.w": lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignmentV2(params, _3127opcode="00000",_2625control_bits="00", _1412function="010", _62opcode="01011"),
    "amoxor.w": lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignmentV2(params, _3127opcode="00100",_2625control_bits="00", _1412function="010", _62opcode="01011"),
    "amoand.w": lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignmentV2(params, _3127opcode="01100",_2625control_bits="00", _1412function="010", _62opcode="01011"),
    "amoor.w": lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignmentV2(params, _3127opcode="01000",_2625control_bits="00", _1412function="010", _62opcode="01011"),
    "amomin.w": lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignmentV2(params, _3127opcode="10000",_2625control_bits="00", _1412function="010", _62opcode="01011"),
    "amomax.w": lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignmentV2(params, _3127opcode="10100",_2625control_bits="00", _1412function="010", _62opcode="01011"),
    "amominu.w": lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignmentV2(params, _3127opcode="11000",_2625control_bits="00", _1412function="010", _62opcode="01011"),
    "amomaxu.w": lambda labels, params:_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignmentV2(params, _3127opcode="11100",_2625control_bits="00", _1412function="010", _62opcode="01011"),
}

def extract_label_and_operation(text):
    if ":" in text:
        parts = text.split(":", 1)
        label = parts[0].strip()
        code = parts[1].strip()
        return label, code
    return "", text.strip()

def assemble_code(code, memory, reg):
    labels = []
    parameters = []
    instructions = []
    line_index =[]

    for i,line in enumerate(code.splitlines()):
        removed_comment = line.split(";", 1)[0] if ";" in line else line
        if is_empty_string(removed_comment):
            labels.append("")
            instructions.append("")
            parameters.append("")
            line_index.append(i)
            continue

        label, operation = extract_label_and_operation(removed_comment)
        operation = operation.lstrip(" \t\n")
        words =   re.split(r'[ ,()]+', operation)
        words = [word for word in words if len(word) != 0]

        instruction =  words[0]
        params = words[1:]

        # print(i, "   ;",   line.split(";", 1)[1] if ";" in line else line)
        # continue

        labels.append(label)
        instructions.append(instruction)
        parameters.append(params)
        line_index.append(i)

    not_found_instr = []
    memory_address_to_add_instr_coded = 0
    initial_index_mapped_to_memory = dict()

    labels_constants_dot_data = dict()
    for i, instruction in enumerate(instructions):
        if instruction == ".word":
            labels_constants_dot_data[labels[i]] = parameters[i][0]

    # TODO refactor this and next loop to be made all in one
    operations_with_const_labels = []
    empty_memory_positions = []
    for i, instruction in enumerate(instructions):
        try:

            skip_this = False
            for param in parameters[i]:
                if param in list(labels_constants_dot_data.keys()):
                    operations_with_const_labels.append(i)
                    skip_this = True
                    break

            if skip_this:
                empty_memory_positions.append(memory_address_to_add_instr_coded)
                initial_index_mapped_to_memory[line_index[i]] = memory_address_to_add_instr_coded
                memory[(memory_address_to_add_instr_coded // 10, memory_address_to_add_instr_coded % 10)] = -1
                memory_address_to_add_instr_coded += 1
                continue


            reduced_to_number = functions[instruction](labels, parameters[i])
            memory[(memory_address_to_add_instr_coded // 10, memory_address_to_add_instr_coded % 10)] = reduced_to_number
            initial_index_mapped_to_memory[line_index[i]] = memory_address_to_add_instr_coded
            memory_address_to_add_instr_coded += 1

        except KeyError:
            not_found_instr.append(instruction)

    # TODO
    # add in memory instr that depend on .data
    for indexing, i in enumerate(operations_with_const_labels):
        mem_adr = empty_memory_positions[indexing]
        params = []
        for p in parameters[i]:
            if p in list(labels_constants_dot_data.keys()):
                params.append(labels_constants_dot_data[p])
            else:
                params.append(p)

        reduced_to_number = functions[instructions[i]](labels, params)
        memory[(mem_adr // 10, mem_adr % 10)] = reduced_to_number
        # print(labels[i], instructions[i], parameters[i])






    for i, instruction in enumerate(instructions):
        if instruction == ".word":
            reduced_to_number = dot_word(parameters[i])
            memory[(memory_address_to_add_instr_coded // 10, memory_address_to_add_instr_coded % 10)] = reduced_to_number
            initial_index_mapped_to_memory[line_index[i]] = memory_address_to_add_instr_coded
            memory_address_to_add_instr_coded += 1



    print("instructions not founded/erred:",not_found_instr)
    print("initial code relevant lines indexing:", initial_index_mapped_to_memory)
    print("init" , initial_index_mapped_to_memory)

    first_adr = list(initial_index_mapped_to_memory.keys())[0]
    reg['x3'] = first_adr
    reg['x2'] = 369
    return reg, memory, initial_index_mapped_to_memory



if __name__ == "__main__":
    mock_code = """.data           ; 0
vector:     .word 0x5               ;1
vector1:    .word 0x6			;2
vector2:    .word 0x7			;3
vector3:    .word 0x8             ;4   
.code           ; 5
_start:addi s0, s0, 0x28	   		;6
     addi t0, t0, vector             ; 7
    lw t0, 0x0(s0)				    ;8
    addi s1, s1, 0x4				;9
    addi s6, s6, 0x1                ; 10
;11
parse_vector: beq s1, zero, process_done   ; 12
    lw t4, 0x0(s0)                ; 13
    addi t4, t4, 0xA              ; 14
    ; Check if the element is odd or even	;15
    andi s2, t4, 0x1              ;16
    beq s2, zero, push_even      ; 17
    ori s2, s2, 0x1                    ; 18
    jal ra, push_to_stack              ; 19
push_even: andi s2, s2, 0x0                    ; Set t5 to 0 for even                 ; 20
push_to_stack: push s2                                                        ;21
    ; Move to the next element in the vector					;22
    lw t4, 0x0(s0)								;23
    sub t4, t4, s0								;24
    sw t4, 0x0(s0)            ; Move to the next element             ; 25
    addi s1, s1, 0xFFFFFFFF             ; Decrease the loop counter            ; 26
    jal ra, parse_vector              ; Loop back to parse_vector            ; 27
process_done:pop t1								;28
    pop t2									;29
    pop t3									;30
    addi t0, t0, 0xFFFFFF01    							;31
    sw   t0, 0x10(zero)  									;32
program_end: lb a7, 0x10(zero)              ; Exit code for ecall           ; 33
    ecall                       ; Exit program    				;34"""

    regu = {f"x{i}": 0 for i in range(32)}
    mem = {(line, column): 0 for line in range(37) for column in range(10)}
    regu, mem, initial_index_mapped_to_memory = assemble_code(mock_code, mem, regu)
    # pprint(dictionary)
