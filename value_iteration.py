import copy 
import sys

def updateValue(i, j, action, V):
	x = i+action[0]
	y = j+action[1]
	if (x,y) in V:
		return V[(x,y)]

	return None

# maze_input = "tiny_maze.txt"
# value_file = "value_output.txt"
# q_value_file = "q_value_output.txt"
# policy_file = "policy_output.txt"
# num_epoch = 5
# discount_factor = 0.9

#python value_iteration.py "tiny_maze.txt" "value_output.txt" "q_value_output.txt" "policy_output.txt" 5 0.9

maze_input = sys.argv[1]
value_file = sys.argv[2]
q_value_file = sys.argv[3]
policy_file = sys.argv[4]
num_epoch = int(sys.argv[5])
discount_factor = float(sys.argv[6])

maze = []
step_reward = -1

with open(maze_input, "r") as f:
	row = f.readline()
	while row:
		row = row.strip("\n")
		maze.append(list(row))
		row = f.readline()

V = {}
goal = (-1, -1)
for i in range(len(maze)):
	for j in range(len(maze[0])):
		if maze[i][j] != "*":
			V[(i,j)] = 0
		if maze[i][j] == "G":
			goal = (i,j)


actions = [(0,-1), (-1,0), (0,1), (1,0)]

newV = copy.deepcopy(V)
for e in range(num_epoch):
	for s in newV:
		if s == goal:
			continue

		maxNeighbor = float("-Inf")
		for i in range(len(actions)):
			val = updateValue(s[0], s[1], actions[i], V)
			if val is not None and maxNeighbor < val:
				maxNeighbor = val

		newV[s] = step_reward + discount_factor * maxNeighbor
	V = copy.deepcopy(newV)

q_table = {}
for s in V:
	for i in range(len(actions)):
		s_hat = (s[0]+actions[i][0], s[1]+actions[i][1])
		if s == goal:
			q_table[(s[0], s[1], i)] = 0.0
		elif s_hat not in V:
			q_table[(s[0], s[1], i)] = step_reward + discount_factor * V[s]
		else:
			q_table[(s[0], s[1], i)] = step_reward + discount_factor * V[s_hat]

# for s in q_table:
# 	print s, q_table[s]

policy = {}

for s in V:
	max_action = 0
	max_q = float("-Inf")
	for i in range(len(actions)):
		if max_q < q_table[(s[0], s[1], i)]:
			max_q = q_table[(s[0], s[1], i)]
			max_action = i

	V[s] = max_q
	policy[s] = max_action

with open(value_file, "w") as f:
	for s in V:
		res = str(s[0]) + " " + str(s[1]) + " " + str(V[s]) + "\n"
		f.write(res)
with open(q_value_file, "w") as f:
	for s in q_table:
		res = str(s[0]) + " " + str(s[1]) + " " + str(s[2]) + " " + str(q_table[s]) + "\n"
		f.write(res)

with open(policy_file, "w") as f:
	for s in policy:
		res = str(s[0]) + " " + str(s[1]) + " " + str(policy[s]) + "\n"
		f.write(res)

