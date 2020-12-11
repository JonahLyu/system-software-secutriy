import subprocess

"""
    getPadding.py

    This module will call a bash command of "gdb -x leakFindr.py -q " + file_to_corrupt.
    The out put of this will be filtered so that we get the padding needed to cause a stack overflow
"""
def get_padding(file_to_corrupt = "vuln3-32-test"):
#file_to_corrupt = "vuln3-32-test"
    bashCommand = "gdb -x leakFindr.py -q " + file_to_corrupt

    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf-8').split("\n")
    padding_str = [x for x in output if x.find('loc = ') > -1][0]
    padding = int(padding_str[7:])
    return padding

if (__name__ == "__main__"):
    padding = get_padding("vuln3-32")
    print(padding)
