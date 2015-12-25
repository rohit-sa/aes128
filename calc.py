import collections

rol = lambda val, i: \
    (val << i%8) & (0xff) | \
    ((val & 0xff) >> (8-(i%8)))
	
ror = lambda val, i: \
    ((val & (0xff)) >> i%8) | \
    (val << (8-(i%8)) & (0xff))

def	arrayBits(exp):
	count = exp.bit_length()
	bit_pos = []
	bit_exp = bin(exp)[2:(2+exp.bit_length())]
	for bit in bit_exp:
		count = count - 1
		if bit == '1':
			bit_pos.append(count)
	return bit_pos
	

def add_GF2(word1, word2):
	sum = []
	for i,j in zip(word1,word2):
		sum.append(i^j)
	return sum
	
	
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

def mod_GF2(x):
	if x == 0:
		return 0
	else:
		while (arrayBits(x)[0]) >= 8:
			x = x ^ (0x11b << (arrayBits(x)[0]) - 8)
		return x
	
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
	
def count_ones(n):
	c = 0
	while n !=0:
		c = c +1
		n = n & (n-1)
	if c % 2 == 0:
		return 0
	else:
		return 1

def bit_scrb(b,op):
	b_scram = 0
	if op is 'encrypt':
		for i in range(8):
			b_scram |= (count_ones((rol(241,i)) & b) ^ ((0x63 >> i) & 1)) << i
	else:
		for i in range(8):
			b_scram |= (count_ones((rol(164,i)) & b) ^ ((0x05 >> i) & 1)) << i
	
	return b_scram

