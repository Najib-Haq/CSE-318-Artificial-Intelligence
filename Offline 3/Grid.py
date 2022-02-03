import numpy as np

from Ghost import Ghost
from Sensor import Sensor

class Grid:
    def __init__(self, i, j, obstacles=[]):
        '''
        i, j = width, height of grid
        obstacles = list of (x, y) position of obstacles
        '''
        self.rows = i
        self.cols = j
        self.cells_wo_obstacles = (i*j)-len(obstacles)
        # initialize cell with 1/working_cells probability value and 0 for obstacles
        self.grid = np.full(shape=(i, j), fill_value=(1/self.cells_wo_obstacles))
        for ob in obstacles:
            self.grid[ob[0]][ob[1]] = 0

        self.ghost = Ghost(self.grid)
        self.sensor = Sensor(i, j)
        self.time_step = 0


    def show_grid(self):
        for i in range(self.rows):
            print("    |" + "-"*9*self.cols)
            print(f"{str(i).rjust(3)} |", end="")
            for j in range(self.cols):
                if self.grid[i][j] == 0: print(f'  {"OBS".rjust(4)}  |', end="")
                else: print(f' {self.grid[i][j]:.4f} |', end="")
            print()
        print("    |" + "-"*9*self.cols)
        
        print("    ", end="")
        for j in range(self.cols):
            print(str(j).rjust(9), end="")
        print()


        # for key in self.ghost.all_moves.keys():
        #     print(f'{key} : {self.ghost.all_moves[key]}')

        # print(self.ghost.position)
        # self.ghost.get_next_move()
        # print(self.ghost.position)
        
    def increase_time_step(self):
        self.ghost.get_next_move()
        print("Casper moved here : ", self.ghost.position)
        self.time_lapse()
        self.time_step += 1

    ###################### HMM METHODS #################################
    def normalize(self):
        sum_grid = np.sum(self.grid)
        self.grid /= sum_grid

    def observation(self, sensor_pos, sensor_reading):
        print(f"Sensor at : {sensor_pos[0]}, {sensor_pos[1]} and reading : {sensor_reading}" )
        # TODO : ?? do i need to do this for all positions or only this one
        val_indexes = self.sensor.get_adjacent(sensor_pos)
        mask = np.where(self.grid > 0, 1, 0)
        reading = 0.85 if sensor_reading else 0.15

        for idx in val_indexes:
            mask[idx[0], idx[1]] = 0

        self.grid = mask*self.grid*(1-reading) + (1-mask)*self.grid*reading
        self.normalize()

    def time_lapse(self):
        old_grid = self.grid.copy()
        all_prev_moves = self.ghost.all_prev_moves

        # TODO : ??
        for next_move in all_prev_moves.keys():
            prob = 0
            for prev_data in all_prev_moves[next_move]:
                prob += old_grid[prev_data[0], prev_data[1]]*prev_data[2]
            self.grid[next_move[0], next_move[1]] = prob