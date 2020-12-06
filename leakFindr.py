import gdb

def stopHandler(msg):
    if (msg.stop_signal == "SIGSEGV"):
        info_out = gdb.execute("info reg eip", to_string = True)
        reg_split = info_out.split(" ")
        reg_split = [x for x in reg_split if x != '']
        print(reg_split[1][2:])
        eip_val_as_str = bytearray.fromhex(reg_split[1][2:]).decode()
        print(eip_val_as_str)

        with open("junk.txt") as filler:
            filler_to_str = filler.read()
            loc = filler_to_str.find(eip_val_as_str)
            print ("loc = ", loc)

gdb.events.stop.connect(stopHandler)

gdb.execute("r junk.txt")
gdb.execute("quit")
