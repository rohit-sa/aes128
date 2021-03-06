# Start of Code

import numpy as np
import calc as calc
import encryption as en
import decryption as de
import struct


def outBinFile(state,path):
	outputFileHandle = open(path,'ab')
	for i in state:
		outputFileHandle.write(struct.pack('B',i))
	
def inBinFile(path):
	with open(path,'rb') as inputFileHandle:
		inData = inputFileHandle.read()
	hexData =[]
	inputFileHandle.close()
	for sublist in list(inData):
		for i in sublist:
			hexData.append(struct.unpack('B',i))
	
	cipher = []
	cipherText = raw_input("16 byte cipher: ")
	for i in list(cipherText[:16]):
		cipher.append(ord(i))
	return (hexData, cipher)	
	
def outTextFile(state,path):
	outputFileHandle = open(path,'a')
	for i in state:
		outputFileHandle.write(chr(i))
	
def inPlainTextFile(path):
	with open(path,'r') as inputFileHandle:
		inData = inputFileHandle.read()
	hexData =[]
	inputFileHandle.close()
	
	for sublist in list(inData):
		for i in sublist:
			hexData.append(ord(i))

	while (len(hexData) % 16) != 0:
		hexData.append(32)
	cipher = []
	cipherText = raw_input("16 byte cipher: ")
	for i in list(cipherText[:16]):
		cipher.append(ord(i))
	return (hexData, cipher)

	
def g(inData,round):
	outData = inData[1:]
	outData.append(inData[0])
	for i in range(4):
		outData[i] = S_box[(outData[i] & 0xf0) >> 4][outData[i] & 0x0f] 
	outData[0] = outData[0] ^ calc.mod_GF2(1 << (round-1))
	return outData

	
def keyExpansion_G(inputWord):
	word = inputWord
	for i in range(0,40,4):
			word.append(calc.add_GF2(word[i],g(word[i+3],(i+4)/4)))
			word.append(calc.add_GF2(word[i+4],word[i+1]))
			word.append(calc.add_GF2(word[i+5],word[i+2]))
			word.append(calc.add_GF2(word[i+6],word[i+3]))

	return word 

def genTables():
	SBox = [[0 for j in range(16)] for i in range(16)] 
	inv_SBox = [[0 for j in range(16)] for i in range(16)] 
	tableList = [[0 for j in range(16)] for i in range(16)] 
	for i in range(16):
		for j in range(16): 
			SBox[i][j] = (i<<4) | j
			inv_SBox[i][j] = (i<<4) | j

	for i in range(16):
		for j in range(16):
			inv_SBox[i][j] = calc.bit_scrb(inv_SBox[i][j],'decrypt')		
			if SBox[i][j] != 0:
				SBox[i][j] = calc.mulInv_GF2(SBox[i][j])
			else:
				SBox[i][j] = 0
			if inv_SBox[i][j] != 0:
				inv_SBox[i][j] = calc.mulInv_GF2(inv_SBox[i][j])
			else:
				inv_SBox[i][j] = 0
			SBox[i][j] = calc.bit_scrb(SBox[i][j],'encrypt')

	return (SBox, inv_SBox)

def main():
	StateArray = []
	choice = raw_input("1.Encrypt\n2.Decrypt\nEnter 1 or 2: ")
	inpath = raw_input("Enter inpath: ")
	outpath = raw_input("Enter outpath: ")
	if choice == '1':
		(inputText,cipherKey) = inPlainTextFile(inpath)	
	else:
		(inputText,cipherKey) = inBinFile(inpath)	

	if(len(cipherKey) < 16):
		cipherKey = cipherKey + [0 for i in range(16 - len(cipherKey))]
	else:
		cipherKey = cipherKey[:16]
		
	cipherKeyArray = np.asarray(cipherKey).reshape(4,4).T
	keyWord = []
	keyWord = cipherKeyArray.T.tolist()
	global S_box, inv_S_box
	(S_box, inv_S_box) = genTables()
	keys = keyExpansion_G(keyWord)
	for i in range(len(inputText)/16):
		StateArray = np.asarray(inputText[16*i:16*(i+1)]).reshape(4,4).tolist()
		if choice == '1':
			StateArray = en.encrypt(StateArray,S_box,keys)
			npArray = np.array(StateArray).T.tolist()
			out = [value for rows in npArray for value in rows]
			outBinFile(out,outpath)
		else:
			StateArray = np.array(StateArray).T.tolist()
			StateArray = de.decrypt(StateArray,inv_S_box,keys)
			npArray = np.array(StateArray).tolist()
			out = [value for rows in npArray for value in rows]
			outTextFile(out,outpath)
	return 0;

if __name__ == "__main__":
	if(main() == 0):
		print("Execution sucessful")
	else:
		print("Fail")	

	
