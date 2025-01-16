from pprint import pprint

from core import instruction_set
from Assembler import abi_names

gp = "gp"



def number_to_binary_string_32bit(number):
    """
    Converts a given integer or float to its 32-bit binary string representation.

    :param number: The number to convert (int or float).
    :return: 32-bit binary string representation of the number.
    """
    if isinstance(number, int):
        # Convert integer to 32-bit binary representation
        if number < 0:
            number = (1 << 32) + number  # Handle negative numbers with 2's complement
        binary_str = f'{number:032b}'  # Format as 32-bit binary
        return binary_str
    elif isinstance(number, float):
        # Convert float to binary using 32-bit IEEE 754 representation (single precision)
        import struct
        packed = struct.pack('!f', number)  # Pack float into 4 bytes (big-endian single precision)
        binary_str = ''.join(f'{byte:08b}' for byte in packed)  # Convert each byte to binary string
        return binary_str
    else:
        raise TypeError("Input must be an integer or a float.")


def binary_string_to_number(binary_str):
    """
    Converts a binary string to its integer or float representation.

    :param binary_str: A string representing a binary number (e.g., "0101010").
    :return: The corresponding integer or float number.
    """
    # Check if the input is valid
    if not isinstance(binary_str, str) or not set(binary_str).issubset({'0', '1'}):
        raise ValueError("Input must be a binary string containing only '0' and '1'.")

    # Convert binary string to integer
    return int(binary_str, 2)


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
## 3758097335 => lui t2, 0x7 ##
## 1342178711 => auipc a1, 0xA ##
##########################################


def unpack__3112immediate_117destination_register_62opcode_10alignment(mem, address, instructioni):
    instruction = mem[nr_to_tuple(address)]

    print("Unpacker.py: auipc, lui:", number_to_binary_string_32bit(instruction))

    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _1915destination_register = (instruction >> 7) & 0b1111111
    #_3125immediate_value = (instruction >> 12) & 0b111111111111111111111

    instruction = number_to_binary_string_32bit(instruction)
    
    _3125immediate_value = instruction[0:19]
    _3125immediate_value = _3125immediate_value[::-1]
    
    _3125immediate_value = binary_string_to_number(_3125immediate_value)


    rd = [k for k, v in abi_names.items() if v == _1915destination_register][0]

    opcode_bin = f"{_62opcode:05b}{_10alignment:02b}"
    print("unpacker:", opcode_bin)
    instruction_name = None


    value = _3125immediate_value

    if opcode_bin in instruction_set:
        instruction_name = instruction_set[opcode_bin]
    else:
        instruction_name = "Unknown function"

    if instruction_name is None:
        instruction_name = "Unknown opcode"

    decoded_instruction = {
        "immediate_value": int(value),
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

    cod_bin = number_to_binary_string_32bit(instruction)

    value = binary_string_to_number(cod_bin[:12])


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
                    cod_bin = number_to_binary_string_32bit(instruction)
                    imm_bin = cod_bin[0:5]
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
        "immediate_value": int(value),
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


# def unpack__3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address, instructioni):
#     instruction = mem[nr_to_tuple(address)]

#     _10alignment = instruction & 0b11
#     _62opcode = (instruction >> 2) & 0b11111
#     _117destination_register = (instruction >> 7) & 0b11111
#     _1412function = (instruction >> 12) & 0b111
#     _1915source_register = (instruction >> 15) & 0b11111
#     _2420shamt = (instruction >> 20) & 0b11111
#     _2625control_bits = (instruction >> 25) & 0b11
#     _3127opcode = (instruction >> 27) & 0b11111

#     opcode_bin = f"{_62opcode:05b}{_10alignment:02b}"

#     instruction_name = None

#     print("TESTSETSTESTSETSETSET,")
#     if opcode_bin in instruction_set:
#         current_level = instruction_set[opcode_bin]

#         if isinstance(current_level, dict):
#             # try function bits
#             func3_bin = f"{_1412function:03b}"
#             if func3_bin in current_level:
#                 next_level = current_level[func3_bin]
#                 # nested case if I need to search deeper
#                 if isinstance(next_level, dict):
#                     funct7_bin = f"{_3127opcode:05b}"
#                     if funct7_bin in next_level:
#                         instruction_name = next_level[funct7_bin]
#                     else:
#                         instruction_name = "Unknown function"
#                 else:
#                     instruction_name = next_level
#             else:
#                 instruction_name = "Unknown function"
#         else:
#             instruction_name = current_level
#     else:
#         instruction_name = "Unknown opcode"

#     rs1 = get_register_name(_1915source_register)
#     rd = get_register_name(_117destination_register)

#     decoded_instruction = {
#         "opcode_higher": f"{_3127opcode:05b}",
#         "control_bits": f"{_2625control_bits:02b}",
#         "immediate_value": int(_2420shamt),
#         "source_register_1": rs1,
#         "function": f"{_1412function:03b}",
#         "destination_register": rd,
#         "opcode": f"{_62opcode:05b}",
#         "alignment": f"{_10alignment:02b}",
#         "decoded_function": instruction_name
#     }

#     # print("unpacker:", decoded_instruction)

#     return decoded_instruction


# unpack__3127opcode_2625control_bits_2420shamt_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, 0)


##########################################
# exemplu adresa sub 1081282099 #
##########################################


def unpack_3127opcode_2625control_bits_2420source_register_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address, instructioni):
    instruction = mem[nr_to_tuple(address)]

    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    _117destination_register = (instruction >> 7) & 0b11111
    _1412function = (instruction >> 12) & 0b111
    _1915source_register = (instruction >> 15) & 0b11111
    _2420source_register = (instruction >> 20) & 0b11111
    _2625control_bits = (instruction >> 25) & 0b1111111
    _3127opcode = (instruction >> 27) & 0b111

    rs1 = [k for k, v in abi_names.items() if v == _1915source_register][0]
    rs2 = [k for k, v in abi_names.items() if v == _2420source_register][0]
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


