import copy
import os
import pandas as pd
from statistics import mean

from match_stats import read_match_and_generate_stats
from template_enum import player_position_row, soccer_field_grid, player_types, pos_map, player_row_position


def get_soccer_field_grid(df, team):
    team = team.lower()
    assert team == "home" or team == "away", "get_soccer_field_grid() team parameter to either be home or away"

    formation = df[team + "_formation"]
    sequence = df[team + "_sequence"]

    if ("-" in formation):
        formation = formation.split("-")
    elif ("/" in formation):
        formation = formation.split("/")
        formation[2] = formation[2][-1]
        # only keep the last character of the last value
        # if csv converted formation value to -/-/-, there is only 3 values (csv converted it into a date format)
        # only the value is changed into 4 digit value for year.
    else:
        print(formation)
        raise Exception("Check pre-processing for formation")

    # formation up to 5 rows
    assert len(formation) <= 5, 'Check processing for formation'

    sequence = sequence.split(",")
    # first is goal keeper -- always C
    assert sequence[0] == 'C', "Goal Keeper not at C position!"

    template = ["-1(6)", 0, 0, 0, 0, 0, 0, 0, "-1(6)"]
    i = 1
    entire_formation = ['', [], '']
    row_index = 0  # row index in formation
    formation_row_index = 0  # row index in processed formation -- 1 def, 1 for, remaining mid
    for x in formation:
        y = 0

        row_formation = copy.deepcopy(template)
        while (y < int(x)):
            pos = player_position_row.get(sequence[i])

            row_formation[pos] = 1

            y = y + 1  # index of players
            i = i + 1  # index of player positions "L", "LR", "CL", "C", "CR", "RL", "R"

        if (row_index != 0 and row_index != len(formation) - 1):
            entire_formation[formation_row_index].append(row_formation)

        else:
            entire_formation[formation_row_index] = row_formation
            formation_row_index = formation_row_index + 1

        if (row_index == len(formation) - 2):
            formation_row_index = formation_row_index + 1

        row_index = row_index + 1

    return entire_formation


def generate_positions_for_stats(n, row):  # Generates 0001000 -> [C]
    posStr = ['L', 'RL', 'CL', 'C', 'CR', 'LR', 'R']
    pattern = pos_map[n]

    positions = []
    row = row[1:-1]
    for i in range(7):
        if row[i] == 1:
            positions.append(posStr[i])
    print(row, "Positions -> ", positions)
    return positions


