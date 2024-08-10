import matplotlib.pyplot as plt
import tkinter as tk
import neat
# nic-0, pesiakb-1, konb-2, strelecb-3, vezab-4, kralovnab-5, kralb-6,pesiakc-7, konc-8, strelecc-9, vezac-10, kralovnac-11, kralc-12


def define_board():
	global pole, sur, empasant, rbl, rbp, rcl, rcp, last_move
	last_move = 50
	pole = [
		[[10, 0], [8, 0], [9, 0], [11, 0], [12, 0], [9, 0], [8, 0], [10, 0]],
		[[7, 0] for _ in range(8)],
		[[0, 0] for _ in range(8)],
		[[0, 0] for _ in range(8)],
		[[0, 0] for _ in range(8)],
		[[0, 0] for _ in range(8)],
		[[1, 0] for _ in range(8)],
		[[4, 0], [2, 0], [3, 0], [5, 0], [6, 0], [3, 0], [2, 0], [4, 0]]
	]
	sur = [-1, -1]
	empasant = [-1, -1]
	rbl, rbp, rcl, rcp = 0, 0, 0, 0


def validator(y,x):
	global rbl,rbp,rcl,rcp,pole,empasant
	if pole[7][4][0]!=6:rbl,rbp=0,0
	if pole[7][0][0]!=4:rbl=0
	if pole[7][7][0]!=4:rbp=0
	if pole[0][4][0]!=12:rcl,rcp=0,0
	if pole[0][0][0]!=10:rcl=0
	if pole[0][7][0]!=10:rcp=0
	if 0<pole[sur[1]][sur[0]][0]<7 and 0<pole[y][x][0]<7 or pole[sur[1]][sur[0]][0]>6 and pole[y][x][0]>6: #nie su rovnaka farba
		return 0

	if pole[sur[1]][sur[0]][0]==1:#biely pesiak
		if sur[1]-y<=0:
			return 0
		if sur[0]==x:
			if pole[y][x][0]!=0 or pole[max(0,sur[1]-1)][sur[0]][0]!=0:
				return 0
			if sur[1]-y>1 and sur[1]!=6:
				return 0
			if sur[1]-y>2:
				return 0
			if sur[1]-y==2:
				empasant=[x,y+1]
				return 1
		elif sur[1]-y>1:
			return 0
		elif abs(sur[0]-x)>1:
			return 0
		if sur[0]!=x and (pole[y][x][0]==0 and (y!=empasant[1] and x!=empasant[0])):
			return 0
		if (y==empasant[1] and x==empasant[0]):
			pole[empasant[1]+1][empasant[0]][0]=0
		if y==0:
			pole[sur[1]][sur[0]][0]=5

	if pole[sur[1]][sur[0]][0]==7:#cierny pesiak
		if y-sur[1]<=0:
			return 0
		if sur[0]==x:
			if pole[y][x][0]!=0 or pole[min(7,sur[1]+1)][sur[0]][0]!=0:
				return 0
			if y-sur[1]>1 and sur[1]!=1:
				return 0
			if y-sur[1]>2:
				return 0
			if y-sur[1]==2:
				empasant=[x,y-1]
				return 1
		elif y-sur[1]>1:
			return 0
		elif abs(sur[0]-x)>1:
			return 0
		if sur[0]!=x and (pole[y][x][0]==0 and y!=empasant[1] and x!=empasant[0]):
			return 0
		if (y==empasant[1] and x==empasant[0]):
			pole[empasant[1]-1][empasant[0]][0]=0
		if y == 7:
			pole[sur[1]][sur[0]][0] = 11


	empasant=[-1,-1]
	if pole[sur[1]][sur[0]][0] in [2, 8]: #kon
		if abs(x - sur[0]) != 1 or abs(y - sur[1]) != 2:
			if abs(x - sur[0]) != 2 or abs(y - sur[1]) != 1: 
				return 0

	if pole[sur[1]][sur[0]][0] in [3,9]:#strelec
		if abs(x-sur[0])!=abs(y-sur[1]):
			return 0
		h,v=1 if x-sur[0]>0 else -1,1 if y-sur[1]>0 else -1
		for i in range(1,10):
			if sur[0]+h*i==x and sur[1]+v*i==y:
				break
			if pole[sur[1]+v*i][sur[0]+h*i][0]!=0:
				return 0

	if pole[sur[1]][sur[0]][0] in [4,10]:#veza
		if x==sur[0] and y!=sur[1]:
			if any(pole[i][x][0]!=0 for i in range(min(y, sur[1]) + 1, max(y, sur[1]))):
				return 0
		elif x!=sur[0] and y==sur[1]:
			if any(pole[y][i][0]!=0 for i in range(min(x, sur[0]) + 1, max(x, sur[0]))):
				return 0
		else:
			return 0

	if pole[sur[1]][sur[0]][0] in [5,11]:#kralovna
		if abs(x - sur[0]) == abs(y - sur[1]):#je strelec
			h,v=1 if x-sur[0]>0 else -1, 1 if y-sur[1]>0 else -1 
			for i in range(1,10):
				if sur[0]+h*i==x and sur[1]+v*i==y:
					break
				if pole[sur[1]+v*i][sur[0]+h*i][0]!=0:
					return 0

		elif x==sur[0] and y!=sur[1]: #je veza
			if any(pole[i][x][0] != 0 for i in range(min(y, sur[1]) + 1, max(y, sur[1]))):
				return 0
		elif x!=sur[0] and y==sur[1]:
			if any(pole[y][i][0] != 0 for i in range(min(x, sur[0]) + 1, max(x, sur[0]))):
				return 0
		else:
			return 0

	if pole[sur[1]][sur[0]][0]==6:#kralb
		if abs(y-sur[1])>1 or abs(x-sur[0])>1:
			if y-sur[1]!=0:
				return 0
			if rbl==0 and rbp==0:
				return 0
			if abs(x-sur[0])!=2:
				return 0
			if x>sur[0]:
				if not rbp or any([pole[7][i][0]!=0 for i in range(5,7)]):
					return 0
				pole[7][7][0]=0
				pole[7][5][0]=4
			else:
				if not rbl or any([pole[7][i][0]!=0 for i in range(1,4)]):
					return 0
				pole[7][0][0]=0
				pole[7][3][0]=4

	if pole[sur[1]][sur[0]][0]==12:#kralc
		if abs(y-sur[1])>1 or abs(x-sur[0])>1:
			if y-sur[1]!=0:
				return 0
			if rcl==0 and rcp==0:
				return 0
			if abs(x-sur[0])!=2:
				return 0
			if x>sur[0]:
				if not rcp or any([pole[0][i][0]!=0 for i in range(5,7)]):
					return 0
				pole[0][7][0]=0
				pole[0][5][0]=10
			else:
				if not rcl or any([pole[0][i][0]!=0 for i in range(1,4)]):
					return 0
				pole[0][0][0]=0
				pole[0][3][0]=10

	return 1


