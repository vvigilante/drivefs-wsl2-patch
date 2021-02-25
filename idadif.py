#!/usr/bin/env python
# Small IDA .dif patcher
import re
from sys import argv,exit

def patch(file, dif, revert=False):
	code = open(file,'rb').read()
	dif = open(dif,'r').read()
	m = re.findall('([0-9a-fA-F]+): ([0-9a-fA-F]+) ([0-9a-fA-F]+)', dif)
	for offset,orig,new in m:
		o, orig, new = int(offset,16), bytearray.fromhex(orig), bytearray.fromhex(new)
		if revert:
			if code[o]==new[0]:
				code = code[:o]+orig+code[o+1:]
				print("Reverted location %s (%02X <- %02X)"% (offset, orig[0], new[0]))
			else:
				if code[o] == orig[0]:
					print("Location %s is already at its original state (orig: %02X, patched: %02X, current: %02X)"% (offset, orig[0], new[0], code[o]))
				else:
					raise Exception("patched byte at %s is not %02X" % (offset, ord(new)))
		else:
			if code[o]==orig[0]:
				code = code[:o]+new+code[o+1:]
				print("Patched location %s (%02X -> %02X)"% (offset, orig[0], new[0]))
			else:
				#print(type(offset),offset)
				#print(type(orig[0]),orig[0])
				#print(type(code[o]),code[o])
				if code[o] == new[0]:
					print("Location %s is already patched (orig: %02X, patched: %02X, current: %02X)"% (offset, orig[0], new[0], code[o]))
				else:
					raise Exception( "original byte at %s is not %02X, it is %02X" % (offset, orig[0], code[o]) )
	open(file,'wb').write(code)

def main():
	if len(argv)<3:
		print( "Usage: %s <binary> <IDA.dif file> [revert]" % (argv[0]))
		print( "Applies given IDA .dif file to patch binary; use revert to revert patch.")
		exit(0)
	
	file, dif, revert = argv[1], argv[2], False
	if len(argv)>3:
		revert = True
		print( "Reverting patch %r on file %r" % (dif, file))
	else:
		print( "Patching file %r with %r" % (file, dif))
	
	try:
		patch(file, dif, revert)
		print( "Done")
	except Exception as e:
		print( "Error: %s" % str(e))
		#raise e
		exit(1)

if __name__ == "__main__":
	main()
