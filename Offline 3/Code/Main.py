import numpy as np

from Grid import Grid


def file_input():
    obstacle_list = []
    with open("input.txt", "r") as file:
        row, col, obs = [int(i) for i in file.readline().split(" ")]
        print("Input : ",row, col, obs)
        for i in range(obs):
            obstacle_list.append([int(i) for i in file.readline().split(" ")])
        # print(obstacle_list)

        grid_o = Grid(row, col, obstacle_list)
        print("Initial Probability : ")
        grid_o.show_grid()

        i = 1
        while(True):
            line = file.readline().rstrip('\n').split(" ")
            # line = input().split(" ")
            # increase one time step
            
            # print(">>After Time Step :")
            # grid_o.show_grid()

            print("Input : ",line)
            if line[0].upper() == "R":
                grid_o.increase_time_step()
                grid_o.observation((int(line[1]), int(line[2])), int(line[3]))
                print(f">>Probability Update ({i}th Reading):")
                i += 1
                grid_o.show_grid()
            elif line[0].upper() == "C":
                print(">>Casper is most probably at : ", np.unravel_index(grid_o.grid.argmax(), grid_o.grid.shape))
            elif line[0].upper() == "Q":
                break
            

def manual_input():
    obstacle_list = []
    row, col, obs = [int(i) for i in input().split(" ")]
    print("Input : ", row, col, obs)
    for i in range(obs):
        obstacle_list.append([int(i) for i in input().split(" ")])
    # print(obstacle_list)

    grid_o = Grid(row, col, obstacle_list)
    print("Initial Probability : ")
    grid_o.show_grid()

    i = 1
    while(True):
        line = input().split(" ")
        # line = input().split(" ")
        # increase one time step
        
        # print(">>After Time Step :")
        # grid_o.show_grid()

        print("Input : ",line)
        if line[0].upper() == "R":
            grid_o.increase_time_step()
            grid_o.observation((int(line[1]), int(line[2])), int(line[3]))
            print(f">>Probability Update ({i}th Reading):")
            i += 1
            grid_o.show_grid()
        elif line[0].upper() == "C":
            print(">>Casper is most probably at : ", np.unravel_index(grid_o.grid.argmax(), grid_o.grid.shape))
        elif line[0].upper() == "Q":
            break
        


if __name__ == "__main__":
    file_input()
    # manual_input()