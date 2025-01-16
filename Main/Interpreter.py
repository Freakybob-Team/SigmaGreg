import random
import winsound
import os
import sys
import time

class TheInterpreter:
    def __init__(self):
        self.variables = {}
        self.program_lines = []
        self.functions = {}
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
                        self.execute(line)
        except Exception as e:
            print(f"ERRRORORR reading file '{filename}': {e}")

        

            
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
            elif command == "gregCall":
                self.handle_function_call(args)
            elif command == "gregDef":
                self.handle_function_definition(line, self.program_lines)
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

        try:
            self.variables[var_name] = eval(value, {}, self.variables)
        except:
            if value.startswith('"') and value.endswith('"'):
                self.variables[var_name] = value[1:-1].replace("\\n", "\n")
            elif value == "True":
                self.variables[var_name] = True
            elif value == "False":
                self.variables[var_name] = False
            else:
                self.variables[var_name] = value

    def handle_print(self, args):
        value = " ".join(args)
        try:
            value = eval(value, {}, self.variables)
            print(value)
        except:
            if (value.startswith('f"') and value.endswith('"')) or (value.startswith('f "') and value.endswith('"')):
                try:
                    value = eval(value.replace('f "', 'f"').replace('f"', 'f"'), {}, self.variables)
                except Exception as e:
                    print(f"Error evaluating f-string: {e}")
            elif value.startswith('"') and value.endswith('"'):
                print(value[1:-1].replace('\\n', '\n'))
            elif value == '\\n':
                print()
            elif value in self.variables:
                print(self.variables[value])
            else:
                print(f"Warning: Undefined variable '{value}' in print statement rgr")

    def handle_input(self, args):
        var_name = " ".join(args)
        if var_name.startswith('"') and var_name.endswith('"'):
            print("Error: Variable names cannot be enclosed in quotes.")
            return
        if var_name.endswith(":"):
            var_name = var_name[:-1]
        value = input(f"{var_name} >>> ")
        self.variables[var_name] = value

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

    def parse_lines(self, lines):
        line_idx = 0
        while line_idx < len(lines):
            line = lines[line_idx].strip()

            if line.startswith("greg "):
                self.execute(line)
            elif line.startswith("gregDef "):
                self.handle_function_definition(line, lines, line_idx)
                line_idx += 1
            else:
                line_idx += 1

        if "main" in self.functions:
            self.run_function("main")
        else:
            for line in lines:
                self.execute(line.strip())
    def handle_function_definition(self, line, lines, line_idx):
        function_name = line[8:].strip().split("{")[0].strip()
        if not function_name:
            print("Error: function error - Missing function name S:OBS:")
            return

        function_body = []
        open_brackets = 0
        line_idx += 1

        while line_idx < len(lines):
            line = lines[line_idx].strip()

            if "{" in line:
                open_brackets += 1
            if "}" in line:
                open_brackets -= 1

            if open_brackets == 0 and line != "}":
                break

            if line:
                function_body.append(line)
            line_idx += 1

        self.functions[function_name] = function_body

    def handle_function_call(self, args):
        function_name = args[0]
        if function_name in self.functions:
            self.run_function(function_name)
        else:
            print(f"Function '{function_name}' not defined SOB")

    def run_function(self, function_name):
        function_body = self.functions[function_name]
        for line in function_body:
            self.execute(line)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        interpreter = TheInterpreter()
        interpreter.run(filename)
        print("----------------------------------------------")
        input("Press enter to exit..")  




