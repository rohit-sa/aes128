<<<<<<< HEAD
import collections

def	arrayBits(exp):
	count = exp.bit_length()
	bit_pos = []
	bit_exp = bin(exp)[2:(2+exp.bit_length())]
	for bit in bit_exp:
		count = count - 1
		if bit == '1':
			bit_pos.append(count)
	return bit_pos
	
def div_GF2(m ,n):
	if n == 1:
		return (m,n)
	else:
		q = 1 << (arrayBits(m)[0] - arrayBits(n)[0])
		r = m ^ (n << (arrayBits(m)[0] - arrayBits(n)[0]))
		while (arrayBits(r)[0]) >= (arrayBits(n)[0]):
			q = q ^ (1 << (arrayBits(r)[0] - arrayBits(n)[0]))
			r = r ^ (n << (arrayBits(r)[0] - arrayBits(n)[0]))
		return (q,r)
	
def mul_GF2(q, x):
	p = 0
	for i in arrayBits(q):
		p = p ^ (x << i)
	return p

def mulInv_GF2(y):
	x = [[0 for j in range(3)] for i in range(20)] 
	x[0][0] = 0x11B
	x[1][0] = y
	x[1][1] = 1
	x[0][2] = 1
	rem = 0
	i = 0
	while x[i+1][0] != 1:
		for j in range(0,3):
				(quo,rem) = div_GF2(x[i][0],x[i+1][0])
				x[i+2][j] = x[i][j] ^ mul_GF2(quo, x[i+1][j])
		i = i + 1

	x = x[:i+2]			
	return x[i+1][1]
	
def bit_scramble(b):
	x = [[0 for j in range(8)] for i in range(8)] 
	
=======
import collections

def	arrayBits(exp):
	count = exp.bit_length()
	bit_pos = []
	bit_exp = bin(exp)[2:(2+exp.bit_length())]
	for bit in bit_exp:
		count = count - 1
		if bit == '1':
			bit_pos.append(count)
	return bit_pos
	
def div_GF2(m ,n):
	if n == 1:
		return (m,n)
	else:
		q = 1 << (arrayBits(m)[0] - arrayBits(n)[0])
		r = m ^ (n << (arrayBits(m)[0] - arrayBits(n)[0]))
		while (arrayBits(r)[0]) >= (arrayBits(n)[0]):
			q = q ^ (1 << (arrayBits(r)[0] - arrayBits(n)[0]))
			r = r ^ (n << (arrayBits(r)[0] - arrayBits(n)[0]))
		return (q,r)
	
def mul_GF2(q, x):
	p = 0
	for i in arrayBits(q):
		p = p ^ (x << i)
	return p

def mulInv_GF2(y):
	x = [[0 for j in range(3)] for i in range(20)] 
	x[0][0] = 0x11B
	x[1][0] = y
	x[1][1] = 1
	x[0][2] = 1
	rem = 0
	i = 0
	while x[i+1][0] != 1:
		for j in range(0,3):
				(quo,rem) = div_GF2(x[i][0],x[i+1][0])
				x[i+2][j] = x[i][j] ^ mul_GF2(quo, x[i+1][j])
		i = i + 1

	x = x[:i+2]			
	return x[i+1][1]
	
def bit_scramble(b):
	x = [[0 for j in range(8)] for i in range(8)] 
	
>>>>>>> 555743d7d1f7d385591ae97dfe0ad573c39045ce
