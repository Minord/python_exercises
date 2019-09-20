
#bueno voy a implementar unos decorators
import numpy as np
import matplotlib.pyplot as plt
import time


#test decorators

def decorator(func):
	def wrapper(*args, **kwargs):
		print('before')
		func(*args, **kwargs)
		print('after')
	return wrapper

def helloWorld(more_text):
	print('hello world' + more_text)

helloWorld = decorator(helloWorld)

#helloWorld(', and bye cruel world')

#ok it work

def inAll(data, func):
	for x in range(len(data)):
		data[x] = func(data[x])
	return data


def perTwo(data):
	return data * 2

def inv(data):
	return 1 / data

data = [3,5,2,2,3,5,6,6,3]

print(data)
print(inAll(data, perTwo))
print(inAll(data, inv))

#yeah it work

matrix = np.zeros((16, 16))

def per_cords(matrix, func):
	heigth, width = matrix.shape
	for x in range(width):
		for y in range(heigth):
			matrix[y, x] = func((x,y))
	return matrix

def cordMul(cords):
	return cords[0] * cords[1]

#plt.imshow(matrix)
#plt.show()
print('operate in matrix')

init_time = time.time()

#actually this is most fast what i spected
for i in range(1000):
	matrix = per_cords(matrix, cordMul)


final_time = time.time() - init_time
print(f'it takes {final_time} seconds')

#plt.imshow(matrix)
#plt.show()

bench_time = True


#yeah it works
def checktime(func):
	def wrapper(*args, **kwargs):
		if bench_time:
			init_time = time.time()
			func(*args, **kwargs)
			final_time = time.time() - init_time
			print(f'it takes {final_time} seconds')
		else:
			return func(*args, **kwargs)
	return wrapper

@checktime
def helloWorld(times):
	for x in range(times):
		print('hello world dsfgsdgsdfgdsfgdsgdsfgdsfdfgsdfgsdfgdsfg')


helloWorld(1000)