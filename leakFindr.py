import gdb,sys
import re

def stopHandler(msg):
    if (msg.stop_signal == "SIGSEGV"):
        info_out = gdb.execute("info reg eip", to_string = True)
        info_out.replace("\t", " ")
        reg_split= re.split(' |\t', info_out)
        reg_split = [x for x in reg_split if x != '']
        eip_val_as_str = bytearray.fromhex(reg_split[1][2:]).decode()
        print(eip_val_as_str)

        with open("junk.txt") as filler:
            filler_to_str = filler.read()
            loc = filler_to_str.find(eip_val_as_str)
            print ("loc = ", loc)

gdb.events.stop.connect(stopHandler)

gdb.execute("r junk.txt")
sys.exit(0)
