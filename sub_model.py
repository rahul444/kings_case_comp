# FOUL TROUBLE MODEL
# 0.01544 minutes remaining
# 0.1134 fouls
# -0.0003038 minutes squared
# 0.003306 minutes*fouls 
# -0.3145 intercept


# 1. Loop through directory of game ids
# 2. Filter pbp table by that game_id
# 3. Filter for only plays with fouls
# 4. Get Team, Player, and num fouls from description
# 5. Using advanced stat table get advanced stat for that player
# 6. Get max advanced stat for best replacement player (use position from advanced stat table)
# 7. Calculate foul_trouble function
# 8. Calculate opportunity cost using advanced stat
# 9. Get win prob at the time of given foul play
# 10. Combine all 3 factors with weights and return single value if player should be subbed out

# [PHI] Okafor Foul: Shooting (1 PF) (2 FTA) (L Richardson)

import os
import pandas as pd

def foul_trouble(min_remaining, fouls):
    return (0.01544 * min_remaining) + (0.1134 * fouls) - (0.0003038 * (min_remaining ** 2)) + (0.003306 * min_remaining * fouls) - 0.3145

def opportunity_cost():
    return 1

def win_probaiblity(time, filename):
    wp = pd.read_csv('./win_prob/2016/' + filename)
    for row in wp.iterrows():
        if row[1][0] > time:
            return row[1][1]
    return 0.5

pbp = pd.read_csv('./data/pbp_info_2016-17.csv')
for filename in os.listdir('./win_prob/2016/'):
    print(filename)
    game_id, team = filename.split('_')
    game = pbp[pbp['game_id'] == int(game_id)]
    foul_plays = game[game['description'].str.contains('Foul:')]
    num_periods = game['period'].max()
    total_seconds = (48 + (num_periods - 4) * 5) * 60
    
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
        min_remaining = min_remaining_in_q
        seconds_elapsed = total_seconds - (60 * min_remaining)

        cur_foul_trouble = foul_trouble(min_remaining, num_fouls)
        win_prob = win_probaiblity(seconds_elapsed, filename)
        opportunity_cost = 1

        print(cur_foul_trouble)
        print(win_prob)
        if win_prob > 0.75:
            pass
        elif win_prob < 0.25:
            pass
        else:
            pass
            
    break