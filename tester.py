from os import remove
from time import sleep
from re import findall
import subprocess


class test():
    def __init__(self, input_values, expected_output):
        self.input_values = input_values
        self.expected_output = expected_output


class test_producer():
    def prepare_code(self, code, out_file):
        """Writing code to file"""
        with open(out_file, 'w') as f:
            f.write(code)


    def compile_java(self, input_file, java_class):
        """Compiling c++ code"""
        command_line = ["javac", input_file]
        s = subprocess.Popen(command_line, stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE, stdin = subprocess.PIPE, universal_newlines = True)
        error = s.communicate()
        sleep(0.5)
        if s.returncode == 0:
            remove(input_file)
            return 0, str(java_class[0])
        else:
            return 1, error


    def compile_c(self, input_file):
        """Compiling c++ code"""
        out_file = input_file[:-2] + '.out'
        command_line = ["gcc", input_file, '-o', out_file, '-std=c99']
        s = subprocess.Popen(command_line, stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE, stdin = subprocess.PIPE, universal_newlines = True)
        error = s.communicate()
        sleep(0.5)
        if s.returncode == 0:
            remove(input_file)
            return 0, out_file
        else:
            return 1, error

    def compile_cpp(self, input_file):
        """Compiling c++ code"""
        out_file = input_file[:-4] + '.out'
        command_line = ["g++", input_file, '-o', out_file]
        s = subprocess.Popen(command_line, stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE, stdin = subprocess.PIPE, universal_newlines = True)
        error = s.communicate()
        sleep(0.5)
        if s.returncode == 0:
            remove(input_file)
            return 0, out_file
        else:
            return 1, error

    def check_python(self, input_file):
        command_line = ["python3", input_file]
        s = subprocess.Popen(command_line, stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE, stdin = subprocess.PIPE, universal_newlines = True)
        error = s.communicate(self.tests[0].input_values)
        sleep(0.5)
        if s.returncode == 0:
            return 0, input_file
        else:
            return 1, error

    def produce_test(self, test, command_line):
        """Producing test"""
        s = subprocess.Popen(command_line, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE,
                             universal_newlines = True)
        if test.input_values != '':
            q = s.communicate(test.input_values)
        else:
            q = s.communicate()
        q = str(q[0][:-1])
        return q == test.expected_output

    def tests_producing(self, code, file_name, lang):
        """Producing all tests"""
        if lang == 'python3':
            self.file_name = file_name + '.py'
            self.program_name = file_name + '.py'
            self.prepare_code(code, self.program_name)
            python_code_check = self.check_python(self.program_name)
            if python_code_check[0] != 0:
                print(python_code_check[1][1])
                self.tests_result = (False, python_code_check[1][1])
                remove(self.file_name)
                return False, python_code_check[1][1]
            self.command_line = ['python3', self.program_name]

        elif lang == 'cpp':
            self.file_name = file_name + '.cpp'
            self.prepare_code(code, self.file_name)
            compile_return = self.compile_cpp(self.file_name)
            if compile_return[0] != 0:
                print(compile_return[1][1])
                self.tests_result = (False, compile_return[1][1])
                remove(self.file_name)
                return False, compile_return[1][1]
            self.program_name = compile_return[1]
            self.command_line = ['./{0}'.format(self.program_name)]

        elif lang == 'c':
            self.file_name = file_name + '.c'
            self.prepare_code(code, self.file_name)
            compile_return = self.compile_c(self.file_name)
            if compile_return[0] != 0:
                print(compile_return[1][1])
                self.tests_result = (False, compile_return[1][1])
                remove(self.file_name)
                return False, compile_return[1][1]
            self.program_name = compile_return[1]
            self.command_line = ['./{0}'.format(self.program_name)]

        elif lang == 'java':
            self.file_name = file_name + '.java'
            java_class = findall(r'class ([a-zA-Z_]+)', self.code)
            self.prepare_code(code, self.file_name)
            compile_return = self.compile_java(self.file_name, java_class)
            if compile_return[0] != 0:
                print(compile_return[1][1])
                self.tests_result = (False, compile_return[1][1])
                remove(self.file_name)
                return False, compile_return[1][1]
            java_class = str(java_class[0])
            self.program_name = compile_return[1] + '.class'
            self.command_line = ['java', java_class]



        for i in self.tests:
            self.tests_result[1].append(self.produce_test(i, self.command_line))

        remove(self.program_name)
        return self.tests_result

    def __init__(self, tests_array, code, file_name, lang):
        self.tests = []
        self.tests_array = tests_array
        self.code = code
        self.tests_result = [True, []]
        for i in tests_array:
            self.tests.append(test(i[0], i[1]))

        self.tests_producing(self.code, file_name, lang)