def unpack__b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(mem, address, instructioni):
    instruction = mem[nr_to_tuple(address)]

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
    binstr = number_to_binary_string_32bit(instruction)
    first = binstr[:7]
    second = binstr[20:25]
    ans = first + second
    ans = binary_string_to_number(ans)
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", binstr)
    # print(first, second)

    imm = ans
    # print("ADRESA LA CARE VREAU SA SAR:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", ans)

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
    _3120offset = number_to_binary_string_32bit(instruction)

    _3120offset = _3120offset[0:12]
    _3120offset = _3120offset[::-1]

    _3120offset = binary_string_to_number(_3120offset)

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

    # print("UNPACKER PRIMU:", bin(imm_high))
    # print("UNPACKER AL DOILEA:", bin(imm_low))


    immediate = (imm_high << 5) | imm_low


    rs1_name = [k for k, v in abi_names.items() if v == rs1][0]
    rs2_name = [k for k, v in abi_names.items() if v == rs2][0]

    opcode_bin = f"{opcode:05b}{alignment:02b}"
    # print("unpacker:", opcode_bin)

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
    instruction = mem[nr_to_tuple(address)]

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
    instruction = mem[nr_to_tuple(address)]

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

    strbin =number_to_binary_string_32bit(instruction)
    #print(strbin)
    imm = binary_string_to_number(strbin[:20])

    #print("JAL jump adr:______________________________", imm)

    #print("unpacker:", f"{imm:b}")
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
    dict_entry = _62opcode << 2 | _10alignment
    dict_entry = f"{dict_entry:05b}"

    instruction = number_to_binary_string_32bit(instruction)


    first_search = instruction[7:12]
    second_search = instruction[0:5]

    decoded_function = None
    if dict_entry in instruction_set:
        current_level = instruction_set[dict_entry]  
        if isinstance(current_level, dict):
            current_level = current_level.get(funct3_bin, None)
            if isinstance(current_level, dict):
                current_level = current_level.get(first_search, None)
                if isinstance(current_level, dict):
                    decoded_function = current_level.get(second_search, "Unknown function")
                else:
                    decoded_function = current_level
            else:
                decoded_function = current_level
        else:
            decoded_function = current_level
    else:
        decoded_function = "Unknown function"

    decoded = {
        "opcode": dict_entry,
        "rd": rd,
        "rs1": rs1,
        "funct3": funct3_bin,
        "funct12": funct12_bin,
        "decoded_function": decoded_function,
    }

    return decoded


