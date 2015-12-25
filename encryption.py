import numpy as np
import calc as calc

def encrypt(state,S_box,keys):
	global keywords, Sbox
	keywords = keys
	Sbox = S_box
	state = AddRoundKey(state,0)	
	for i in range(1,10):
		state = SubBytes(state)
		state = ShiftRows(state)
		state = MixColumns(state)
		state = AddRoundKey(state,i)	
	state = SubBytes(state)
	state = ShiftRows(state)
	return AddRoundKey(state,10)

def SubBytes(state):
	for i in range(4):
		for j in range(4):
			state[i][j] = Sbox[(state[i][j] & 0xf0) >> 4][state[i][j] & 0x0f] 
			
	return state

def MixColumns(state):
	StateArray_mixed =[[0 for j in range(4)] for i in range(4)]
	a = np.array([2,3,1,1])
	for i in range(4):
		for j in range(4):
			StateArray_mixed[i][j] = calc.mod_GF2(calc.mul_GF2(state[i][0],a[0])) ^ calc.mod_GF2(calc.mul_GF2(state[i][1],a[1])) ^ calc.mod_GF2(calc.mul_GF2(state[i][2],a[2])) ^ calc.mod_GF2(calc.mul_GF2(state[i][3],a[3]))
			a = np.roll(a,1)
 
	return StateArray_mixed
	
def ShiftRows(state):
	npArray = np.array(state).T
	for i in range(4):
		npArray[i] = np.roll(npArray[i],-i)
		
	return npArray.T.tolist()

	
def AddRoundKey(state,round):
	for i in range(4):
		for j in range(4):
			state[i][j] = state[i][j] ^ keywords[round*4:(round*4)+4][i][j]
			
	return state