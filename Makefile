.DEFAULT_GOAL := vuln3

vuln3:
	gcc -fno-stack-protector -m32 -static vuln3.c -o vuln3-32
