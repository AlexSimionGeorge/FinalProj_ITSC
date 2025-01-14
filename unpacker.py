from pprint import pprint

from core import instruction_set
from Assembler import abi_names

gp = "gp"


def nr_to_tuple(nr):
    return nr // 10, nr % 10


def remove_trailing_zeros_and_revert(binary_value):
    binary_str = bin(binary_value)[2:]

    cleaned_binary = binary_str[::-1].lstrip('0')[::-1]
    reverted_binary = cleaned_binary[::-1]

    return int(reverted_binary, 2) if reverted_binary else 0


def revert(number):
    # Convert the number to binary without the "0b" prefix
    binary_representation = bin(number)[2:]
    # Reverse the binary string
    reversed_binary = binary_representation[::-1]
    # Convert the reversed binary back to decimal
    reversed_decimal = int(reversed_binary, 2)
    return reversed_decimal


def get_register_name(reg_num):
    # Find the ABI name for a given register number
    for name, number in abi_names.items():
        if number == reg_num:
            return name
    return f"{reg_num}"


def print_bin(binary_input):
    # Remove '0b' if it's present and ensure it's a valid binary string
    binary_input = binary_input.strip()
    if binary_input.startswith("0b"):
        binary_input = binary_input[2:]

    # Display bit number and value
    bit_indices = "Bit: " + " ".join(f"{i:02}" for i in range(len(binary_input)))  # Align bit numbers
    bit_values = "Val: " + "   ".join(binary_input)  # Align bit values with spacing

    # Print the aligned output
    print("unpacker:", bit_indices)
    print("unpacker:", bit_values)


##########################################
## 3758097335 => lui t2, x7 ##
## 1342178711 => auipc a1, 0xA ##
##########################################


def unpack__3112immediate_117destination_register_62opcode_10alignment(mem, address, instructioni):
    instruction = mem[nr_to_tuple(address)]

    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _1915destination_register = (instruction >> 7) & 0b1111111
    _3125immediate_value = (instruction >> 12) & 0b111111111111111111111

    rd = [k for k, v in abi_names.items() if v == _1915destination_register][0]

    opcode_bin = f"{_62opcode:05b}{_10alignment:02b}"
    print("unpacker:", opcode_bin)
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

    # print("unpacker:", decoded_instruction)

    return decoded_instruction


# print("unpacker:", "TEST LUI : \n\n")
# unpack__3112immediate_117destination_register_62opcode_10alignment(mem, 0)
# print("unpacker:", "\n\n\n\n\n")


##########################################

### in teorie aici intra toata familia din
### fam de instr 0110011

# addi t2, t1, 0x5 => 2684552083 #
# addi t2, t1, 0x27(39) => 3825402771 #
# addi t2, t1, 0x335(821) => 2898461587 #


##########################################


def unpack__3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address,
                                                                                                        instructioni):
    instruction = mem[nr_to_tuple(address)]

    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _117destination_register = (instruction >> 7) & 0b11111
    _1412function = (instruction >> 12) & 0b111
    _1915source_register = (instruction >> 15) & 0b11111
    _3120immediate_value = (instruction >> 20) & 0b111111111111

    value = remove_trailing_zeros_and_revert(_3120immediate_value)
    print("unpacker:", _3120immediate_value)

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

    # print("unpacker:", decoded_instruction)
    return decoded_instruction


# print("unpacker:", "addi:\n\n")
# unpack__3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, 0)
# print("unpacker:", "\n\n")

##########################################

# 1413907 => slli t1,a1,0x1
# 19288979 => srli  t2,a2,0x12
# 1077337619 => srai  t3,a3,0x3

##########################################


def unpack__3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(
        mem, address, instructioni):
    instruction = mem[nr_to_tuple(address)]

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

    # print("unpacker:", decoded_instruction)

    return decoded_instruction


# unpack__3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, 0)


##########################################
# exemplu adresa sub 1081282099 #
##########################################


def unpack_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(
        mem, address, instructioni):
    instruction = mem[nr_to_tuple(address)]

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
    print("unpacker:", opcode_bin)

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

    return decoded_instruction


# unpack_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, 0)


##########################################

## BRANCH INSTRUCITONS ##

## beq t3, a0, end ##

## AICI MAI AM DE LUCRU ##

##########################################


def unpack__b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(mem,
                                                                                                             address,
                                                                                                             instructioni):
    instruction = 11406179

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
    print("unpacker:", opcode_bin)
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

    # calcul offset ##
    offset11 = _3125offset >> 6
    offset94 = _3125offset & 0b0111111
    offset30 = _117offset >> 1
    offset10 = _117offset & 0b1
    imm = (offset11 << 10) | (offset94 << 3) | (offset30) | (offset10 << 9)

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

    print("unpacker:", decoded_instruction)

    return decoded_instruction


##########################################

