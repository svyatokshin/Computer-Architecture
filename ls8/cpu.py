# """CPU functionality."""

# import sys


# class CPU:
#     """Main CPU class."""

#     def __init__(self):
#         """Construct a new CPU."""
#         self.reg = [0] * 8
#         self.pc = 0
#         self.ram = [0] * 256

#     def load(self):
#         """Load a program into memory."""

#         address = 0

#         # # For now, we've just hardcoded a program:

#         # program = [
#         #     # From print8.ls8
#         #     0b10000010,  # LDI R0,8
#         #     0b00000000,
#         #     0b00001000,
#         #     0b01000111,  # PRN R0
#         #     0b00000000,
#         #     0b00000001,  # HLT
#         # ]

#         # for instruction in program:
#         #     self.ram[address] = instruction
#         #     address += 1

#         if len(sys.argv) < 2:
#             print("Remember to pass second filename")
#             print("usage: python3 fileio.py <second_file_name.ls8>")
#             exit()

#         file = sys.argv[1]

#         try:
#             with open(file, 'r') as f:
#                 for line in f:
#                     if line != "\n" and line[0] != '#':
#                         self.ram[address] = int(line[0:8], 2)
#                         address += 1

#         except FileNotFoundError:
#             print(f'Error from {sys.argv[0]}: file {sys.argv[1]} not found!')
#             exit()

#     def alu(self, op, reg_a, reg_b):
#         """ALU operations."""

#         if op == "ADD":
#             self.reg[reg_a] += self.reg[reg_b]
#         elif op == "SUB":
#             self.reg[reg_a] -= self.reg[reg_b]
#         elif op == "MUL":
#             self.reg[reg_a] *= self.reg[reg_b]
#         elif op == "DIV":
#             self.reg[reg_a] /= self.reg[reg_b]
#         elif op == "OR":
#             self.reg[reg_a] |= self.reg[reg_b]

#         else:
#             raise Exception("Unsupported ALU operation")

#     def trace(self):
#         """
#         Handy function to print out the CPU state. You might want to call this
#         from run() if you need help debugging.
#         """

#         print(f"TRACE: %02X | %02X %02X %02X |" % (
#             self.pc,
#             # self.fl,
#             # self.ie,
#             self.ram_read(self.pc),
#             self.ram_read(self.pc + 1),
#             self.ram_read(self.pc + 2)
#         ), end='')

#         for i in range(8):
#             print(" %02X" % self.reg[i], end='')

#         print()

#     def ram_read(self, address):
#         return self.ram[address]

#     def ram_write(self, address, value):
#         self.reg[address] = value

#     def run(self):
#         """Run the CPU."""
#         running = True

#         while running:
#             command = self.ram[self.pc]
#             # self.trace()
#             if command == 0b10000010:  # LDI
#                 self.reg[self.ram_read(self.pc + 1)
#                          ] = self.ram_read(self.pc + 2)
#                 # self.pc += 2

#             elif command == 0b01000111:  # PRN
#                 print(self.reg[self.ram_read(self.pc + 1)])
#                 # self.pc += 1

#             elif command == 0b10100010:  # MUL
#                 self.alu("MUL", self.ram_read(self.pc + 1),
#                          self.ram_read(self.pc + 2))

#             elif command == 0b00000001:  # HLT
#                 running = False

#             else:
#                 print('unknown command!')
#                 running = False

#             # self.pc += 1
#             self.pc += (command >> 6) + 1


"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256

        self.registers = [0] * 8

        self.registers[7] = 0xF4

        self.pc = 0

    def load(self):
        """Load a program into memory."""

        if (len(sys.argv)) != 2:
            print("remember to pass the second file name")
            print("usage: python3 fileio.py <second_file_name.py>")
            sys.exit()

        address = 0
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    # parse the file to isolate the binary opcodes
                    possible_number = line[:line.find('#')]
                    if possible_number == '':
                        continue  # skip to next iteration of loop
                    instruction = int(possible_number, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
            sys.exit()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.pc,
    #         #self.fl,
    #         #self.ie,
    #         self.ram_read(self.pc),
    #         self.ram_read(self.pc + 1),
    #         self.ram_read(self.pc + 2)
    #     ), end='')

    #     for i in range(8):
    #         print(" %02X" % self.reg[i], end='')

    #     print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:

            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            num_operands = IR >> 6
            self.pc += 1 + num_operands

            is_alu_op = ((IR >> 5) & 0b001) == 1

            if is_alu_op:
                self.alu(operand_a, operand_b)

            if IR == HLT:
                running = False

            elif IR == LDI:
                self.registers[operand_a] = operand_b

            elif IR == PRN:
                print(self.registers[operand_a])
