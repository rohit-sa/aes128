#input a file with characters output bin file ?
#store the charaters into state array only 16 bytes at a time
#abcdefghijklmnop =>[('a','e','i','m'),('b','f','j','n'),('c','g','k','o'),('d','h','l','p')] but in hex
	
# Start of Code

import numpy as np
import calc as calc
path = 'C:\Users\RSA\Desktop\Coding\Python Projects\AES\in.txt'
with open(path,'r') as inputFileHandle:
	inData = inputFileHandle.read(16)

hexData =[]

for i in list(inData):
	hexData.append(i.encode('hex'))
	
StateArray = np.asarray(hexData).reshape(4,4).T

keyWord = []
keyWord = StateArray.T

def keyExpansion_G(inputWord):
	inputWord = inputWord << 8
	

def genTables():
	tableList = [[0 for j in range(16)] for i in range(16)] 
	for i in range(16):
		for j in range(16): 
			tableList[i][j] = (i<<4) | j

	for i in range(16):
		for j in range(16): 
			if tableList[i][j] != 0:
				tableList[i][j] = calc.mulInv_GF2(tableList[i][j])
			else:
				tableList[i][j] = 0
	
	
	print tableList	


genTables()