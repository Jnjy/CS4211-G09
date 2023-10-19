import copy
import os
import pandas as pd
from template_enum import player_position_row, soccer_field_grid

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
    row_index = 0 # row index in formation
    formation_row_index = 0 # row index in processed formation -- 1 def, 1 for, remaining mid
    for x in formation:
        y = 0

        row_formation = copy.deepcopy(template)
        while (y < int(x)):
            pos = player_position_row.get(sequence[i])

            row_formation[pos] = 1
            
            y = y + 1 # index of players
            i = i + 1 # index of player positions "L", "LR", "CL", "C", "CR", "RL", "R"
        
        if (row_index != 0 and row_index != len(formation)-1):
            entire_formation[formation_row_index].append(row_formation)
            
        else: 
            entire_formation[formation_row_index] = row_formation
            formation_row_index = formation_row_index + 1


        if (row_index == len(formation)-2): 
            formation_row_index = formation_row_index + 1
            
        row_index = row_index + 1

    return entire_formation

def replace_file_content(match_id, team, grid_formation):
    template_file = open('./template.pcsp', 'rt')
    data = template_file.read()
    template_file.close()

    result_file = open(f'./pcsp_files/{match_id}_{team}.pcsp', 'wt')
    data = data.replace(soccer_field_grid["ATKDEFPOS"], str(grid_formation[0]))
    data = data.replace(soccer_field_grid["ATKMIDPOS"], str(grid_formation[1]))
    data = data.replace(soccer_field_grid["ATKFORPOS"], str(grid_formation[2]))

    result_file.write(data)

    result_file.close()

def __main__():
    matches_dir = "./datasets/matches/"
    for file_loc in os.listdir(matches_dir):
        match_file = matches_dir + file_loc
        df = pd.read_csv(match_file)

        pcsp_path = './pcsp_files'
        if not os.path.exists(pcsp_path):
            os.mkdir(pcsp_path)

        i = 0
        while (i < df.shape[0]):
            team_arr = ["home", "away"]
            for team in team_arr:
                record = df.iloc[i]
                field_grid = get_soccer_field_grid(record, team)

                match_url = record.loc["match_url"]
                match_url = match_url.split('/match/')
                match_id = match_url[-1]

                replace_file_content(match_id, team, field_grid)

            i = i + 1



if __name__ == '__main__':
    __main__()

# actual result : matches["home_goals", "away_goals"]