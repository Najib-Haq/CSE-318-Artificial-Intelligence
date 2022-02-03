import numpy as np
from tqdm import tqdm
import pandas as pd
import os
import gc
import seaborn as sns
import matplotlib.pyplot as plt
# import plotly.express as px

from Board import *
from Node import *
from Minmax import *
from Game import *

def play_100_games(pc, pc_args, player, player_args, depth, move_order):
    win_loss_ratio = 0
    all_moves = list(range(NO_OF_BINS))
    for i in tqdm(range(100), total=100):
        if move_order: np.random.shuffle(all_moves) # change move order
        else: depth = np.random.choice([2, 3, 4]) # else change depth
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
    return df_dict

def gen_report(csv_name="report_depth3.csv", ALL_EXP={}, check_depths=None):
    df_data = {
        "player0_hr" : [], 
        "player0_args" : [], 
        "player1_hr" : [],
        "player1_args" : [], 
        "ratio" : [], 
        "depth" : [], 
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
                    depth if isinstance(depth, list) else [depth, depth], 
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


def gen_corr_graph(csv_name, image_name, title=""):
    df = pd.read_csv(csv_name)
    # print("columns : ", df.columns)
    players_0 = df['player0_hr'].unique()
    data = []
    for p in players_0:
        vals = df[df['player0_hr'] == p]['ratio'].values
        data.append(vals)
    
    fig, ax = plt.subplots(figsize=(10,10))
    # seaborn code
    ax = sns.heatmap(
            data,
            annot=True,
            xticklabels=players_0,
            yticklabels=players_0,
            ax=ax,
            fmt='.3g',
        )

    ax.set_yticklabels(ax.get_yticklabels(), rotation = 0)
    ax.set(xlabel='Player 1', ylabel='Player 0')
    ax.set_title('Player 0 wins vs Player 1 ' + title)
    fig = ax.get_figure()
    fig.savefig(image_name)

    # plotly code
    # fig = px.imshow(data,
    #                 labels=dict(x="Player_1", y="Player_0", color="Ratio"),
    #                 x=players_0,
    #                 y=players_0,
    #                 width=800, height=800,
    #             )
    # fig.update_xaxes(side="bottom")
    # # fig.show()    
    # fig.write_image("fig_depth2.png")



if __name__ == "__main__":
    np.random.seed(42)
    # print(play_100_games(1, [], 1, [], 4, False))

    # exp h vs h and which weights are best
    ##############################################
    ALL_EXP1 = {
        (1, "eq"): [], 
        (2, "eq"): [2, 2],
        (2, "w2"): [2, 4],
        (2, "w1"): [4, 2],
        (3, "eq"): [2, 2, 2],
        (3, "w1"): [4, 2, 2],
        (3, "w2"): [2, 4, 2],
        (3, "w3"): [2, 2, 4],
        (4, "eq"): [2, 2, 2],
        (4, "w1"): [4, 2, 2],
        (4, "w2"): [2, 4, 2],
        (4, "w3"): [2, 2, 4],
        (5, "eq"): [2, 2, 2],
        (5, "w1"): [4, 2, 2],
        (5, "w2"): [2, 4, 2],
        (5, "w3"): [2, 2, 4],
        (6, "eq"): [2, 2, 2],
        (6, "w1"): [4, 2, 2],
        (6, "w2"): [2, 4, 2],
        (6, "w3"): [2, 2, 4],
    }
    gen_report("report_compare_h_w.csv", ALL_EXP1, check_depths=[2])
    gen_corr_graph("report_compare_h_w.csv", "compare_h_w.png", ": Compare Heuristics and Weights")

    
    # exp (best w) depth 4
    ###############################################
    ALL_EXP2 = {
        (1, "eq"): [], 
        (2, "w1"): [4, 2],
        (3, "w1"): [4, 2, 2],
        (4, "w3"): [2, 2, 4],
        (5, "w1"): [4, 2, 2],
        (6, "w3"): [2, 2, 4],
    }
    gen_report("report_depth4.csv", ALL_EXP2, check_depths=[6])
    gen_corr_graph("report_depth4.csv", "compare_depth4.png", ": Depth 6")

    
    # exp (best w) depth 6
    ###############################################
    ALL_EXP3 = {
        (1, "eq"): [], 
        (2, "w1"): [4, 2],
        (3, "w1"): [4, 2, 2],
        (4, "w3"): [2, 2, 4],
        (5, "w1"): [4, 2, 2],
        (6, "w3"): [2, 2, 4],
    }
    gen_report("report_depth6.csv", ALL_EXP3, check_depths=[8])
    gen_corr_graph("report_depth6.csv", "compare_depth6.png", ": Depth 8")

    
    # exp (best w) 2nd player depth >
    ###############################################
    ALL_EXP4 = {
        (1, "eq"): [], 
        (2, "w1"): [4, 2],
        (3, "w1"): [4, 2, 2],
        (4, "w3"): [2, 2, 4],
        (5, "w1"): [4, 2, 2],
        (6, "w3"): [2, 2, 4],
    }
    gen_report("report_diff_depth.csv", ALL_EXP4, check_depths=[[2, 5]])
    gen_corr_graph("report_diff_depth.csv", "compare_diff_depth.png", ": Depth1 > Depth0")