## lbu t1, 0x2(t2) => 1073988355

##########################################


def unpack__3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address,
                                                                                                     instructioni):
    instruction = mem[nr_to_tuple(address)]

    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _117destination_register = (instruction >> 7) & 0b11111
    _1412function = (instruction >> 12) & 0b111
    _1915source_register = (instruction >> 15) & 0b11111
    _3120offset = (instruction >> 20) & 0b111111111111

    rs = [k for k, v in abi_names.items() if v == _1915source_register][0]
    rd = [k for k, v in abi_names.items() if v == _117destination_register][0]

    opcode_bin = f"{_62opcode:05b}{_10alignment:02b}"
    print("unpacker:", opcode_bin)
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

    # print("unpacker:", decoded_instruction)

    return decoded_instruction


def unpack__3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(mem, address, instructioni):
    instruction = mem[nr_to_tuple(address)]

    alignment = instruction & 0b11
    opcode = (instruction >> 2) & 0b11111
    imm_low = (instruction >> 7) & 0b11111
    imm_low = revert(imm_low)
    function = (instruction >> 12) & 0b111
    rs1 = (instruction >> 15) & 0b11111
    rs2 = (instruction >> 20) & 0b11111
    imm_high = (instruction >> 25) & 0b1111111
    imm_high = revert(imm_high)
    
    print("UNPACKER PRIMU:", bin(imm_high))
    print("UNPACKER AL DOILEA:", bin(imm_low))
    
    
    immediate = (imm_high << 5) | imm_low
    

    rs1_name = [k for k, v in abi_names.items() if v == rs1][0]
    rs2_name = [k for k, v in abi_names.items() if v == rs2][0]

    opcode_bin = f"{opcode:05b}{alignment:02b}"
    print("unpacker:", opcode_bin)

    if opcode_bin == "0100011":
        function_bin = f"{function:03b}"
        instruction_name = instruction_set[opcode_bin][function_bin]
    else:
        instruction_name = "Not a store instruction"

    decoded_instruction = {
        "immediate_value": immediate,
        "base_register": rs1_name,
        "source_register": rs2_name,
        "opcode": f"{opcode:05b}",
        "alignment": f"{alignment:02b}",
        "function": f"{function:03b}",
        "decoded_function": instruction_name
    }

    return decoded_instruction


def unpack_jalr(mem, address, instructioni):
    instruction = 9765607

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

    decoded_function = {
        "opcode": "1100111",
        "rd": rd,
        "rs1": rs1,
        "immediate": imm,
        "decoded_function": instruction_set["1100111"]
    }

    print("unpacker:", decoded_function)

    return decoded_function


# unpack_jalr(mem, 0, None)


## test 2147616111 ##
def unpack_jal(mem, address, instruction):
    print("unpacker:", bin(instruction))

    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _117rd = (instruction >> 7) & 0b11111
    _1912imm_19_12 = (instruction >> 12) & 0b11111111
    _1912imm_19_12 = revert(_1912imm_19_12)
    _20imm_11 = (instruction >> 20) & 0b1
    _3021imm_10_1 = (instruction >> 21) & 0b1111111111
    _3021imm_10_1 = revert(_3021imm_10_1)
    _31imm_20 = (instruction >> 31) & 0b1

    rd = [k for k, v in abi_names.items() if v == _117rd][0]

    imm = (_31imm_20 << 19) | (_1912imm_19_12 << 11) | (_20imm_11 << 10) | (_3021imm_10_1)
    print("unpacker:", f"{imm:b}")
    # if (_31imm_20):
    #      imm |= -(1 << 21)

    decoded_function = {
        "opcode": "1101111",
        "rd": rd,
        "immediate": imm,
        "decoded_function": instruction_set["1101111"]
    }

    print("unpacker:", decoded_function)

    return decoded_function


# unpack_jal(mem, 0, None)


def unpack_system(mem, address, instructioni):
    instruction = mem[nr_to_tuple(address)]

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
            if _1915rs1 == 0:  # verific daca sunt diferite aici
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


