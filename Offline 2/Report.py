import numpy as np
from tqdm import tqdm
import pandas as pd
import os
import gc
# import seaborn as sn
import plotly.express as px

from Board import *
from Node import *
from Minmax import *
from Game import *

ALL_EXP = {
    (1, ""): [], 
    (2, "eq"): [0.5, 0.5],
    (2, "w2"): [0.3, 0.7],
    (2, "w1"): [0.7, 0.3],
    (3, "eq"): [0.33, 0.33, 0.33],
    (3, "w1"): [0.66, 0.33, 0.33],
    (3, "w2"): [0.33, 0.66, 0.33],
    (3, "w3"): [0.33, 0.33, 0.66],
    (4, "eq"): [0.33, 0.33, 0.33],
    (4, "w1"): [0.66, 0.33, 0.33],
    (4, "w2"): [0.33, 0.66, 0.33],
    (4, "w3"): [0.33, 0.33, 0.66],
    (5, "eq"): [0.5, 0.5],
    (5, "w2"): [0.3, 0.7],
    (5, "w1"): [0.7, 0.3],
    (6, "eq"): [0.5, 0.5],
    (6, "w2"): [0.3, 0.7],
    (6, "w1"): [0.7, 0.3],
}

check_depths = [3]

def play_100_games(pc, pc_args, player, player_args, depth, move_order):
    win_loss_ratio = 0
    all_moves = list(range(NO_OF_BINS))
    for i in tqdm(range(100), total=100):
        if move_order: np.random.shuffle(all_moves) # change move order
        else: depth = np.random.choice(check_depths) # else change depth
        g = Game("pc", True)
        g.set_heuristic(
            pc_hr=pc, 
            pc_hr_args=pc_args,
            player_hr=player, 
            player_hr_args=player_args, 
            depth=depth, 
            move_order=all_moves)
        winner = g.game_play_pc(verbose=False)
        if winner == g.player: win_loss_ratio += 1
    # gc.collect()
    return win_loss_ratio

def add_to_dict(df_dict, p0, p0_hr, p1, p1_hr, ratio, depth):
    df_dict['player0_hr'].append(str(p0[0]) + '_' + p0[1])
    df_dict['player0_args'].append(p0_hr)
    df_dict['player1_hr'].append(str(p1[0]) + '_' + p1[1])
    df_dict['player1_args'].append(p1_hr)
    df_dict['ratio'].append(ratio)
    df_dict['depth'].append(depth)
    # df_dict['move_order'].append(move_order)
    return df_dict


def gen_report(csv_name="report_depth3.csv"):
    df_data = {
        "player0_hr" : [], 
        "player0_args" : [], 
        "player1_hr" : [],
        "player1_args" : [], 
        "ratio" : [], 
        "depth" : [], 
        # "move_order" : []
    }

    for p0 in ALL_EXP.keys():
        for p1 in ALL_EXP.keys():
            for depth in check_depths:
                print("GAME : ", p0, " vs ", p1, " ; depth: ", depth)
                ratio = play_100_games(
                    p1[0],
                    ALL_EXP[p1],
                    p0[0],
                    ALL_EXP[p0],
                    depth,
                    move_order=True
                )
                df_data = add_to_dict(df_data, p0, ALL_EXP[p0], p1, ALL_EXP[p1], ratio, depth)

    # save csv
    if os.path.isfile(csv_name):
        df = pd.read_csv(csv_name)
        df = df.append(pd.DataFrame(df_data), ignore_index=True)
    else:
        df = pd.DataFrame(df_data)
    df.to_csv(csv_name, index=False)


def gen_corr_graph(csv_name):
    df = pd.read_csv(csv_name)
    # print("columns : ", df.columns)
    players_0 = df['player0_hr'].unique()
    data = []
    for p in players_0:
        vals = df[df['player0_hr'] == p]['ratio'].values
        data.append(vals)
    fig = px.imshow(data,
                    labels=dict(x="Player_1", y="Player_0", color="Ratio"),
                    x=players_0,
                    y=players_0,
                    width=800, height=800,
                )
    fig.update_xaxes(side="bottom")
    # fig.show()    
    fig.write_image("fig_depth2.png")



if __name__ == "__main__":
    np.random.seed(42)
    # print(play_100_games(1, [], 1, [], 4, False))
    # gen_report()
    gen_corr_graph("report.csv")