def decode_atomic_functions(mem, address, instructioni):
    instruction = mem[nr_to_tuple(address)]
    
    instruction = number_to_binary_string_32bit(instruction)
    
    _3127func = instruction[0:5]   
    _26aq = instruction[5]         
    _25rl = instruction[6]         
    _2420rs2 = instruction[7:12]   
    _1915rs1 = instruction[12:17] 
    _1412func3 = instruction[17:20] 
    _117rd = instruction[20:25]   
    _62opcode = instruction[25:30] 
    _10alignment = instruction[30:32]  
    
    print("_____________________+++++++++++++++++++____________________", _62opcode + _10alignment)

    dict_entry = f"{int(_62opcode + _10alignment, 2):05b}"
    
    rs1 = [k for k, v in abi_names.items() if v == int(_1915rs1, 2)][0]
    rs2 = [k for k, v in abi_names.items() if v == int(_2420rs2, 2)][0]
    rd = [k for k, v in abi_names.items() if v == int(_117rd, 2)][0]
    
    if dict_entry in instruction_set:
        current_level = instruction_set[dict_entry]
        
        if isinstance(current_level, dict):
            print("WWWWWWWWWWWWWWWWWWWWWWWWWWW", current_level)
            current_level = current_level.get(_1412func3, "Unknown function")
            print("WWWWWWWWWWWWWWWWWWWWWWWWWWW", current_level)
            if isinstance(current_level, dict):
                current_level = current_level.get(_3127func, "Unknown function")
                
                if isinstance(current_level, dict):
                    current_level = current_level.get(_2420rs2, "Unknown function")
        
        decoded_function = current_level
    else:
        decoded_function = "Unknown function"

    decoded = {
        "opcode": dict_entry,
        "rd": rd,
        "rs1": rs1,
        "rs2": rs2,
        "func3": _1412func3,
        "func": _3127func,
        "aq": _26aq,
        "rl": _25rl,
        "alignment": _10alignment,
        "decoded_function": decoded_function,
    }

    print("DWQOPDMQPOWDMOPWQMDPWOQMDPOWMQOPDMWQPODMQWPO:", decoded["decoded_function"])

    return decoded



##########################################

#### DECODING FUNCTION ###

##########################################


def decode_and_execute_instruction(mem, reg, initial_index_mapped_to_memory):
    address = initial_index_mapped_to_memory[reg["x3"]]
    print("UNPACKER.PY:", initial_index_mapped_to_memory[reg["x3"]], reg["x3"])
    instruction = mem[nr_to_tuple(address)]

    # Extract opcode and alignment
    _10alignment = instruction & 0b11
    _62opcode = (instruction >> 2) & 0b11111
    opcode_bin = f"{_62opcode:05b}{_10alignment:02b}"
    print("AAAAAAAAAAAAAAAAAA", opcode_bin)
    # print("RELEVANT:__________________:", instruction)

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
        decoded = unpack__3120offset_1915source_register_1412function_117destination_register_62opcode_10alignment(mem, address,None)

    elif opcode_bin == "1100011":  # Branch instructions
        decoded = unpack__b_3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(mem, address, None)

    elif opcode_bin == "1100111":  # JALR
        decoded = unpack_jalr(mem, address, None)
        
    elif opcode_bin == "1101111":  # JAL
        decoded = unpack_jal(mem, address, None)
        
    elif opcode_bin == "1110011":  # System instructions
        decoded = unpack_system(mem, address, None)
        
    elif opcode_bin == "0100011":
        decoded = unpack__3125offset_2420source_register_1915source_register_1412function_117offset_62opcode_10alignment(mem, address, None)

    elif opcode_bin == "0101111":
        decoded = decode_atomic_functions(mem, address, None)
    # Ensure `decoded_function` is valid
    if decoded and "decoded_function" in decoded:
        execution_function = decoded["decoded_function"]          
        if callable(execution_function) or opcode_bin == "0010011":
            # Build arguments dynamically based on the instruction type
            if opcode_bin in {"0110111", "0010111"}:  # LUI, AUIPC
                execution_args = [
                    f"x{abi_names[decoded['destination_register']]}",
                    decoded["immediate_value"],
                ]

            elif opcode_bin == "0010011":
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
                mem, reg = execution_function(*execution_args, mem, reg, initial_index_mapped_to_memory)
                # print("FIX DUPA_______________", reg['x3'])

            except Exception as e:
                print("unpacker:", f"Error during execution: {e}")
        else:
            print("unpacker:", f"Invalid or unknown decoded function for instruction at address {address}")
    else:
        print("unpacker:", f"Unknown or unimplemented instruction at address {address}")

    return mem, reg



