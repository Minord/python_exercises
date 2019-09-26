import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import random


def FindOnes(matrix):
	heigth, width = matrix.shape

	ones_directions = []

	for x in range(width):
		for y in range(heigth):
			if(matrix[y,x] == 1):
				ones_directions.append((y,x))
	return ones_directions

def changeState(matrix, directions):
	for cord in directions:
		print('pass for here')
		matrix[cord] = 1
		matrix[cord[0], cord[1]] = 1

	return matrix



def update(data):
	adress = FindOnes(data)

	return changeState(data, adress)

#now it works
def gameloop():
	grid_space = np.zeros((64,64))
	grid_space[32,32] = 1

	fig = plt.figure()
	im = plt.imshow(grid_space)

	def init():
		im.set_data(grid_space)

	def animate(i):
		im.set_data(update(grid_space))
		return im


	anim = animation.FuncAnimation(fig, animate, init_func=init, frames=100,
                               interval=50)

	plt.show()
		

if __name__ == "__main__":                           
	gameloop()                              
	                                     