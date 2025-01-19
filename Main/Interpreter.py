import random
import winsound
import os
import sys
import time

class TheInterpreter:
    def __init__(self):
        self.variables = {}
        self.program_lines = []

    def run(self, filename):
        if os.path.exists(filename):
            self.run_file(filename)
        else:
            print(f"Error: File '{filename}' not found SOB")

    def run_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        self.execute(line, filename)
        except Exception as e:
            print(f"ERRRORORR reading file '{filename}': {e}")

    def execute(self, line, filename):
        line = line.strip()
        if line.startswith("`"):
            self.in_multiline_comment = True
            return

        elif line.startswith("include"):
            self.handle_include(line, filename)

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
            elif command == "gregCurDateTime":
                self.handle_current_datetime()
            elif command == "gregCurDate":
                self.handle_current_date()
            elif command == "gregCurTime":
                self.handle_current_time()
            elif command == "gregClear":
                self.handle_clear()
            elif command == "gregWriteToFile":
                self.handle_write_to_file(args)
            elif command == "gregReadFile":
                self.handle_read_file(args)
            elif command == "exit":
                sys.exit()
            elif command == "gregExit":
                raise SystemExit
            elif command == "gregLeave":
                raise SystemExit
            elif command == "gregQuit":
                raise SystemExit
            else:
                print(f"Unrecognized command: {command} sob")

    def handle_include(self, line, filename):
        parts = line.split()
        if len(parts) > 1:
            include_filename = parts[1].strip('"')
            if os.path.exists(include_filename):
                self.run_file(include_filename)
            else:
                print(f"Error: Include file '{include_filename}' not found in {filename}")

    def handle_if(self, line):
        if line.startswith("gregPr"):
            line = line.replace("gregPr", "").strip().strip('"')
            print(line)
            return
    
        condition_part = line.strip()[2:].strip()
        try:
            condition_start = condition_part.index('(') + 1
            condition_end = condition_part.index(')')
            condition = condition_part[condition_start:condition_end]

            condition_result = eval(condition, {}, self.variables)

            if condition_result:
                action_start = condition_part.index('then') + 4
                action = condition_part[action_start:].strip()[1:-1]
                self.execute(action, "Inline")
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
                self.execute(action, "Inline")
            elif else_part:
                action = else_part.strip()[1:-1]
                self.execute(action, "Inline")
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

    def handle_beep(self):        
        winsound.Beep(1000, 500)

    def handle_random(self, args):
        min_val, max_val = map(int, args)
        if min_val >= max_val:
            print("Error: Invalid range for random number generation :sob:")
            return
        print(f"{random.randint(min_val, max_val)}")

    def handle_type(self, args):
        var_name = args[0]
        if var_name in self.variables:
            value = self.variables[var_name]
            print(f"Variable '{var_name}' is of type {type(value).__name__} greg")
        else:
            print(f"Error: Variable '{var_name}' not found greg")

    def handle_print_all(self):
        print("Current variables:")
        for var_name, value in self.variables.items():
            print(f"{var_name} = {value}")

    def handle_sleep(self, args):
        try:
            time_seconds = int(args[0])
            time.sleep(time_seconds)
        except ValueError:
            print("Error: Invalid time value: Plz put a number g")

    def handle_clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def handle_current_datetime(self):
        print(time.strftime("%m/%d/%Y %H:%M:%S", time.localtime()))

    def handle_current_time(self):
        print(time.strftime("%I:%M:%S %p", time.localtime()))

    def handle_current_date(self):
        print(time.strftime("%m/%d/%Y", time.localtime()))

    def handle_write_to_file(self, args):
        filename = args[0].strip('"')
        content = " ".join(args[1:]).strip('"')
        try:
            with open(filename, 'w') as f:
                f.write(content)
            print(f"Written to file: {filename}")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def handle_read_file(self, args):
        filename = args[0].strip('"')
        try:
            with open(filename, 'r') as f:
                content = f.read()
            print(content)
        except Exception as e:
            print(f"Error reading file: {e}")
            
if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        interpreter = TheInterpreter()
        interpreter.run(filename)
        print("----------------------------------------------")
        input("Press enter to exit..")
