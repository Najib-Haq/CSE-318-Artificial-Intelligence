import numpy as np

from Grid import Grid

if __name__ == "__main__":
    obstacle_list = []
    with open("input.txt", "r") as file:
        row, col, obs = [int(i) for i in file.readline().split(" ")]
        print(row, col, obs)
        for i in range(obs):
            obstacle_list.append([int(i) for i in file.readline().split(" ")])
        print(obstacle_list)

        grid_o = Grid(row, col, obstacle_list)
        print("Initial Probability : ")
        grid_o.show_grid()

        while(True):
            line = file.readline().rstrip('\n').split(" ")
            # increase one time step
            grid_o.increase_time_step()
            print(">>After Time Step :")
            grid_o.show_grid()

            print(line)
            if line[0].upper() == "R":
                grid_o.observation((int(line[1]), int(line[2])), int(line[3]))
                print(">>After Observation :")
                grid_o.show_grid()
            elif line[0].upper() == "C":
                print("Casper is in : ", np.unravel_index(grid_o.grid.argmax(), grid_o.grid.shape))
            elif line[0].upper() == "Q":
                break
            
