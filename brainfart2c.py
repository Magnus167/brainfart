from typing import *

class BrainFart2C:
    def __init__(
        self,
        code: str = "",
        data: List[int] = [0] * 1000,
        instruction_pointer: int = 0,
        data_pointer: int = 0,
        outfile: str = "brainfart2c_out.c",
    ):
        """BrainFart2C Init
        :param code <str>: The program to run. Defaults to empty string.
        :param data <List[int]>: The data to use. Defaults to 1000 cells of 0.
        :param instruction_pointer <int>: The instruction pointer. Defaults to 0.
        :param data_pointer <int>: The data pointer. Defaults to 0.

        :return <BrainFart2C>: A BrainFart2C object.
        """
        self.instructions = "+-<>.,[]"
        self.code = "".join([c for c in code if c in self.instructions])
        self.data = data
        self.iPtr = instruction_pointer
        self.dPtr = data_pointer

    def generate(self):
        instr_map = {
            "+": "++*ptr;",
            "-": "--*ptr;",
            ">": "++ptr;",
            "<": "--ptr;",
            ".": "putchar(*ptr);",
            ",": "*ptr = getchar();",
            "[": "while(*ptr){",
            "]": "}",
        }
        p = f"char array[{len(self.data)}] = {self.data};"
        p += f"char *ptr = array;"
        for instr in instr_map:
            p += self.code.replace(instr, instr_map[instr])

        if self.outfile:
            with open(self.outfile, "w") as f:
                f.write(p)
        else:
            return p                


def exampleA():
    # adds two numbers A, B. leaves the result in B
    program = "[->+<]"
    data = [10, 20] + [0] * 8
    bf = BrainFart2C(program, data)
    output = bf.run()
    print(output)
    return output


def exampleB():
    # program that moves a block of values one cell to the right
    program = ">>>[[->+<]<]"
    data = [0] * 10
    data[1:4] = [2, 3, 4]
    # ↑↑ 0 followed by 2, 3, 4 followed by 6 0s (10 total)
    bf = BrainFart2C(program, data)
    output = bf.run()
    print(output)
    return output

def print_help():
    print("BrainFart2C.py - A BrainFart-to-C converter written in Python")
    print("Usage: BrainFart2C.py <file>")
    hString = """
    +: Increment the value at the current cell by 1.
    -: Decrement the value at the current cell by 1.
    >: Move the data pointer to the next cell.
    <: Move the data pointer to the previous cell.
    .: Output the value at the current cell.
    ,: Input a value and store it at the current cell.
    [: If the value at the current cell is 0, jump to the matching ].
    ]: If the value at the current cell is nonzero, jump to the matching [.
    ------------------------
    This program does not compile the C code. It only generates it.
    ------------------------
    Example A:
    # adds two numbers A, B. leaves the result in B

    program = "[->+<]"
    data = [10, 20] + [0] * 8 # 10 cells [10, 20, 0...]
    print(data)
    >>> [10, 20, 0, 0, 0, 0, 0, 0, 0, 0]

    bf = BrainFart2C(program, data)
    output = bf.run()

    print(output)
    >>> 0, 30, 0, 0, 0, 0, 0, 0, 0, 0]
    ------------------------
    Example B:
    # program that moves a block of values one cell to the right
    program = ">>>[[->+<]<]"
    data = [0] * 10
    data[1:4] = [2, 3, 4]
    print(data)
    >>> [0, 2, 3, 4, 0, 0, 0, 0, 0, 0]

    bf = BrainFart2C(program, data)
    print(bf.run())

    >>> [0, 0, 2, 3, 4, 0, 0, 0, 0, 0]
    ------------------------
    """
    print(hString)
def __main():
    import sys, argparse
    # -p, --program <str>: The program to run. Defaults to empty string.
    # -f, --file <str>: The file to run. Defaults to empty string.
    # -d, --data <str>: CSV of data to use. Defaults to 1000 cells of 0 if not provided.
    parser = argparse.ArgumentParser(description="BrainFart2C.py - A BrainFart-to-C converter written in Python")
    # parser.add_argument("-h", "--help", action="store_true", help="Prints this help message.")
    parser.add_argument("-p", "--program", type=str, default="", help="The program to run. Defaults to empty string.")
    parser.add_argument("-f", "--file", type=str, default="", help="The file to run. Defaults to empty string.")
    parser.add_argument("-d", "--data", type=str, default="", help="CSV of data to use. Defaults to 1000 cells of 0 if not provided.")
    args = parser.parse_args()

    if (len(sys.argv) == 1) or (args.help):
        print_help()
        sys.exit(0)

    if args.file:
        with open(args.file, "r") as f:
            program = f.read()
    else:
        program = args.program

    if args.data:
        data = [int(d) for d in args.data.split(",")]
    else:
        data = [0] * 1000
    
    bf = BrainFart2C(program, data)
    output = bf.run()
    print(output)



if __name__ == "__main__":
    __main()
    