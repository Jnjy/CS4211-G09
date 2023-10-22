import sys
import pandas as pd
import player_enum


def get_player_stats_by_id(file_path, player_id):
    df = pd.read_csv(file_path)
    df = df[df['sofifa_id'] == player_id]
    return df


def get_player_stats_by_ids(year="20152016", player_ids=[], is_away_team=False, lineup=[4, 2, 3, 1]):
    file_path = f"./datasets/ratings/epl_ratings_{year}.csv"
    target_file = "./data_output/match_player_stats_away.txt" if is_away_team else "./data_output/match_player_stats_home.txt"
    action_stats_arr = []
    for idx, player_id in enumerate(player_ids):
        player_stats_df = get_player_stats_by_id(file_path, player_id)
        if idx == 0:
            # output_player_stats(player_stats_df, player_enum.GOALKEEPER)
            action_stats_arr.extend(get_player_stats(player_stats_df, is_away_team)[player_enum.GK])
        if len(lineup) == 3:
            if 1 <= idx <= lineup[0]:
                # output_player_stats(player_stats_df, player_enum.DEFENDER)
                action_stats_arr.extend(get_player_stats(player_stats_df)[player_enum.DEF])
            elif lineup[0] < idx <= lineup[0] + lineup[1]:
                # output_player_stats(player_stats_df, player_enum.MIDFIELDER)
                action_stats_arr.extend(get_player_stats(player_stats_df)[player_enum.MID])
            elif lineup[0] + lineup[1] < idx <= lineup[0] + lineup[1] + lineup[2]:
                # output_player_stats(player_stats_df, player_enum.FORWARD)
                action_stats_arr.extend(get_player_stats(player_stats_df)[player_enum.FOR])
        if len(lineup) == 4:
            if 1 <= idx <= lineup[0]:
                # output_player_stats(player_stats_df, player_enum.DEFENDER)
                action_stats_arr.extend(get_player_stats(player_stats_df)[player_enum.DEF])
            elif lineup[0] < idx <= lineup[0] + lineup[1]:
                # output_player_stats(player_stats_df, player_enum.MIDFIELDER)
                action_stats_arr.extend(get_player_stats(player_stats_df)[player_enum.MID])
            elif lineup[0] + lineup[1] < idx <= lineup[0] + lineup[1] + lineup[2]:
                # output_player_stats(player_stats_df, player_enum.MIDFIELDER)
                action_stats_arr.extend(get_player_stats(player_stats_df)[player_enum.MID])
            elif lineup[0] + lineup[1] + lineup[2] < idx <= lineup[0] + lineup[1] + lineup[2] + lineup[3]:
                # output_player_stats(player_stats_df, player_enum.FORWARD)
                action_stats_arr.extend(get_player_stats(player_stats_df)[player_enum.FOR])
        if len(lineup) == 5:
            if 1 <= idx <= lineup[0]:
                # output_player_stats(player_stats_df, player_enum.DEFENDER)
                action_stats_arr.extend(get_player_stats(player_stats_df)[player_enum.DEF])
            elif lineup[0] < idx <= lineup[0] + lineup[1]:
                # output_player_stats(player_stats_df, player_enum.MIDFIELDER)
                action_stats_arr.extend(get_player_stats(player_stats_df)[player_enum.MID])
            elif lineup[0] + lineup[1] < idx <= lineup[0] + lineup[1] + lineup[2]:
                # output_player_stats(player_stats_df, player_enum.MIDFIELDER)
                action_stats_arr.extend(get_player_stats(player_stats_df)[player_enum.MID])
            elif lineup[0] + lineup[1] + lineup[2] < idx <= lineup[0] + lineup[1] + lineup[2] + lineup[3]:
                # output_player_stats(player_stats_df, player_enum.FORWARD)
                action_stats_arr.extend(get_player_stats(player_stats_df)[player_enum.MID])
            elif lineup[0] + lineup[1] + lineup[2] + lineup[3] < idx <= lineup[0] + lineup[1] + lineup[2] + lineup[3] \
                    + lineup[4]:
                action_stats_arr.extend(get_player_stats(player_stats_df)[player_enum.FOR])

    return action_stats_arr


