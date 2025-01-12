# fuck c++, python is easier

import random
import winsound
import os
import sys

class TheInterpreter:
    def __init__(self):
        self.variables = {}
        self.program_lines = []
    
    def run(self, filename=None):
        if filename:
            self.run_file(filename)
        else:
            self.run_interactive()

    def run_file(self, filename):
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            return
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        self.execute(line)
        except Exception as e:
            print(f"Error reading file '{filename}': {e}")

    def run_interactive(self):
        print("SigmaGreg Terminal: Type the commands below to execute one line programs! Type 'exit' to quit... type 'gregWRITE' to write a program!!!!")
        while True:
            line = input("> ")
            if line == "exit":
                print("Exiting the interpreter, bai bai!!!")
                break
            try:
                self.execute(line)
            except Exception as e:
                print(f"Error: {e}")

    def execute(self, line):
        if ':' in line and '=' not in line and not line.strip().startswith('"'):
            self.handle_empty_variable(line)
        elif '=' in line:
            self.handle_assignment(line)
        else:
            parts = line.split()
            command = parts[0]
            args = parts[1:]

            if command == "gregPr":
                self.handle_print(args)
            elif command == "gregMa":
                self.handle_math(args)
            elif command == "gregIn":
                self.handle_input(args)
            elif command == "gregWRITE":
                self.handle_write()
            elif command == "gregRUN":
                self.handle_run()
            elif command == "gregType":
                self.handle_type(args)
            elif command == "gregRandom":
                self.handle_random(args)
            elif command == "gregPrintAll":
                self.handle_print_all()
            elif command == "gregBeep":
                self.handle_beep()
            elif command == "make_file":
                self.handle_make_file()
            else:
                print(f"Unrecognized command: {command} sob")

    def handle_empty_variable(self, line):
        var_name = line.strip(":").strip()
        if var_name:
            self.variables[var_name] = None

    def handle_assignment(self, line):
        var_name, value = line.split('=', 1)
        var_name = var_name.strip()
        value = value.strip()

        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
            self.variables[var_name] = value
        elif value.isdigit():
            self.variables[var_name] = int(value)
        elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
            self.variables[var_name] = float(value)
        elif ':' in value:
            self.variables[var_name] = value
        else:
            self.variables[var_name] = None



    def handle_print(self, args):
        value = " ".join(args)
        if value.startswith('f"') and value.endswith('"'):
            try:
                value = eval(value, {}, self.variables)
                print(value)
            except Exception as e:
                print(f"Error evaluating f-string: {e}")
        elif value.startswith('f "') and value.endswith('"'):
            try:
                value = eval('f"' + value[3:], {}, self.variables)
                print(value)
            except Exception as e:
                print(f"Error evaluating f-string: {e}")
        elif value.startswith('"') and value.endswith('"'):
            print(value[1:-1])
        elif value in self.variables:
            print(self.variables[value])
        else:
            print(f"Warning: Undefined variable '{value}' in print statement rgr")


    

    def handle_math(self, args):
        if len(args) == 3:
            operand1, operator, operand2 = float(args[0]), args[1], float(args[2])
            result = {
                "+": operand1 + operand2,
                "-": operand1 - operand2,
                "*": operand1 * operand2,
                "/": operand1 / operand2 if operand2 != 0 else "Error: Division by zero dummy"
            }.get(operator, f"Error: Unknown operation '{operator}' greg/ Supported operations are: +, -, *, /")
            if isinstance(result, str):
                print(result)
            else:
                print(int(result) if result.is_integer() else result)
        else:
            var_name, operand1, operator, operand2 = args[0], float(args[1]), args[2], float(args[3])
            result = {
                "+": operand1 + operand2,
                "-": operand1 - operand2,
                "*": operand1 * operand2,
                "/": operand1 / operand2 if operand2 != 0 else "Error: Division by zero dummy"
            }.get(operator, f"Error: Unknown operation '{operator}' greg/ Supported operations are: +, -, *, /")
            if isinstance(result, str):
                print(result)
            else:
                self.variables[var_name] = int(result) if result.is_integer() else result

    def handle_input(self, args):
        var_name = " ".join(args)
        if var_name.startswith('"') and var_name.endswith('"'):
            print("Error: Variable names cannot be enclosed in quotes.")
            return
        if var_name.endswith(":"):
            var_name = var_name[:-1]
        value = input(f"{var_name} >>> ")
        self.variables[var_name] = value


    def handle_write(self):
        print("Enter your code below. Type 'end' to finish writing the program!!!!")
        while True:
            line = input()
            if line == "end":
                break
            self.program_lines.append(line)
        print("Program written successfully. Type 'gregRUN' to run it! Type 'make_file' to turn your file into a .sgc file!")

    def handle_run(self):
        if not self.program_lines:
            print("No program to run. Please write a program first using 'gregWRITE' greg")
            return
        print("Running program...")
        for line in self.program_lines:
            self.execute(line)
        self.program_lines.clear()
        print("Program execution complete :fire:")

    def handle_type(self, args):
        var_name = args[0]
        if var_name in self.variables:
            value = self.variables[var_name]
            print(f"Variable '{var_name}' is of type {type(value).__name__} greg")
        else:
            print(f"Error: Variable '{var_name}' not found greg")

    def handle_random(self, args):
        min_val, max_val = map(int, args)
        if min_val >= max_val:
            print("Error: Invalid range for random number generation :sob:")
            return
        print(f"Random number: {random.randint(min_val, max_val)}")

    def handle_print_all(self):
        print("Current variables:")
        for var_name, value in self.variables.items():
            print(f"{var_name} = {value}")
            
    def handle_beep(self):        
        winsound.Beep(1000, 500)

    def handle_make_file(self):
        if not self.program_lines:
            print("No program to save... Please write a program first using 'gregWRITE' greg!")
            return
        filename = input("Enter the name for your .sgc file!: ")
        if not filename:
            print("File name cannot be empty dummy")
            return
        if not filename.endswith(".sgc"):
            filename += ".sgc"
        try:
            with open(filename, 'w') as file:
                for line in self.program_lines:
                    file.write(line + "\n")
            print(f"Program saved successfully to {filename}!!!")
        except Exception as e:
            print(f"Error saving file: {e}")
        


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        interpreter = TheInterpreter()
        interpreter.run(filename)
    else:
        interpreter = TheInterpreter()
        interpreter.run()

