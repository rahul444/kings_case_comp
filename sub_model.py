import os
import pandas as pd
import csv
import matplotlib.pyplot as plt

def convert(string):
    if (string == 'PF' or string == 'SF'):
        return 1
    elif (string == 'SG' or string == 'PG'):
        return 2
    else:
        return 3

# vorp, ws/48, per
def subCost(lastName, teamName):
    with open('./nba17_advanced.csv') as reader:
        csv_reader = csv.reader(reader)
        startValue = 0
        position = ''
        for row in csv_reader:
            if lastName in row[1] and row[4] == teamName:
                position = row[2]
                startValue = float(row[7]) * .33 + float(row[23]) * .33 + float(row[28]) * .33

    with open('./nba17_advanced.csv') as reader_15new:
        csv_reader15new = csv.reader(reader_15new)

        max = 0
        for rows in csv_reader15new:
            if rows[4] == teamName:
                if convert(rows[2]) == convert(position):
                    compare = float(rows[7]) * .33 + float(rows[23]) * .33 + float(rows[28]) * .33
                    if compare != startValue:
                        if compare > max:
                            max = compare

        return startValue - max

def foul_trouble(min_remaining, fouls):
    return (0.01544 * min_remaining) + (0.1134 * fouls) - (0.0003038 * (min_remaining ** 2)) + (0.003306 * min_remaining * fouls) - 0.3145


def win_probaiblity(time, filename):
    wp = pd.read_csv('./win_prob/2016/' + filename)
    for row in wp.iterrows():
        if row[1][0] > time:
            return row[1][1]
    return 0.5

pbp = pd.read_csv('./data/pbp_info_2016-17.csv')
for filename in os.listdir('./win_prob/2016/'):
    game_id, wp_team = filename.split('_')

    if game_id != '21601108':
        continue

    print(filename)

    game = pbp[pbp['game_id'] == int(game_id)]
    foul_plays = game[game['description'].str.contains('Foul:')]
    num_periods = game['period'].max()
    total_seconds = (48 + (num_periods - 4) * 5) * 60
    
    sub_vals = []
    win_probs = []
    sub_costs = []
    foul_troubles = []

    for foul_play in foul_plays.iterrows():
        desc = foul_play[1][14]
        team = desc.split()[0][1:-1]
        player_last_name = desc.split()[1]
        num_fouls = int(desc[desc.index('(') + 1])

        period = foul_play[1][7]
        minutes, seconds = foul_play[1][6].split(':')
        min_remaining_in_q = float(minutes) + (float(seconds) / 60)
        # if we are in OT assume we are only going to play one OT
        if period < 5:
            min_remaining = (12 * (4 - period)) + min_remaining_in_q
        else:
            min_remaining = min_remaining_in_q
        seconds_elapsed = total_seconds - (60 * min_remaining)

        cur_foul_trouble = foul_trouble(min_remaining, num_fouls)
        win_prob = win_probaiblity(seconds_elapsed, filename)
        sub_cost = subCost(player_last_name, team) / 10
        
        if team != wp_team:
            win_prob = 1 - win_prob

        sub_val = 1.255 * cur_foul_trouble + 0.318 * (1 - win_prob) - 0.228 * sub_cost


        if player_last_name == 'Curry':
            print(desc)
            print(cur_foul_trouble)
            print(win_prob)
            print(sub_cost)
            print(sub_val)
            sub_vals.append(sub_val)
            sub_costs.append(sub_cost)
            win_probs.append(win_prob)
            foul_troubles.append(cur_foul_trouble)

    
    plt.plot(range(1, 6), sub_costs, label='Substitution Cost')
    plt.plot(range(1, 6), win_probs, label='Win Probability')
    plt.plot(range(1, 6), foul_troubles, label='Foul Trouble')
    plt.xlabel("Number of Fouls")
    plt.ylabel("Metric")
    plt.legend()

    plt.show()

    plt.plot(range(1, 6), sub_vals)
    plt.title("Steph Curry's Substitution Index")
    plt.xlabel("Number of Fouls")
    plt.ylabel("Substitution Index")

    plt.show()

    print(sub_vals)
            
    # break