def get_player_stats(df, is_away=False) -> dict[str, list]:
    stats_map = {
        "Def": [],
        "Mid": [],
        "For": [],
        "GK": []
    }
    stats_map["Def"].extend((df['attacking_short_passing'].values[0], df['skill_long_passing'].values[0],
                             df['defending_sliding_tackle'].values[0], df['skill_dribbling'].values[0]))

    stats_map["Mid"].extend((df['attacking_short_passing'].values[0], df['skill_long_passing'].values[0],
                             df['power_long_shots'].values[0], df['defending_sliding_tackle'].values[0],
                             df['attacking_crossing'].values[0], df['skill_dribbling'].values[0]))

    # r_closeShot, r_longShot, r_volley, r_header, r_tackled, r_dribble, r_shortPass, r_longPass
    stats_map["For"].extend((df['attacking_finishing'].values[0], df['power_long_shots'].values[0],
                             df['attacking_volleys'].values[0], df['attacking_heading_accuracy'].values[0],
                             df['defending_sliding_tackle'].values[0], df['skill_dribbling'].values[0],
                            df['attacking_short_passing'].values[0], df['skill_long_passing'].values[0]))

    if is_away:
        stats_map["GK"].extend((df['goalkeeping_kicking'].values[0], df['goalkeeping_kicking'].values[0]))
    else:
        stats_map["GK"].extend((df['goalkeeping_handling'].values[0],))
    return stats_map


# For() takes in r_closeShot, r_longShot, r_volley, r_header, r_tackled, r_dribble
def output_player_stats(df, player_type: int):
    print(f"###### Player Type: {player_enum.player_output_mapping.get(player_type)}  ######")

    try:
        print("Player Name -> ", df['long_name'].values[0])
    except:
        print("Player (fifa id) -> ", df['sofifa_id'].values[0])

    # print("Club Name -> ", df['club_name'].values[0])
    # print("Short Pass -> ", df['attacking_short_passing'].values[0])
    # print("Long Pass -> ", df['skill_long_passing'].values[0])
    # print("Dribble -> ", df['skill_dribbling'].values[0])
    # print("Attacking Crossing -> ", df['attacking_crossing'].values[0])
    print("Attacking FK Accuracy -> ", df['skill_fk_accuracy'].values[0])

    # r_shortPass, r_longPass, r_tackled, r_dribble
    print("\n###### Def() ######")
    print("Short Pass -> ", df['attacking_short_passing'].values[0])
    print("Long Pass -> ", df['skill_long_passing'].values[0])
    print("Tackling -> ", df['defending_sliding_tackle'].values[0],
          " **This should be weighted tackle metrics, ignore for now!")
    print("Dribble -> ", df['skill_dribbling'].values[0])

    # r_shortPass, r_longPass, r_longShot, r_tackled, r_cross, r_dribble
    print("\n###### Mid() ######")
    print("Short Pass -> ", df['attacking_short_passing'].values[0])
    print("Long Pass -> ", df['skill_long_passing'].values[0])
    print("Power Long Shot -> ", df['power_long_shots'].values[0])
    print("Tackling -> ", df['defending_sliding_tackle'].values[0],
          " **This should be weighted tackle metrics, ignore for now!")
    print("Attacking Crossing -> ", df['attacking_crossing'].values[0])
    print("Dribble -> ", df['skill_dribbling'].values[0])

    # r_closeShot, r_longShot, r_volley, r_header, r_tackled, r_dribble
    print("\n###### For() ######")
    print("Attacking Finishing -> ", df['attacking_finishing'].values[0])
    print("Power Long Shot -> ", df['power_long_shots'].values[0])
    print("Attacking Volleys -> ", df['attacking_volleys'].values[0])
    print("Attacking Heading -> ", df['attacking_heading_accuracy'].values[0])
    print("Tackling -> ", df['defending_sliding_tackle'].values[0],
          " **This should be weighted tackle metrics, ignore for now!")
    print("Dribble -> ", df['skill_dribbling'].values[0])

    print("\n###### Goal Keeping Stats ######")
    print("Goal Keeping Diving -> ", df['goalkeeping_diving'].values[0])
    print("Goal Keeping Handling -> ", df['goalkeeping_handling'].values[0])
    print("Goal Keeping Kicking -> ", df['goalkeeping_kicking'].values[0])
    print("Goal Keeping Positioning -> ", df['goalkeeping_positioning'].values[0])
    print("Goal Keeping Reflexes -> ", df['goalkeeping_reflexes'].values[0],
          "\n=================================================\n")


# run from project root
# python ./scripts/player_stats.py ./datasets/ratings/epl_ratings_20152016.csv 9014
def __main__():
    arguments = sys.argv[1:]
    output_player_stats(get_player_stats_by_id(arguments[0], int(arguments[1])))


if __name__ == '__main__':
    __main__()
