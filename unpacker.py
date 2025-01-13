from core import instruction_set
from core import reg

#reg = {f"R{i}": 0 for i in range(32)}
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


def unpack__3112immediate_117destination_register_62opcode_10alignment(mem, address, instructioni):
    instruction = mem[address]

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

    #print(decoded_instruction)
    
    return decoded_instruction

#print("TEST LUI : \n\n")
#unpack__3112immediate_117destination_register_62opcode_10alignment(mem, 0)
#print("\n\n\n\n\n")


##########################################

### in teorie aici intra toata familia din
### fam de instr 0110011

# addi t2, t1, 0x5 => 2684552083 #
# addi t2, t1, 0x27(39) => 3825402771 #
# addi t2, t1, 0x335(821) => 2898461587 #


##########################################



def unpack__3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address, instructioni):
    instruction = mem[address]

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

    #print(decoded_instruction)
    return decoded_instruction

#print("addi:\n\n")
#unpack__3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, 0)
#print("\n\n")

##########################################

# 1413907 => slli t1,a1,0x1
# 19288979 => srli  t2,a2,0x12
# 1077337619 => srai  t3,a3,0x3

##########################################


def unpack__3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address, instructioni):
    instruction = mem[address]
    

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
    
    #print(decoded_instruction)
    
    return decoded_instruction

#unpack__3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, 0)



##########################################
# exemplu adresa sub 1081282099 #
##########################################


def unpack_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address, instructioni):
    instruction = mem[address]

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

    #print(decoded_instruction)

#unpack_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, 0)


##########################################

## BRANCH INSTRUCITONS ##

## beq t3, a0, end ##

## AICI MAI AM DE LUCRU ##

##########################################


def unpack__b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(mem, address, instructioni):
    instruction = mem[address] 

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

    #print(decoded_instruction)
    
    return decoded_instruction

#unpack__b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(mem, 0)




##########################################

## lbu t1, 0x2(t2) => 1073988355

##########################################



def unpack__3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address, instructioni):
    instruction = mem[address] 

    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _117destination_register = (instruction >> 7) & 0b11111
    _1412function = (instruction >> 12) & 0b111
    _1915source_register = (instruction >> 15) & 0b11111
    _3120offset = (instruction >> 20) & 0b111111111111

    rs = [k for k, v in abi_names.items() if v == _1915source_register][0]
    rd = [k for k, v in abi_names.items() if v == _117destination_register][0]

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

    imm = _3120offset
    if (_3120offset & 0b100000000000):
        imm |= -(1 << 12) 


    decoded_instruction = {
        "offset": imm,
        "source_register": rs,
        "destination_register": rd,
        "function": f"{_1412function:03b}",
        "opcode": f"{_62opcode:05b}",
        "alignment": f"{_10alignment:02b}",
        "decoded_function": instruction_name
    }

    #print(decoded_instruction)
    
    return decoded_instruction

#unpack__3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, 0)




def unpack_jalr(mem, address, instructioni):
    instruction = mem[address]
    
    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _117rd = (instruction >> 7) & 0b11111
    _1412function = (instruction >> 12) & 0b111
    _1915rs1 = (instruction >> 15) & 0b11111
    _3120imm = (instruction >> 20) & 0b111111111111


    rs1 = [k for k, v in abi_names.items() if v == _1915rs1][0]
    rd = [k for k, v in abi_names.items() if v == _117rd][0]

    imm = _3120imm
    if (_3120imm & 0b100000000000):
        imm |= -(1 << 12)

    return {
        "opcode": "1100111",
        "rd": rd,
        "rs1": rs1,
        "immediate": imm,
        "decoded_function": "jalr"
    }


def unpack_jal(mem, address, instructioni):
    instruction = mem[address]
    
    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _117rd = (instruction >> 7) & 0b11111
    _1912imm_19_12 = (instruction >> 12) & 0b11111111
    _20imm_11 = (instruction >> 20) & 0b1
    _3021imm_10_1 = (instruction >> 21) & 0b1111111111
    _31imm_20 = (instruction >> 31) & 0b1

    rd = [k for k, v in abi_names.items() if v == _117rd][0]

    imm = (_31imm_20 << 20) | (_1912imm_19_12 << 12) | (_20imm_11 << 11) | (_3021imm_10_1 << 1)
    if (_31imm_20):
        imm |= -(1 << 21)

    return {
        "opcode": "1101111",
        "rd": rd,
        "immediate": imm,
        "decoded_function": "jal"
    }



def unpack_system(mem, address, instructioni):
    instruction = mem[address]
    
    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _117rd = (instruction >> 7) & 0b11111
    _1412funct3 = (instruction >> 12) & 0b111
    _1915rs1 = (instruction >> 15) & 0b11111
    _3120funct12 = (instruction >> 20) & 0b111111111111

    rs1 = [k for k, v in abi_names.items() if v == _1915rs1][0]
    rd = [k for k, v in abi_names.items() if v == _117rd][0]

    funct3_bin = f"{_1412funct3:03b}"
    funct12_bin = f"{_3120funct12:012b}"

    if funct3_bin == "000":
        if funct12_bin == "000000000000":
            decoded_function = "ecall"
        elif funct12_bin == "000000000001":
            decoded_function = "ebreak"
        elif funct12_bin == "000000000010":
            if _1915rs1 == 0: #verific daca sunt diferite aici
                decoded_function = "uret"
            elif _1915rs1 == 2:
                decoded_function = "sret"
            elif _1915rs1 == 6:
                decoded_function = "mret"
            elif _1915rs1 == 5:
                decoded_function = "wfi"
            elif _1915rs1 == 16:
                decoded_function = "ret"
            else:
                decoded_function = "unknown_system"
        else:
            decoded_function = "unknown_system"
    else:
        decoded_function = "unknown_system"

    return {
        "opcode": "1110011",
        "rd": rd,
        "rs1": rs1,
        "funct3": funct3_bin,
        "funct12": funct12_bin,
        "decoded_function": decoded_function
    }
    
    
    