def generate_stats_template(df, match_id, year, team, grid_formation):
    home_stats, home_weighted_stats, away_stats, away_weighted_stats, home_lineup, away_lineup \
        = read_match_and_generate_stats(df, match_id, year, team)
    assert len(away_lineup) in (3, 4, 5)
    atkDefLen, atkMid1Len, atkMid2Len, atkMid3Len, atkForLen = -1, -1, -1, -1, -1
    if len(away_lineup) == 3:
        atkDefLen = away_lineup[0]
        atkMid1Len = away_lineup[1]
        atkForLen = away_lineup[2]
    elif len(away_lineup) == 4:
        atkDefLen = away_lineup[0]
        atkMid1Len = away_lineup[1]
        atkMid2Len = away_lineup[2]
        atkForLen = away_lineup[3]
    elif len(away_lineup) == 5:
        atkDefLen = away_lineup[0]
        atkMid1Len = away_lineup[1]
        atkMid2Len = away_lineup[2]
        atkMid3Len = away_lineup[3]
        atkForLen = away_lineup[4]

    atkKepStats = f'AtkKep = [pos[C] == 1]Kep_1({away_stats.pop(0)}, {away_stats.pop(0)}, C);'

    atkDefStats = 'AtkDef = '
    for idx, pos_val in enumerate(generate_positions_for_stats(atkDefLen, grid_formation[0])):
        r_shortpass = away_stats.pop(0)
        r_longpass = away_stats.pop(0)
        r_dribble = away_stats.pop(0)
        r_tackle = int(mean(home_weighted_stats["Def"])) if len(home_weighted_stats["Def"]) > 0 else 0
        weighted_tackle = int((1 - (r_dribble / (r_dribble + r_tackle))) * 100)

        atkDefStats += f'[pos[{pos_val}] == 1]Def({r_shortpass}, {r_longpass}, {r_dribble}, ' \
                       f'{weighted_tackle}, {pos_val}){" [] " if idx < atkDefLen - 1 else ";"}'

    # AtkMid1, AtkMid2, AtkMid3
    atkMidStatsList = ['', '', '']
    atkMidLenList = [atkMid1Len, atkMid2Len, atkMid3Len]
    for idx, atkMidI in enumerate(atkMidStatsList):
        if idx == 1 and atkMid2Len == -1:
            break
        if idx == 2 and atkMid3Len == -1:
            break
        # print("Debug -> ", grid_formation[1:-1][0][idx], "Idx -> ", idx)
        for j, pos_val in enumerate(generate_positions_for_stats(atkMidLenList[idx], grid_formation[1:-1][0][idx])):
            r_shortpass = away_stats.pop(0)
            r_longpass = away_stats.pop(0)
            r_longshot = away_stats.pop(0)
            r_cross = away_stats.pop(0)
            r_dribble = away_stats.pop(0)
            r_tackle = int(mean(home_weighted_stats["Mid"])) if len(home_weighted_stats["Mid"]) > 0 else 0
            weighted_tackle = int((1 - (r_dribble / (r_dribble + r_tackle))) * 100)
            
            atkMidStatsList[idx] += f'[pos[{pos_val}] == 1]Mid{idx+1}({r_shortpass}, {r_longpass}, ' \
                                   f'{r_longshot}, {weighted_tackle}, {r_cross}, ' \
                                   f'{r_dribble}, {pos_val}){" [] " if j < atkMidLenList[idx] - 1 else ";"}'

    atkForStats = 'AtkFor = '
    if atkForLen == 0:
        atkForStats += 'Skip;'
    # If you need to reverse order of player stats for row, just reverse here. (Don't need! -HC)
    for idx, pos_val in enumerate(generate_positions_for_stats(atkForLen, grid_formation[-1])):
        r_finish = away_stats.pop(0)
        r_longshot = away_stats.pop(0)
        r_volley = away_stats.pop(0)
        r_header = away_stats.pop(0)
        r_dribble =away_stats.pop(0)
        r_shortpass =away_stats.pop(0)
        r_longpass = away_stats.pop(0)
        r_tackle = int(mean(home_weighted_stats["For"])) if len(home_weighted_stats["For"]) > 0 else 0
        weighted_tackle = int((1 - (r_dribble / (r_dribble + r_tackle))) * 100)

        atkForStats += f'[pos[{pos_val}] == 1]For({r_finish}, {r_longshot}, {r_volley}, ' \
                       f'{r_header}, {weighted_tackle}, {r_dribble}, {r_shortpass}, ' \
                       f'{r_longpass}, {pos_val}){" [] " if idx < atkForLen - 1 else ";"}'

    defKepStats = f'DefKep = [pos[C] == 1]Kep_2({home_stats.pop(0)}, C);'
    return atkKepStats, atkDefStats, atkMidStatsList, atkForStats, defKepStats


