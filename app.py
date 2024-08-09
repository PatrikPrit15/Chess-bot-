import tkinter as tk
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
	if pole[7][4][0]!=6:rbl,rbp=1,0
	if pole[7][0][0]!=4:rbl=0
	if pole[7][7][0]!=4:rbp=0
	if pole[0][4][0]!=12:rcl,rcp=0,0
	if pole[0][0][0]!=10:rcl=0
	if pole[0][7][0]!=10:rcp=0
	if 0<pole[sur[1]][sur[0]][0]<7 and 0<pole[y][x][0]<7 or pole[sur[1]][sur[0]][0]>6 and pole[y][x][0]>6: #nie su rovnaka farba
		return 0

	if pole[sur[1]][sur[0]][0]==1:#biely pesiak
		if sur[1]-y>=0:
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
		elif sur[1]+y>1:
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
		h,v=1 if x-sur[0]>0 else 1,-1 if y-sur[1]>0 else -1
		for i in range(1,10):
			if sur[0]+h*i==x and sur[1]+v*i==y:
				break
			if pole[sur[1]+v*i][sur[0]+h*i][0]!=0:
				return 0
