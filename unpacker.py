from core import instruction_set

reg = {f"R{i}": 0 for i in range(32)}
mem = {(line, column): 0 for line in range(37) for column in range(10)}

gp = "gp" 

abi_names = {'zero': 0, 'ra': 1, 'sp': 2, 'gp': 3, 'tp': 4, 't0': 5, 't1': 6, 't2': 7, 's0/fp': 8, 's1': 9, 'a0': 10, 'a1': 11, 'a2': 12, 'a3': 13, 'a4': 14, 'a5': 15, 'a6': 16, 'a7': 17, 's2': 18, 's3': 19, 's4': 20, 's5': 21, 's6': 22, 's7': 23, 's8': 24, 's9': 25, 's10': 26, 's11': 27, 't3': 28, 't4': 29, 't5': 30, 't6': 31}


def remove_trailing_zeros_and_revert(binary_value):
    binary_str = bin(binary_value)[2:]
    
    
    cleaned_binary = binary_str[::-1].lstrip('0')[::-1]
    reverted_binary = cleaned_binary[::-1]
    
    return int(reverted_binary, 2) if reverted_binary else 0


def get_register_name(reg_num):
    # Find the ABI name for a given register number
    for name, number in abi_names.items():
        if number == reg_num:
            return name
    return f"{reg_num}" 


##########################################
## 3758097335 => lui t2, x7 ##
## 1342178711 => auipc a1, 0xA ##
##########################################


def unpack__3112immediate_117destination_register_62opcode_10alignment(mem, address):
    instruction = 1342178711

    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _1915destination_register = (instruction >> 7) & 0b1111111
    _3125immediate_value = (instruction >> 12) & 0b111111111111111111111

    rd = [k for k, v in abi_names.items() if v == _1915destination_register][0]

    opcode_bin = f"{_62opcode:05b}{_10alignment:02b}"
    print(opcode_bin)
    instruction_name = None

    value = remove_trailing_zeros_and_revert(_3125immediate_value)
    
    if opcode_bin in instruction_set:
        instruction_name = instruction_set[opcode_bin]
    else:
        instruction_name = "Unknown function"

    if instruction_name is None:
        instruction_name = "Unknown opcode"

    decoded_instruction = {
        "immediate_value": value,
        "destination_register": rd,
        "opcode": f"{_62opcode:05b}",
        "alignment": f"{_10alignment:02b}",
        "decoded_function": instruction_name
    }

    print(decoded_instruction)
    
    return decoded_instruction

print("TEST LUI : \n\n")
unpack__3112immediate_117destination_register_62opcode_10alignment(mem, 0)
print("\n\n\n\n\n")


##########################################

### in teorie aici intra toata familia din
### fam de instr 0110011

# addi t2, t1, 0x5 => 2684552083 #
# addi t2, t1, 0x27(39) => 3825402771 #
# addi t2, t1, 0x335(821) => 2898461587 #


##########################################



def unpack__3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address):
    instruction = 3825402771

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


    opcode_bin = f"{_62opcode:05b}{_10alignment:02b}"
    instruction_name = None
    
    if opcode_bin in instruction_set:
        current_level = instruction_set[opcode_bin]
        
        if isinstance(current_level, dict):
            func3_bin = f"{_1412function:03b}"
            if func3_bin in current_level:
                next_level = current_level[func3_bin]
                
                if isinstance(next_level, dict):
                    imm_bin = f"{_3120immediate_value:012b}"
                    if imm_bin in next_level:
                        instruction_name = next_level[imm_bin]
                    else:
                        instruction_name = next_level
                else:
                    instruction_name = next_level
            else:
                instruction_name = "Unknown function"
        else:
            instruction_name = current_level
    else:
        instruction_name = "Unknown opcode"

    decoded_instruction = {
        "immediate_value": f"{value}",
        "source_register_1": rs1,
        "function": f"{_1412function:03b}",
        "destination_register": rd,
        "opcode": f"{_62opcode:05b}",
        "alignment": f"{_10alignment:02b}",
        "decoded_function": instruction_name
    }

    print(decoded_instruction)
    return decoded_instruction

print("addi:\n\n")
unpack__3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, 0)
print("\n\n")

##########################################

# 1413907 => slli t1,a1,0x1
# 19288979 => srli  t2,a2,0x12
# 1077337619 => srai  t3,a3,0x3

##########################################


