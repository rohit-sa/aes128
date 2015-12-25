import numpy as np
import calc as calc

def decrypt(state,S_box,keys):
	global keywords, inv_Sbox
	keywords = keys
	inv_Sbox = S_box
	state = AddRoundKey(state,10)
	for i in range(9,0,-1):
		state = InvShiftRows(state)
		state = InvSubBytes(state)
		state = AddRoundKey(state,i)
		state = InvMixColumns(state)
	state = InvShiftRows(state)
	state = InvSubBytes(state)
	return AddRoundKey(state,0)

def InvSubBytes(state):
	for i in range(4):
		for j in range(4):
			state[i][j] = inv_Sbox[(state[i][j] & 0xf0) >> 4][state[i][j] & 0x0f] 
			
	return state

def InvMixColumns(state):
	StateArray_mixed =[[0 for j in range(4)] for i in range(4)]
	a = np.array([14,11,13,9])
	for i in range(4):
		for j in range(4):
			StateArray_mixed[i][j] = calc.mod_GF2(calc.mul_GF2(state[i][0],a[0])) ^ calc.mod_GF2(calc.mul_GF2(state[i][1],a[1])) ^ calc.mod_GF2(calc.mul_GF2(state[i][2],a[2])) ^ calc.mod_GF2(calc.mul_GF2(state[i][3],a[3]))
			a = np.roll(a,1)
 
	return StateArray_mixed
	
def InvShiftRows(state):
	npArray = np.array(state).T
	for i in range(4):
		npArray[i] = np.roll(npArray[i],i)
		
	return npArray.T.tolist()

	
def AddRoundKey(state,round):
	for i in range(4):
		for j in range(4):
			state[i][j] = state[i][j] ^ keywords[round*4:(round*4)+4][i][j]
			
	return state