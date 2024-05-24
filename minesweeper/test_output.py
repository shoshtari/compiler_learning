bombs = [[0 for y in range(80)] for x in range(5)]
def new_bomb(x, y):
	bombs[x][y] = 'x'
	for i in range(x-1, x + 2):
		for j in range(y-1, y+2):
			if i < 0 or j < 0 or i >= len(bombs) or j >= len(bombs[0]) or  bombs[i][j] == 'x' :
				continue
			bombs[i][j] += 1
new_bomb(0, 1)
new_bomb(3, 5)
new_bomb(4, 7)
for row in bombs:
	for column in row:
		if column == 'x':
			print('*', end ='')
		else:
			symbol = '#' if column == 0 else column
			print(symbol, end ='')
	print()