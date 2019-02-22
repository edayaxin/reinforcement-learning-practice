import random
import sys

class environment:
	
	def __init__(self, filename):
		self.filename = filename
		self.step_reward = -1
		self.goal_reward = 0

		maze = []
		with open(filename, "r") as f:
			row = f.readline()
			while row:
				row = row.strip("\n")
				maze.append(list(row))
				row = f.readline()

		self.V = {}
		self.goal = (-1, -1)
		for i in range(len(maze)):
			for j in range(len(maze[0])):
				if maze[i][j] != "*":
					self.V[(i,j)] = 0
				if maze[i][j] == "G":
					self.goal = (i,j)
				if maze[i][j] == "S":
					self.init_state = (i,j) 

		self.cur_state = self.init_state

	def step(self, a):

		if self.cur_state == self.goal:
			return self.cur_state, self.goal_reward, 1 

		next_state = (self.cur_state[0] + a[0], self.cur_state[1] + a[1])
		next_state = self.cur_state if (next_state not in self.V) else next_state
		self.cur_state = next_state

		reward = self.step_reward 
		is_terminal = 1 if next_state == self.goal else 0

		return next_state, reward, is_terminal

	def reset(self):
		self.cur_state = self.init_state
		return self.init_state

def get_max_q_neighbor(x, y, q, actions = [(0,-1), (-1,0), (0,1), (1,0)]):

	action = 0
	max_q = q[(x, y, action)]

	for i in range(len(actions)):
		if max_q < q[(x, y, i)]:
			max_q = q[(x, y, i)]
			action = i
	return action, max_q


# maze_input = "tiny_maze.txt"
# value_file = "value_output.txt"
# q_value_file = "q_value_output.txt"
# policy_file = "policy_output.txt"
# num_episode = 1000
# max_episode_length = 20
# learning_rate = 0.8
# discount_factor = 0.9
# epsilon = 0.05

# python q_learning.py tiny_maze.txt value_output.txt q_value_output.txt policy_output.txt 1000 20 0.8 0.9 0.05

maze_input = sys.argv[1]
value_file = sys.argv[2]
q_value_file = sys.argv[3]
policy_file = sys.argv[4]
num_episode = int(sys.argv[5])
max_episode_length = int(sys.argv[6])
learning_rate = float(sys.argv[7])
discount_factor = float(sys.argv[8])
epsilon = float(sys.argv[9])

terminal_true = 1
terminal_false = 0
maze_solver = environment(maze_input)
actions = [(0,-1), (-1,0), (0,1), (1,0)]

q_table = {}
for s in maze_solver.V:
	for i in range(len(actions)):
		q_table[(s[0], s[1], i)] = 0.0

for episode_i in range(num_episode):

	episode_length = max_episode_length
	is_terminal = terminal_false

	while episode_length > 0:

		x, y = maze_solver.cur_state[0], maze_solver.cur_state[1]

		det_action, q_next = get_max_q_neighbor(x, y, q_table)

		if random.random() <= 1 - epsilon:
			action = det_action
		else:
			action = random.randint(0, 3)

		next_state, reward, is_terminal = maze_solver.step(actions[action])

		x_next, y_next = next_state[0], next_state[1]
		action_next, q_max_next = get_max_q_neighbor(x_next, y_next, q_table)

		q_table[(x,y,action)] = (1-learning_rate)*q_table[(x,y,action)] + learning_rate*(reward + discount_factor*q_max_next)
		
		episode_length -= 1
		if is_terminal == terminal_true:
			break

	maze_solver.reset()

policy = {}
V = maze_solver.V
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



