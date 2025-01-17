import random
import winsound
import os
import sys
import time

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
        line = line.strip()
        if line.startswith("`"):
            self.in_multiline_comment = True
            return
        
        elif 'if' in line and 'else' in line:
            self.handle_if_else(line)

        elif 'if' in line:
            self.handle_if(line)
        elif ':' in line and '=' not in line and not line.strip().startswith('"'):
            self.handle_empty_variable(line)

        elif '=' in line:
            self.handle_assignment(line)

        else:
            parts = line.split()
            command = parts[0]
            args = parts[1:]

            if command == "gregPr":
                self.handle_print(args)
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
            elif command == "gregSleep":
                self.handle_sleep(args)
            elif command == "make_file":
                self.handle_make_file()
            elif command == "gregCurDateTime":
                self.handle_current_datetime()
            elif command == "gregCurTime":
                self.handle_current_time()
            elif command == "gregCurDate":
                self.handle_current_date()
            else:
                print(f"Unrecognized command: {command} sob")

    def handle_if(self, line):
        condition_part = line.strip()[2:].strip()
        try:
            condition_start = condition_part.index('(') + 1
            condition_end = condition_part.index(')')
            condition = condition_part[condition_start:condition_end]

            condition_result = eval(condition, {}, self.variables)

            if condition_result:
                action_start = condition_part.index('then') + 4
                action = condition_part[action_start:].strip()[1:-1]
                self.execute(action)
        except ValueError:
            print("Error: Condition not found or invalid format.")
        except Exception as e:
            print(f"Error: {e}")
    def handle_if_else(self, line):
        condition_block = line.split("else")
        if len(condition_block) < 1:
            print("Error: Invalid if statement syntax.")
            return

        condition_part = condition_block[0].strip()[2:].strip()
        else_part = condition_block[1].strip() if len(condition_block) > 1 else None

        try:
            condition_start = condition_part.index('(') + 1
            condition_end = condition_part.index(')')
            condition = condition_part[condition_start:condition_end]

            condition_result = eval(condition, {}, self.variables)

            if condition_result:
                action_start = condition_part.index('then') + 4
                action = condition_part[action_start:].strip()[1:-1]
                self.execute(action)
            elif else_part:
                action = else_part.strip()[1:-1]
                self.execute(action)
        except ValueError:
            print("Error: Condition not found or invalid format.")
        except Exception as e:
            print(f"Error: {e}")

    def handle_empty_variable(self, line):
        var_name = line.strip(":").strip()
        if var_name:
            self.variables[var_name] = None

    def handle_assignment(self, line):
        var_name, value = line.split('=', 1)
        var_name = var_name.strip()
        value = value.strip()

        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace("\\n", "\n")
            if "{" in value and "}" in value: 
                value = eval(f'f"{value}"', {}, self.variables)
            self.variables[var_name] = value
        elif value.isdigit():
            self.variables[var_name] = int(value)
        elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
            self.variables[var_name] = float(value)
        elif value == "True":
            self.variables[var_name] = True
        elif value == "False":
            self.variables[var_name] = False
        elif ':' in value:
            self.variables[var_name] = value
        else:
            try:
                self.variables[var_name] = eval(value, {}, self.variables)
            except Exception:
                self.variables[var_name] = None


    def handle_print(self, args):
        value = " ".join(args)
        if (value.startswith('f"') and value.endswith('"')) or (value.startswith('f "') and value.endswith('"')):
            try:
                value = eval(value.replace('f "', 'f"').replace('f"', 'f"'), {}, self.variables)
                print(value.replace('\\n', '\n'))
            except Exception as e:
                print(f"Error evaluating f-string: {e}")
        elif value.startswith('"') and value.endswith('"'):
            print(value[1:-1].replace('\\n', '\n'))
        elif value == '\\n':
            print()
        elif value in self.variables:
            print(self.variables[value])
        else:
            try:
                print(eval(value, {}, self.variables))
            except:
                print(f"Warning: Undefined variable or invalid expression '{value}' in print statement rgr")

    def handle_input(self, args):
        var_name = args[0]
        prompt = " ".join(args[1:]) if len(args) > 1 else f"{var_name} >>> "
        if '"' in prompt:
            prompt = prompt.replace('"', '')
        if var_name.startswith('"') and var_name.endswith('"'):
            print("Error: Variable names cannot be enclosed in quotes.")
            return
        if var_name.endswith(":"):
            var_name = var_name[:-1]
        value = input(prompt)
        self.variables[var_name] = value.strip()

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

    def handle_sleep(self, args):
        try:
            time_seconds = int(args[0])
            time.sleep(time_seconds)
        except ValueError:
            print("Error: Invalid time value: Plz put a number g")

    def handle_current_datetime(self):
        print(time.strftime("%m/%d/%Y %H:%M:%S", time.localtime()))

    def handle_current_time(self):
        print(time.strftime("%I:%M:%S %p", time.localtime()))
    
    def handle_current_date(self):
        print(time.strftime("%m/%d/%Y", time.localtime()))
    
    
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
