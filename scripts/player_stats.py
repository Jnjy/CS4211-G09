import sys
from typing import Tuple, Dict, List, Any

import pandas as pd
import player_enum


def get_player_stats_by_id(file_path, player_id):
    specific_player_columns = ['sofifa_id', 'attacking_short_passing', 'skill_long_passing',
                               'skill_dribbling', 'power_long_shots', 'attacking_crossing', 'attacking_finishing',
                               'attacking_volleys', 'attacking_heading_accuracy', 'goalkeeping_kicking',
                               'goalkeeping_handling', 'defending_standing_tackle',
                               'defending_sliding_tackle', 'mentality_interceptions', 'mentality_penalties']
    df = pd.read_csv(file_path, engine='pyarrow', usecols=specific_player_columns)
    df = df[df['sofifa_id'] == player_id]
    return df


def get_player_stats_by_ids(year="20152016", player_ids=[], is_away_team=False, lineup=[4, 2, 3, 1]):
    file_path = f"./datasets/ratings/epl_ratings_{year}.csv"
    action_stats_arr = []
    player_weighted_stats_map = {
        'Def': [],
        'Mid': [],
        'For': []
    }
    for idx, player_id in enumerate(player_ids):
        player_stats_df = get_player_stats_by_id(file_path, player_id)
        if idx == 0:
            stats_map, stats_map_aux = get_player_stats(player_stats_df, is_away_team)
            action_stats_arr.extend(stats_map[player_enum.GK])
        if len(lineup) == 3:
            if 1 <= idx <= lineup[0]:
                stats_map, stats_map_aux = get_player_stats(player_stats_df)
                action_stats_arr.extend(stats_map[player_enum.DEF])
                player_weighted_stats_map['Def'].append(stats_map_aux['Def'])
            elif lineup[0] < idx <= lineup[0] + lineup[1]:
                stats_map, stats_map_aux = get_player_stats(player_stats_df)
                action_stats_arr.extend(stats_map[player_enum.MID])
                player_weighted_stats_map['Mid'].append(stats_map_aux['Mid'])
            elif lineup[0] + lineup[1] < idx <= lineup[0] + lineup[1] + lineup[2]:
                stats_map, stats_map_aux = get_player_stats(player_stats_df)
                action_stats_arr.extend(stats_map[player_enum.FOR])
                player_weighted_stats_map['For'].append(stats_map_aux['For'])
        if len(lineup) == 4:
            if 1 <= idx <= lineup[0]:
                stats_map, stats_map_aux = get_player_stats(player_stats_df)
                action_stats_arr.extend(stats_map[player_enum.DEF])
                player_weighted_stats_map['Def'].append(stats_map_aux['Def'])
            elif lineup[0] < idx <= lineup[0] + lineup[1]:
                stats_map, stats_map_aux = get_player_stats(player_stats_df)
                action_stats_arr.extend(stats_map[player_enum.MID])
                player_weighted_stats_map['Mid'].append(stats_map_aux['Mid'])
            elif lineup[0] + lineup[1] < idx <= lineup[0] + lineup[1] + lineup[2]:
                stats_map, stats_map_aux = get_player_stats(player_stats_df)
                action_stats_arr.extend(stats_map[player_enum.MID])
                player_weighted_stats_map['Mid'].append(stats_map_aux['Mid'])
            elif lineup[0] + lineup[1] + lineup[2] < idx <= lineup[0] + lineup[1] + lineup[2] + lineup[3]:
                stats_map, stats_map_aux = get_player_stats(player_stats_df)
                action_stats_arr.extend(stats_map[player_enum.FOR])
                player_weighted_stats_map['For'].append(stats_map_aux['For'])
        if len(lineup) == 5:
            if 1 <= idx <= lineup[0]:
                stats_map, stats_map_aux = get_player_stats(player_stats_df)
                action_stats_arr.extend(stats_map[player_enum.DEF])
                player_weighted_stats_map['Def'].append(stats_map_aux['Def'])
            elif lineup[0] < idx <= lineup[0] + lineup[1]:
                stats_map, stats_map_aux = get_player_stats(player_stats_df)
                action_stats_arr.extend(stats_map[player_enum.MID])
                player_weighted_stats_map['Mid'].append(stats_map_aux['Mid'])
            elif lineup[0] + lineup[1] < idx <= lineup[0] + lineup[1] + lineup[2]:
                stats_map, stats_map_aux = get_player_stats(player_stats_df)
                action_stats_arr.extend(stats_map[player_enum.MID])
                player_weighted_stats_map['Mid'].append(stats_map_aux['Mid'])
            elif lineup[0] + lineup[1] + lineup[2] < idx <= lineup[0] + lineup[1] + lineup[2] + lineup[3]:
                stats_map, stats_map_aux = get_player_stats(player_stats_df)
                action_stats_arr.extend(stats_map[player_enum.MID])
                player_weighted_stats_map['Mid'].append(stats_map_aux['Mid'])
            elif lineup[0] + lineup[1] + lineup[2] + lineup[3] < idx <= lineup[0] + lineup[1] + lineup[2] + lineup[3] \
                    + lineup[4]:
                stats_map, stats_map_aux = get_player_stats(player_stats_df)
                action_stats_arr.extend(stats_map[player_enum.FOR])
                player_weighted_stats_map['For'].append(stats_map_aux['For'])

    return action_stats_arr, player_weighted_stats_map


def get_player_stats(df, is_away=False) -> tuple[dict[str, list[Any]], dict[str, int]]:
    stats_map = {
        "Def": [],
        "Mid": [],
        "For": [],
        "GK": []
    }
    stats_map_aux = {
        "Def": 0,
        "Mid": 0,
        "For": 0,
    }

    stats_map["Def"].extend((df['attacking_short_passing'].values[0], df['skill_long_passing'].values[0],
                             df['skill_dribbling'].values[0]))

    stats_map_aux["Def"] += (df['defending_standing_tackle'].values[0] + df['defending_sliding_tackle'].values[0]
                             + df['mentality_interceptions'].values[0]) / 3

    stats_map["Mid"].extend((df['attacking_short_passing'].values[0], df['skill_long_passing'].values[0],
                             df['power_long_shots'].values[0],
                             df['attacking_crossing'].values[0], df['skill_dribbling'].values[0]))

    stats_map_aux["Mid"] += (df['defending_standing_tackle'].values[0] + df['defending_sliding_tackle'].values[0]
                             + df['mentality_interceptions'].values[0]) / 3

    stats_map["For"].extend((df['attacking_finishing'].values[0], df['power_long_shots'].values[0],
                             df['attacking_volleys'].values[0], df['attacking_heading_accuracy'].values[0],
                             df['skill_dribbling'].values[0],
                             df['attacking_short_passing'].values[0], df['skill_long_passing'].values[0] , df['mentality_penalties'].values[0]))

    stats_map_aux["For"] += (df['defending_standing_tackle'].values[0] + df['defending_sliding_tackle'].values[0]
                             + df['mentality_interceptions'].values[0]) / 3

    if is_away:
        stats_map["GK"].extend((df['goalkeeping_kicking'].values[0], df['goalkeeping_kicking'].values[0]))
    else:
        stats_map["GK"].extend((df['goalkeeping_handling'].values[0],))
    return stats_map, stats_map_aux

# run from project root
# python ./scripts/player_stats.py ./datasets/ratings/epl_ratings_20152016.csv 9014
def __main__():
    arguments = sys.argv[1:]


if __name__ == '__main__':
    __main__()
