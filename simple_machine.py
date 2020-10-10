import sys
​
#                  AABCDDDD
PRINT_TIM = 0b00000001
HALT = 0b00000010
PRINT_NUM = 0b01000011
SAVE = 0b10000100  # LDI
PRINT_REGISTER = 0b01000101
ADD = 0b10100110
PUSH = 0b01000111
POP = 0b01001000
CALL = 0b01011001
RET = 0b00011010
​
# is_alu_op = (command >> 5) & 0b001 == 1
​
memory = [0] * 256
​
# memory = [
#     SAVE
#     0
#     8 # idx of subroutine
#     PRINT_NUM,
#     99,
#     CALL,  <-- PC
#     0,
#     HALT,
#     PRINT_TIM,      # address aka idx of subroutine
#     PRINT_TIM,
#     RET
# ]
​


def load_memory():
    if (len(sys.argv)) != 2:
        print("remember to pass the second file name")
        print("usage: python3 fileio.py <second_file_name.py>")
        sys.exit()


​
  address = 0
   try:
        with open(sys.argv[1]) as f:
            for line in f:
                # parse the file to isolate the binary opcodes
                possible_number = line[:line.find('#')]
                if possible_number == '':
                    continue  # skip to next iteration of loop
    ​
    instruction = int(possible_number, 2)
    ​
    memory[address] = instruction
    ​
    address += 1
    ​
    except FileNotFoundError:
        print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
        sys.exit()
​
load_memory()
​
# cabinets in your shop: registers
# storage unit: cache
# warehouse outside town: RAM
​
​
# registers
# physically located on CPU, treat as variables
​
# n.b.: SP and PC are both always storing memory addresses!!!!
​
# R0-R7
registers = [0] * 8
registers[7] = 0xF4
​
# cpu should now step through memory and take actions based on commands it finds
​
# a data-driven machine
​
# program counter, a pointer
pc = 0
running = True
​
​
while running:
    command = memory[pc]
​
num_args = command >> 6
​
if command == PRINT_TIM:
    print("tim!")
​
elif command == PRINT_NUM:
    number = memory[pc + 1]
    print(number)
​
elif command == SAVE:
    # get out the arguments
    # pc+1 is reg idx, pc+2 value
    reg_idx = memory[pc + 1]
    value = memory[pc + 2]
​
# put the value into the correct register
registers[reg_idx] = value
​
elif command == PRINT_REGISTER:
    # get out the argument
    reg_idx = memory[pc + 1]
​
# the argument is a pointer to a register
value = registers[reg_idx]
print(value)
​
elif command == ADD:
    # pull out the arguments
    reg_idx_1 = memory[pc + 1]
    reg_idx_2 = memory[pc + 2]
​
# add regs together
registers[reg_idx_1] = registers[reg_idx_1] + registers[reg_idx_2]
​
elif command == HALT:
    running = False
​
elif command == PUSH:
    # 1. Decrement the `SP`.
    # where is the SP?
    registers[7] -= 1
​
# 2. Copy the value in the given register to the address pointed to by`SP`.
# get the value from the given register
# how to find which register to look at?
reg_idx = memory[pc + 1]
value = registers[reg_idx]
​
# How to copy the value to the correct address?
SP = registers[7]
memory[SP] = value
​
elif command == POP:
    #         1. Copy the value from the address pointed to by `SP`
    #            to the given register.
    # we need the SP address
    SP = registers[7]
    # we need value from that address
    value = memory[SP]
​
# we need the register address
reg_idx = memory[pc + 1]
# then put the value in the register
registers[reg_idx] = value
​
# 2. Increment `SP`.
registers[7] += 1
​
elif command == CALL:
    # push command address after CALL onto stack
    # PC points to CALL address right now
    # get command address
    return_address = pc + 2
​
# Then push the return address onto the stack
# Step 1: decrement the SP, stored in R7
registers[7] -= 1
# Step 2: store the value at the SP address
SP = registers[7]
memory[SP] = return_address
​
# set PC to address stored in given register
# retrieve address from register
# find which register
reg_idx = memory[pc + 1]
​
# look in register to find address
subroutine_address = registers[reg_idx]
​
pc = subroutine_address
​
elif command == RET:
    # pop value from top of stack and store in PC
    SP = registers[7]
    return_address = memory[SP]
​
pc = return_address
​
registers[7] += 1
​
​
else:
    print('unknown command!')
    running = False
​
# don't do this if setting pc directly
sets_pc_directly = ((command >> 4) & 0b0001) == 1
if not sets_pc_directly:
    pc += 1 + num_args