max_counter = 0


def eval_genomes(genomes, config):
	global gen, pole, sur, max_counter
	gen += 1
	# start by creating lists holding the genome itself, the
	# neural network associated with the genome
	nets = []
	ge = []
	for genome_id, genome in genomes:
		genome.fitness = 0  # start with fitness level of 0
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		nets.append(net)
		ge.append(genome)

	lmax_counter = 0
	for index1 in range(30):
		for index2 in range(1):
			if index1 == index2:
				continue
			counter = 0
			define_board()
			while last_move > 0:
				pole_bool = tuple(pos == elem for pole_pos in pole for pos, _ in pole_pos for elem in [
								  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
				output = nets[index1].activate(pole_bool)
				sur = [output[:64].index(max(output[:64])) %
					   8, output[:64].index(max(output[:64]))//8]
				if pole[sur[1]][sur[0]][0] == 0 or pole[sur[1]][sur[0]][0] > 6 or [output[64:].index(max(output[64:])) % 8, output[64:].index(max(output[64:]))//8] == [sur[0], sur[1]] or not(validator(output[64:].index(max(output[64:])) // 8, output[64:].index(max(output[64:]))%8)):
					ge[index1].fitness -= 1
					ge[index2].fitness += 0.5
					break
				pole[output[64:].index(max(output[64:])) % 8][output[64:].index(
					max(output[64:]))//8][0] = pole[sur[1]][sur[0]][0]
				pole[sur[1]][sur[0]][0] = 0
				counter += 1
				if all(e != 12 for p in pole for e, _ in p):
					ge[index1].fitness += 1

				pole_bool = tuple(pos == elem for pole_pos in pole[::-1] for pos, _ in pole_pos[::-1] for elem in [
								  0, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6])
				output = nets[index2].activate(pole_bool)
				sur = [output[:64].index(max(output[:64])) %
					   8, output[:64].index(max(output[:64]))//8]
				if pole[sur[1]][sur[0]][0] == 0 or pole[sur[1]][sur[0]][0] <= 6 or [output[64:].index(max(output[64:])) % 8,output[64:].index(max(output[64:]))//8] == [sur[1],sur[0]] or not(validator(output[64:].index(max(output[64:])) % 8, output[64:].index(max(output[64:]))//8)):
					ge[index1].fitness += 0.5
					ge[index2].fitness -= 1
					break
				counter += 1
				pole[output[64:].index(max(output[64:])) % 8][output[64:].index(
					max(output[64:]))//8][0] = pole[sur[1]][sur[0]][0]
				pole[sur[1]][sur[0]][0] = 0
				if all(e != 6 for p in pole for e, _ in p):
					ge[index2].fitness += 1
			else:
				ge[index1].fitness += 0.5
				ge[index2].fitness += 0.5
			lmax_counter = max(counter, lmax_counter)
			print('lmax tahov: ', lmax_counter)
	# plt.plot(pole_counterov)
	# plt.show()
	if lmax_counter > max_counter:
    		print(pole)
		max_counter = counter
	max_counter = max(max_counter, lmax_counter)
	print('max tahov: ', max_counter)


config_file = "config-feedforward.txt"
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
							neat.DefaultSpeciesSet, neat.DefaultStagnation,
							config_file)
# Create the population, which is the top-level object for a NEAT run.
p = neat.Population(config)
gen = 0
# Add a stdout reporter to show progress in the terminal.
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
# p.add_reporter(neat.Checkpointer(5))

# Run for up to 50 generations.
winner = p.run(eval_genomes, 50)

# show final stats
print('\nBest genome:\n{!s}'.format(winner))
