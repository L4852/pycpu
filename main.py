import time
from parse import parse


class Stage:
    def __init__(self):
        self.stage = 0

    def next(self):
        self.stage += 1


class Counter:
    def __init__(self, ram_size):
        self.current = 0
        self.max = ram_size - 1

    def increment(self):
        if self.current < self.max:
            self.current += 1
        else:
            self.current = 0

    def set(self, address):
        self.current = address


class ALU:
    def __init__(self, width):
        self.width = width
        self.zero = False
        self.negative = False

    def add(self, a, b):
        sum = a + b
        if sum < 2 ** self.width:
            self.zero = True if sum == 0 else False
            return sum
        return None

    def subtract(self, a, b):
        diff = a - b
        if abs(diff) < 2 ** self.width:
            self.zero = True if diff == 0 else False
            self.negative = True if diff < 0 else False
            return diff
        return None

    def inc(self, a):
        sum = a + 1
        if sum < 2 ** self.width:
            return sum


class Clock:
    def __init__(self, speed):
        self.delay = 1 / speed

    def tick(self):
        time.sleep(self.delay)


class Processor:
    def __init__(self, ram_contents: list):
        self.OPCODES = [
            "NO_OP",
            "LOAD_AI",
            "LOAD_BI",
            "ADD_AB",
            "SUB_AB",
            "JUMP",
            "JUMP_EQ",
            "JUMP_GT",
            "JUMP_LT",
            "SWAP_AB",
            "SWAP_AC",
            "INC_A",
            "CMP_AB",
            "-",
            "-",
            "HALT",
        ]

        self.HALTED = False

        self.ALU_WIDTH = 16

        self.RAM = ram_contents

        self.RAM_SIZE = len(self.RAM)

        for i in range(self.RAM_SIZE - len(self.RAM) - 1):
            self.RAM.append((0, 0))

        self.RAM.append((15, None))
        self.RAM_SIZE += 1

        self.REGISTERS = [0, 0, 0]
        self.GPREGS = [0, 0, 0, 0]

        self.PC = Counter(self.RAM_SIZE)

        self.INSREG = (0, 0)

        self.INSADRREG = 0

        self.ALUO = ALU(self.ALU_WIDTH)

    def fetch(self):
        self.INSREG = self.RAM[self.PC.current]
        print(f"{self.PC.current} | -> INSTR: [{self.OPCODES[self.INSREG[0]]}, {self.INSREG[1]}]")
        self.PC.increment()

    def execute(self):
        op, data = self.INSREG
        func = getattr(self, self.OPCODES[op])

        if data is not None:
            func(data)
        else:
            func()

    def NO_OP(self, val):
        pass

    def HALT(self):
        print("HALTED")
        self.HALTED = True

    def JUMP(self, addr):
        self.PC.set(addr)
        print(f"JUMP -> {addr}")

    def JUMP_EQ(self, addr):
        if self.ALUO.zero:
            self.PC.set(addr)
            print(f"JUMP -> {addr}")

    def JUMP_GT(self, addr):
        if not self.ALUO.zero and not self.ALUO.negative:
            self.PC.set(addr)
            print(f"JUMP -> {addr}")

    def JUMP_LT(self, addr):
        if not self.ALUO.zero and self.ALUO.negative:
            self.PC.set(addr)
            print(f"JUMP -> {addr}")

    def LOAD_AI(self, val):
        self.REGISTERS[0] = val
        print(f"Saved {val} to RA.")

    def LOAD_BI(self, val):
        self.REGISTERS[1] = val
        print(f"Saved {val} to RB.")

    def ADD_AB(self):
        sum = self.ALUO.add(self.REGISTERS[0], self.REGISTERS[1])

        if sum:
            self.REGISTERS[2] = sum

        print(f"Saved [{self.REGISTERS[0]} + {self.REGISTERS[1]}] to RC")

    def SUB_AB(self):
        diff = self.ALUO.subtract(self.REGISTERS[0], self.REGISTERS[1])

        if diff:
            self.REGISTERS[2] = diff

        print(f"Saved [{self.REGISTERS[0]} + {self.REGISTERS[1]}] to RC")

    def SWAP_AB(self):
        temp = self.REGISTERS[0]
        self.REGISTERS[0] = self.REGISTERS[1]
        self.REGISTERS[1] = temp

    def SWAP_AC(self):
        temp = self.REGISTERS[0]
        self.REGISTERS[0] = self.REGISTERS[2]
        self.REGISTERS[2] = temp

    def INC_A(self):
        self.REGISTERS[0] = self.ALUO.inc(self.REGISTERS[0])
        print(f"RA: [{self.REGISTERS[0]}]")

    def CMP_AB(self):
        self.ALUO.subtract(self.REGISTERS[0], self.REGISTERS[1])


def run(clock_speed=1, files=None):
    if files is None:
        files = []
    clock = Clock(clock_speed)
    # Clock speed approximately in Hz

    unclocked = False

    if clock_speed == -1:
        unclocked = True

    programs = []

    for file in files:
        with open(file + '.txt', 'r') as f:
            data = str(f.read())
            programs.extend(parse(data))

    cpu = Processor(programs)
    while True:
        if not cpu.HALTED:
            if not unclocked:
                clock.tick()
            cpu.fetch()
            cpu.execute()
        else:
            break


def main():
    files = ["testprogram"]

    run(-1, files)


if __name__ == "__main__":
    main()
