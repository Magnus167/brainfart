
class BrainFvck:
    def __init__(self, size=1024, dataArr=None, program=None):
        if dataArr:
            self.data = dataArr
        else:
            self.data = [0] * size
        
        if program:
            self.load(program)
    
    def _run_single(self, instr, dataPtr, instrPtr):
        if instr == '>':
            dataPtr += 1
        if instr == '<':
            dataPtr -= 1
        if instr == '+':
            self.data[dataPtr] += 1
        if instr == '-':
            self.data[dataPtr] -= 1
        if instr == '.':
            print(chr(self.data[dataPtr]), end='')
        if instr == ',':
            self.data[dataPtr] = ord(input())
        if instr == '[':
            pass
        if instr == ']':
            pass

        return dataPtr, instrPtr + 1

    def _run_loop(self, loop_program, data_ptr, program_ptr):
        while self.data[data_ptr] != 0:
            self._run(loop_program, data_ptr, program_ptr)
            
    def _get_loop(self, program, program_ptr):
        i, j, k = 1, 0, 1
        while i != j:
            i += int(program[k] == '[')
            j += int(program[k] == ']')
            k += 1
        return program[program_ptr + 1:program_ptr + k - 1]
          
    def load(self, program):
        self.program = program
        if ~('data' in self.__dict__):
            self.data = [0] * 30000
    def load_file(self, filename):
        try:
            with open(filename, 'r') as f:
                program = f.read()
            self.load(program)
        except FileNotFoundError:
            raise Exception('File not found')

    def run(self):
        try:
            return self._run(self.program)
        except AttributeError:
            raise Exception('No program loaded')


    def _run(self, program, data_ptr=0, program_ptr=0):
        
        # remove all non-brainfuck characters
        program = ''.join([c for c in program if c in '<>+-.,[]'])        
        running = len(program) > 0
        self.data_ptr = data_ptr
        self.program_ptr = program_ptr
        
        while running:
            instr = program[self.program_ptr]
            if instr == '[':
                loop_program = self._get_loop(program, self.program_ptr)
                self._run_loop(loop_program, self.data_ptr, self.program_ptr)
                # self.program_ptr += len(loop_program) + 2
            else:
                self.data_ptr, self.program_ptr = self._run_single(instr, self.data_ptr, self.program_ptr)
            
            running = self.program_ptr < len(program)

        return self.data


def help_string():
    
    dString = \
'''
Example:
Declare a 10-element array and set the first element to 50, and the second to 20. 
Then adding the storing the sum of the two elements in the second element.
        
>> dataArr = [0] * 10
>> dataArr[0:1] = [50, 20]

>> bf = BrainFvck(dataArr=dataArr)
>> print(dataArr)
>> print(bf._run("[->+<]")) 
    
Output:
'''
    print(dString)
    dataArr = [0] * 10
    dataArr[0:1] = [50, 20]

    bf = BrainFvck(dataArr=dataArr)
    print(dataArr)
    print(bf._run("[->+<]")) 

    dString = \
'''
--------------------
Example:
Print "Hello world" by setting the first 11 elements to the ASCII values of "Hello world" and then printing each element.
(Setting the values in BF itself is a bit tedious, so they are just set in Python first)

>> dataArr = [0] * 20
>> dataArr[0:11] = [72, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100]

>> bf = BrainFvck(dataArr=dataArr)
>> p = '.>' * 11   
>> bf.load(p)
>> bf.run()
    
Output:
'''
    print(dString)

    dataArr = [0] * 20
    dataArr[0:11] = [72, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100]

    bf = BrainFvck(dataArr=dataArr)
    p = '.>' * 11   
    bf.load(p)
    bf.run()


if __name__ == '__main__':
    import sys
    
    usage_str =  'python brainfuck.py filename'
    if len(sys.argv) == 1:
        help_string()
    elif len(sys.argv) == 2:
        if sys.argv[1].strip().lower() in ['-h', '--help']:
            help_string()
        else:
            bf = BrainFvck()
            bf.load_file(sys.argv[1])
            bf.run()