##########################################

       #### DECODING FUNCTION ###

##########################################
    
   
def decode_and_execute_instruction(mem, reg, address):
    instruction = mem[address]

    # Extract opcode and alignment
    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    opcode_bin = f"{_62opcode:05b}{_10alignment:02b}"

    print(f"Decoding instruction at address {address}: opcode {opcode_bin}")

    decoded = None
    execution_args = []

    # Decode the instruction and extract `decoded_function`
    if opcode_bin in {"0110111", "0010111"}:  # LUI, AUIPC
        decoded = unpack__3112immediate_117destination_register_62opcode_10alignment(mem, address, None)

    elif opcode_bin == "0010011":  # I-type instructions
        decoded = unpack__3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address, None)

    elif opcode_bin == "0110011":  # R-type instructions
        decoded = unpack_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address, None)

    elif opcode_bin == "0000011":  # Load instructions
        decoded = unpack__3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address, None)

    elif opcode_bin == "1100011":  # Branch instructions
        decoded = unpack__b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(mem, address, None)

    elif opcode_bin == "1100111":  # JALR
        decoded = unpack_jalr(mem, address, None)

    elif opcode_bin == "1101111":  # JAL
        decoded = unpack_jal(mem, address, None)

    elif opcode_bin == "1110011":  # System instructions
        decoded = unpack_system(mem, address, None)

    # Ensure `decoded_function` is valid
    if decoded and "decoded_function" in decoded:
        execution_function = decoded["decoded_function"]

        if callable(execution_function):
            # Build arguments dynamically based on the instruction type
            if opcode_bin in {"0110111", "0010111"}:  # LUI, AUIPC
                execution_args = [
                    f"R{abi_names[decoded['destination_register']]}",
                    decoded["immediate_value"],
                ]

            elif opcode_bin == "0010011":  # I-type
                execution_args = [
                    f"R{abi_names[decoded['destination_register']]}",
                    f"R{abi_names[decoded['source_register_1']]}",
                    decoded["immediate_value"],
                ]

            elif opcode_bin == "0110011":  # R-type
                execution_args = [
                    f"R{abi_names[decoded['destination_register']]}",
                    f"R{abi_names[decoded['source_register_1']]}",
                    f"R{abi_names[decoded['source_register_2']]}",
                ]

            elif opcode_bin == "0000011":  # Load
                execution_args = [
                    f"R{abi_names[decoded['destination_register']]}",
                    decoded["offset"],
                    f"R{abi_names[decoded['source_register']]}",
                ]

            elif opcode_bin == "1100011":  # Branch
                execution_args = [
                    f"R{abi_names[decoded['source_register_1']]}",
                    f"R{abi_names[decoded['source_register_2']]}",
                    decoded["offset"],
                ]

            elif opcode_bin in {"1100111", "1101111"}:  # JALR, JAL
                execution_args = [
                    f"R{abi_names[decoded['rd']]}",
                    decoded["immediate"],
                ]

            # Execute the function
            print(f"Decoded instruction: {decoded}")
            print(f"Execution function: {execution_function}")
            print(f"Execution arguments: {execution_args}")
            try:
                execution_function(*execution_args)
            except Exception as e:
                print(f"Error during execution: {e}")
                return address + 1
            return address + 1
        else:
            print(f"Invalid or unknown decoded function for instruction at address {address}")
    else:
        print(f"Unknown or unimplemented instruction at address {address}")

    return address + 1
    
    
reg['gp'] = 0  # Initialize gp (x3) to 0

# Test data
test_instructions = [
    2147681171,
    2147716627,
    2148402451    
]

test_instructions2 = [
    172803,    
    172931,   
    7540275,   
    29532195,  
    3758097335, 
    1342178711, 
    1413907,    
    2511763,    
    1077337619, 
    279838819,  
    918895,     
    3758098579, 
    115         
]

# Load instructions into memory sequentially
for i, instr in enumerate(test_instructions):
    mem[i] = instr

print("\nStarting execution...\n")

# Execute instructions sequentially
for i in range(len(test_instructions)):
    print(f"\nExecuting instruction at address {i}")
    print(f"Current gp value: {reg['gp']}")
    next_address = decode_and_execute_instruction(mem, reg, i)
    print(f"Instruction executed, gp is now: {reg['gp']}")

# Print final state
print("\nFinal Register State:")
print("-" * 40)
for i in range(32):
    reg_name = [k for k, v in abi_names.items() if v == i][0]
    print(f"{reg_name} (x{i}): {reg[f'R{i}']}")
    if i == 3:  # Special highlight for gp
        print(f">>> gp final value: {reg['gp']} <<<")

print("\nNon-zero Memory Locations:")
print("-" * 40)
for addr in range(len(test_instructions)):
    print(f"Address {addr}: {mem[addr]} (0x{mem[addr]:08x})")