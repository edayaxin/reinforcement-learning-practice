import sys

class environment:
	
	def __init__(self, filename):
		self.filename = filename
		self.step_reward = -1

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
					self.end_state = (i,j)
				if maze[i][j] == "S":
					self.init_state = (i,j) 

		self.cur_state = self.init_state

	def step(self, a):

		if self.cur_state == self.end_state:
			return self.cur_state, 0, 1 

		next_state = (self.cur_state[0] + a[0], self.cur_state[1] + a[1])
		next_state = self.cur_state if (next_state not in self.V) else next_state
		self.cur_state = next_state

		reward = self.step_reward 
		is_terminal = 1 if next_state == self.goal else 0

		return next_state, reward, is_terminal

	def reset(self):
		self.cur_state = self.init_state
		return self.init_state

# maze_input = "medium_maze.txt"
# output_file = "output.feedback"
# action_seq_file = "medium_maze_action_seq.txt"
maze_input = sys.argv[1]
output_file = sys.argv[2]
action_seq_file = sys.argv[3]

actions = [(0,-1), (-1,0), (0,1), (1,0)]

maze_solver = environment(maze_input)

with open(action_seq_file, "r") as f:
	action_seq = f.readline().strip().split(" ")
	action_seq = [int(e) for e in action_seq]

with open(output_file, "w") as f:
	for i in action_seq:
		next_state, reward, is_terminal = maze_solver.step(actions[i])
		res = str(next_state[0]) + " " + str(next_state[1]) + " " + str(reward) + " " + str(is_terminal) + "\n"
		f.write(res) 