def replace_file_content(df, match_id, team, grid_formation, year_str):
    print("Grid Formation -> ", grid_formation)
    template_file = open('../template.pcsp', 'rt')
    data = template_file.read()
    template_file.close()

    result_file = open(f'./pcsp_files/{match_id}_{team}.pcsp', 'wt')
    # Grids
    data = data.replace(soccer_field_grid["ATKDEFPOS"], str(grid_formation[0]).replace("'-1(6)'", '-1(6)'))

    player_stats = generate_stats_template(df, match_id, year_str, team, grid_formation)
    mid_grids = grid_formation[1]
    blank_grid = "[-1(6), 0, 0, 0, 0, 0, 0, 0, -1(6)]"
    if len(mid_grids) == 1:
        data = data.replace(soccer_field_grid["ATKMID1POS"], blank_grid)
        data = data.replace(soccer_field_grid["ATKMID2POS"], blank_grid)
        data = data.replace(soccer_field_grid["ATKMID3POS"], str(mid_grids[0]).replace("'-1(6)'", '-1(6)'))
        data = data.replace(player_types['AtkMid1'], 'Skip;')
        data = data.replace(player_types['AtkMid2'], 'Skip;')
        data = data.replace(player_types['AtkMid3'], player_stats[2][0].replace('Mid1', 'Mid3'))
    if len(mid_grids) == 2:
        data = data.replace(soccer_field_grid["ATKMID1POS"], blank_grid)
        data = data.replace(soccer_field_grid["ATKMID2POS"], str(mid_grids[0]).replace("'-1(6)'", '-1(6)'))
        data = data.replace(soccer_field_grid["ATKMID3POS"], str(mid_grids[1]).replace("'-1(6)'", '-1(6)'))
        data = data.replace(player_types['AtkMid1'], 'Skip;')
        data = data.replace(player_types['AtkMid2'], player_stats[2][0].replace('Mid1', 'Mid2'))
        data = data.replace(player_types['AtkMid3'], player_stats[2][1].replace('Mid2', 'Mid3'))

    if len(mid_grids) == 3:
        data = data.replace(soccer_field_grid["ATKMID1POS"], str(mid_grids[0]).replace("'-1(6)'", '-1(6)'))
        data = data.replace(soccer_field_grid["ATKMID2POS"], str(mid_grids[1]).replace("'-1(6)'", '-1(6)'))
        data = data.replace(soccer_field_grid["ATKMID3POS"], str(mid_grids[2]).replace("'-1(6)'", '-1(6)'))
        data = data.replace(player_types['AtkMid1'], player_stats[2][0])
        data = data.replace(player_types['AtkMid2'], player_stats[2][1])
        data = data.replace(player_types['AtkMid3'], player_stats[2][2])

    data = data.replace(soccer_field_grid["ATKFORPOS"], str(grid_formation[2]).replace("'-1(6)'", '-1(6)'))

    data = data.replace(player_types['AtkKep'], player_stats[0])
    data = data.replace(player_types['AtkDef'], player_stats[1])
    # AtkMid1-3 is on top
    data = data.replace(player_types['AtkFor'], player_stats[3])
    data = data.replace(player_types['DefKep'], player_stats[4])

    result_file.write(data)

    result_file.close()


def __main__():
    matches_dir = "../datasets/matches/"
    specific_match_columns = ['match_url', 'home_xi_sofifa_ids', 'away_xi_sofifa_ids', 'home_formation',
                              'away_formation', 'home_sequence', 'away_sequence']
    for file_loc in os.listdir(matches_dir):
        match_file = matches_dir + file_loc
        year = file_loc.split('_')
        year_str = year[-1].split('.csv')[0]
        df = pd.read_csv(match_file, engine='pyarrow', usecols=specific_match_columns)

        pcsp_path = './pcsp_files'
        if not os.path.exists(pcsp_path):
            os.mkdir(pcsp_path)

        i = 0
        while i < df.shape[0]:
            team_arr = ["home", "away"]
            record = df.iloc[i]
            for team in team_arr:
                field_grid = get_soccer_field_grid(record, team)
                print(field_grid)
                match_url = record.loc["match_url"]
                match_url = match_url.split('/match/')
                match_id = match_url[-1]

                replace_file_content(record, match_id, team, field_grid, year_str)

            i = i + 1


if __name__ == '__main__':
    __main__()

# actual result : matches["home_goals", "away_goals"]
