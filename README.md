# S3_CW

# Pre-requisite
- [ ]  Having ROPgadget in PATH
- [ ]  python 3 

# Quick Usage

```
make vuln3
make ex
```
The above command actully calls:

```shell
#compile first
gcc -fno-stack-protector -m32 -static vuln3.c -o vuln3-32 

#call the script to exploit binary 
python3 auto-exploit.py vuln3-32 command.txt

#test output
./vuln3-32 exploit.bin
```

edit `command.txt` to declare an arbitrary command.