def decode_and_execute_instruction(mem, reg, initial_index_mapped_to_memory):
    address = initial_index_mapped_to_memory[reg["x3"]]

    instruction = mem[nr_to_tuple(address)]

    # Extract opcode and alignment
    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    opcode_bin = f"{_62opcode:05b}{_10alignment:02b}"

    print("RELEVANT:__________________:", instruction)

    decoded = None
    execution_args = []

    # Decode the instruction and extract `decoded_function`
    if opcode_bin in {"0110111", "0010111"}:  # LUI, AUIPC
        decoded = unpack__3112immediate_117destination_register_62opcode_10alignment(mem, address, None)

    elif opcode_bin == "0010011":  # I-type instructions
        decoded = unpack__3120immediate_1915source_register_1412function_117destination_register_62opcode_10alignment(
            mem, address, None)

    elif opcode_bin == "0110011":  # R-type instructions
        decoded = unpack_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(
            mem, address, None)

    elif opcode_bin == "0000011":  # Load instructions
        decoded = unpack__3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(mem,
                                                                                                                   address,
                                                                                                                   None)

    elif opcode_bin == "1100011":  # Branch instructions
        decoded = unpack__b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(
            mem, address, None)

    elif opcode_bin == "1100111":  # JALR
        decoded = unpack_jalr(mem, address, None)

    elif opcode_bin == "1101111":  # JAL
        decoded = unpack_jal(mem, address, None)

    elif opcode_bin == "1110011":  # System instructions
        decoded = unpack_system(mem, address, None)
    elif opcode_bin == "0100011":
        decoded = unpack__3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(mem, address, None)

    # Ensure `decoded_function` is valid
    if decoded and "decoded_function" in decoded:
        execution_function = decoded["decoded_function"]

        if callable(execution_function):
            # Build arguments dynamically based on the instruction type
            if opcode_bin in {"0110111", "0010111"}:  # LUI, AUIPC
                execution_args = [
                    f"x{abi_names[decoded['destination_register']]}",
                    decoded["immediate_value"],
                ]

            elif opcode_bin == "0010011":  # I-type
                execution_args = [
                    f"x{abi_names[decoded['destination_register']]}",
                    f"x{abi_names[decoded['source_register_1']]}",
                    decoded["immediate_value"],
                ]

            elif opcode_bin == "0110011":  # R-type
                execution_args = [
                    f"x{abi_names[decoded['destination_register']]}",
                    f"x{abi_names[decoded['source_register_1']]}",
                    f"x{abi_names[decoded['source_register_2']]}",
                ]

            elif opcode_bin == "0000011":  # Load
                execution_args = [
                    f"x{abi_names[decoded['destination_register']]}",
                    decoded["offset"],
                    f"x{abi_names[decoded['source_register']]}",
                ]
            elif opcode_bin == "0100011":  # store
                pprint(decoded)

                execution_args = [
                    f"x{abi_names[decoded['source_register']]}",
                    decoded["immediate_value"],
                    f"x{abi_names[decoded['base_register']]}",
                ]

            elif opcode_bin == "1100011":  # Branch
                execution_args = [
                    f"x{abi_names[decoded['source_register_1']]}",
                    f"x{abi_names[decoded['source_register_2']]}",
                    decoded["offset"],
                ]

            elif opcode_bin == "1100111":  # JALR
                execution_args = [
                    f"x{abi_names[decoded['rd']]}",
                    f"x{abi_names[decoded['rs1']]}",
                    decoded["immediate"],
                ]
                
            elif opcode_bin == "1101111":  # JAL
                execution_args = [
                    f"x{abi_names[decoded['rd']]}",
                    decoded["immediate"],
                ]

            # Execute the function
            print("unpacker:", f"Decoded instruction: {decoded}")
            print("unpacker:", f"Execution function: {execution_function}")
            print("unpacker:", f"Execution arguments: {execution_args}")
            try:
                execution_function(*execution_args, mem, reg, initial_index_mapped_to_memory)
            except Exception as e:
                print("unpacker:", f"Error during execution: {e}")
                return mem, reg
            return mem, reg
        else:
            print("unpacker:", f"Invalid or unknown decoded function for instruction at address {address}")
    else:
        print("unpacker:", f"Unknown or unimplemented instruction at address {address}")

    return mem, reg


if __name__ == "__main__":
    reg['R3'] = 0  # Initialize gp (x3) to 0

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
        11406179,
        18875759,
        2684356755,
        115,
    ]

    # Load instructions into memory sequentially
    for i, instr in enumerate(test_instructions):
        mem[i] = instr

    print("unpacker:", "\nStarting execution...\n")

    # Execute instructions sequentially
    for i in range(len(test_instructions)):
        print("unpacker:", f"\nExecuting instruction at address {i}")
        print("unpacker:", f"Current pc value: {reg['R3']}")
        next_address = decode_and_execute_instruction(mem, reg)
        print("unpacker:", f"Instruction executed, pc is now: {reg['R3']}")

    # Print final state
    print("unpacker:", "\nFinal Register State:")
    print("unpacker:", "-" * 40)
    for i in range(32):
        reg_name = [k for k, v in abi_names.items() if v == i][0]
        print("unpacker:", f"{reg_name} (x{i}): {reg[f'R{i}']}")
        if i == 3:  # Special highlight for gp
            print("unpacker:", f">>> pc final value: {reg['R3']} <<<")

    print("unpacker:", "\nNon-zero Memory Locations:")
    print("unpacker:", "-" * 40)
    for addr in range(len(test_instructions)):
        print("unpacker:", f"Address {addr}: {mem[addr]} (0x{mem[addr]:08x})")
