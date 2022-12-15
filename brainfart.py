from typing import *

class BrainFart:
    def __init__(
        self,
        code: str = "",
        data: List[int] = [0] * 1000,
        instruction_pointer: int = 0,
        data_pointer: int = 0,
    ):
        """BrainFart Init
        :param code <str>: The program to run. Defaults to empty string.
        :param data <List[int]>: The data to use. Defaults to 1000 cells of 0.
        :param instruction_pointer <int>: The instruction pointer. Defaults to 0.
        :param data_pointer <int>: The data pointer. Defaults to 0.

        :return <BrainFart>: A BrainFart object.
        """
        self.instructions = "+-<>.,[]"
        self.code = "".join([c for c in code if c in self.instructions])
        self.data = data
        self.iPtr = instruction_pointer
        self.dPtr = data_pointer

    def run(
        self,
    ) -> List[int]:

        while self.iPtr < len(self.code):
            c = self.code[self.iPtr]
            if c == "+":
                self.data[self.dPtr] += 1
            elif c == "-":
                self.data[self.dPtr] -= 1
            elif c == ">":
                self.dPtr += 1
            elif c == "<":
                self.dPtr -= 1
            elif c == ".":
                print(chr(self.data[self.dPtr]), end="")
            elif c == ",":
                self.data[self.dPtr] = ord(input()[0])
            elif c == "[":
                if not self.data[self.dPtr]:
                    d, cx = 0, self.iPtr
                    while d != -1:
                        cx += 1
                        if self.code[cx] in "[]":
                            d += 1 if self.code[cx] == "[" else -1
                    self.iPtr = cx

            elif c == "]":
                if self.data[self.dPtr]:
                    d, cx = 0, self.iPtr
                    while d != -1:
                        cx -= 1
                        if self.code[cx] in "[]":
                            d += 1 if self.code[cx] == "]" else -1
                    self.iPtr = cx
            self.iPtr += 1
        return self.data


def exampleA():
    # adds two numbers A, B. leaves the result in B
    program = "[->+<]"
    data = [10, 20] + [0] * 8
    bf = BrainFart(program, data)
    output = bf.run()
    print(output)
    return output


def exampleB():
    # program that moves a block of values one cell to the right
    program = ">>>[[->+<]<]"
    data = [0] * 10
    data[1:4] = [2, 3, 4]
    # ↑↑ 0 followed by 2, 3, 4 followed by 6 0s (10 total)
    bf = BrainFart(program, data)
    output = bf.run()
    print(output)
    return output

def print_help():
    print("BrainFart.py - A BrainFart interpreter written in Python")
    print("Usage: brainfart.py <file>")
    hString = """
    +: Increment the value at the current cell by 1.
    -: Decrement the value at the current cell by 1.
    >: Move the data pointer to the next cell.
    <: Move the data pointer to the previous cell.
    .: Output the value at the current cell.
    ,: Input a value and store it at the current cell.
    [: If the value at the current cell is 0, jump to the matching ].
    ]: If the value at the current cell is nonzero, jump to the matching [.
    """
    print(hString)
    hString = """
    ------------------------
    Example A:
    # adds two numbers A, B. leaves the result in B

    program = "[->+<]"
    data = [10, 20] + [0] * 8 # 10 cells [10, 20, 0...]
    print(data)
    >>> [10, 20, 0, 0, 0, 0, 0, 0, 0, 0]

    bf = BrainFart(program, data)
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

    bf = BrainFart(program, data)
    print(bf.run())

    >>> [0, 0, 2, 3, 4, 0, 0, 0, 0, 0]
    """
def __main():
    import sys, argparse
    # -p, --program <str>: The program to run. Defaults to empty string.
    # -f, --file <str>: The file to run. Defaults to empty string.
    # -d, --data <str>: CSV of data to use. Defaults to 1000 cells of 0 if not provided.
    parser = argparse.ArgumentParser(description="BrainFart.py - A BrainFart interpreter written in Python")
    # parser.add_argument("-h", "--help", action="store_true", help="Prints this help message.")
    parser.add_argument("-p", "--program", type=str, default="", help="The program to run. Defaults to empty string.")
    parser.add_argument("-f", "--file", type=str, default="", help="The file to run. Defaults to empty string.")
    parser.add_argument("-d", "--data", type=str, default="", help="CSV of data to use. Defaults to 1000 cells of 0 if not provided.")
    args = parser.parse_args()

    if (len(sys.argv) == 1):
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
    
    bf = BrainFart(program, data)
    output = bf.run()
    print(output)



if __name__ == "__main__":
    __main()
    