def unpack__3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address):
    instruction = 1077337619
    

    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _117destination_register = (instruction >> 7) & 0b11111
    _1412function = (instruction >> 12) & 0b111
    _1915source_register = (instruction >> 15) & 0b11111
    _2420shamt = (instruction >> 20) & 0b11111
    _2625control_bits = (instruction >> 25) & 0b11
    _3127opcode = (instruction >> 27) & 0b11111

    opcode_bin = f"{_62opcode:05b}{_10alignment:02b}"
    
    instruction_name = None
    
    if opcode_bin in instruction_set:
        current_level = instruction_set[opcode_bin]
        
        if isinstance(current_level, dict):
            # try function bits
            func3_bin = f"{_1412function:03b}"
            if func3_bin in current_level:
                next_level = current_level[func3_bin]
                
                # nested case if I need to search deeper
                if isinstance(next_level, dict):
                    funct7_bin = f"{_3127opcode:05b}"
                    if funct7_bin in next_level:
                        instruction_name = next_level[funct7_bin]
                    else:
                        instruction_name = "Unknown function"
                else:
                    instruction_name = next_level
            else:
                instruction_name = "Unknown function"
        else:
            instruction_name = current_level
    else:
        instruction_name = "Unknown opcode"

    rs1 = get_register_name(_1915source_register)  
    rd = get_register_name(_117destination_register)  
    
    decoded_instruction = {
        "opcode_higher": f"{_3127opcode:05b}",
        "control_bits": f"{_2625control_bits:02b}",
        "shamt_value": f"{_2420shamt}",
        "source_register_1": f"{rs1}",
        "function": f"{_1412function:03b}",
        "destination_register": f"{rd}",  
        "opcode": f"{_62opcode:05b}",
        "alignment": f"{_10alignment:02b}",
        "decoded_function": f"{instruction_name}"
    }
    
    print(decoded_instruction)
    
    return decoded_instruction

unpack__3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, 0)



##########################################
# exemplu adresa sub 1081282099 #
##########################################


def unpack_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address):
    instruction = 1081282099

    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _117destination_register = (instruction >> 7) & 0b11111
    _1412function = (instruction >> 12) & 0b111
    _1915source_register = (instruction >> 15) & 0b11111
    _2420source_register = (instruction >> 20) & 0b11111
    _2625control_bits = (instruction >> 25) & 0b1111111
    _3127opcode = (instruction >> 27) & 0b111

    rs1 = [k for k, v in abi_names.items() if v == _2420source_register][0]
    rs2 = [k for k, v in abi_names.items() if v == _1915source_register][0]
    rd = [k for k, v in abi_names.items() if v == _117destination_register][0]

    opcode_bin = f"{_62opcode:05b}{_10alignment:02b}"
    print(opcode_bin)

    instruction_name = None

    if opcode_bin in instruction_set:
        current_level = instruction_set[opcode_bin]
        
        if isinstance(current_level, dict):
            func7_bin = f"{_2625control_bits:07b}"
            if func7_bin in current_level:
                next_level = current_level[func7_bin]
                
                if isinstance(next_level, dict):
                    funct3_bin = f"{_1412function:03b}"
                    if funct3_bin in next_level:
                        instruction_name = next_level[funct3_bin]
                    else:
                        instruction_name = "Unknown funct7"
                else:
                    instruction_name = next_level
            else:
                instruction_name = "Unknown function"
        else:
            instruction_name = current_level
    else:
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

unpack_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, 0)





##########################################

## BRANCH INSTRUCITONS ##

## beq t3, a0, end ##

## AICI MAI AM DE LUCRU ##

##########################################


def unpack__b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(mem, address):
    instruction = 279838819  

    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _117offset = (instruction >> 7) & 0b11111
    _1412function = (instruction >> 12) & 0b111
    _1915source_register = (instruction >> 15) & 0b11111
    _2420source_register = (instruction >> 20) & 0b11111
    _3125offset = (instruction >> 25) & 0b1111111

    rs1 = [k for k, v in abi_names.items() if v == _1915source_register][0]
    rs2 = [k for k, v in abi_names.items() if v == _2420source_register][0]

    opcode_bin = f"{_62opcode:05b}{_10alignment:02b}"
    print(opcode_bin)
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

    #calcul offset ##
    imm = ((_3125offset & 0b1111110) << 5) | (_117offset << 1)
    # deci if-ul asta il am ca sa verific daca e negativ si sa pot da ##
    # extend la semn ##
    if (_3125offset & 0b1000000): 
        imm |= -(1 << 12)

    decoded_instruction = {
        "offset": imm,
        "source_register_1": rs1,
        "source_register_2": rs2,
        "function": f"{_1412function:03b}",
        "opcode": f"{_62opcode:05b}",
        "alignment": f"{_10alignment:02b}",
        "decoded_function": instruction_name
    }

    print(decoded_instruction)
    
    return decoded_instruction

unpack__b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(mem, 0)