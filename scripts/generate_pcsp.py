import sys
from match_stats import read_match_and_generate_stats


def generate_pcsp(match_id, side, year_range="20152016"):
    team_side = "away"
    if side != "away":
        team_side = "home"
    formation = "4-3-3"
    file_name = f"{match_id}_{team_side}.pcsp"
    file_path = "./scripts/template"
    player_positions = f"{file_path}/player_positions.txt"
    ball_receive_positions_and_player_actions = f"{file_path}/ball_receive_positions_and_player_actions.txt"
    soccer_field_grid = f"{file_path}/grids/Grid-{formation}.txt"
    probabilities = f"{file_path}/probabilities/{formation}.txt"
    home_stats, away_stats = read_match_and_generate_stats(match_id, year_range)
    placeholder_values = away_stats + [home_stats[0],]
    print(placeholder_values)

    with open(player_positions) as f:
        lines_1 = f.readlines()
    with open(ball_receive_positions_and_player_actions) as f:
        lines_2 = f.readlines()
    with open(soccer_field_grid) as f:
        lines_3 = f.readlines()
    with open(probabilities) as f:
        lines_4 = f.readlines()
        lines_4_edited = []
        for line in lines_4:
            num_placeholders = line.count("{}")
            to_place = []
            print(line, len(placeholder_values))
            print(placeholder_values)
            for i in range(num_placeholders):
                if len(placeholder_values) > 0:
                    to_place.append(placeholder_values.pop(0))
                else:  # Not enough placeholders, check if stats are retrieved correctly
                    print("Not enough placeholders, check if stats are retrieved correctly")
                    to_place.append(-1)
            lines_4_edited.append(line.format(*to_place))
    initial_lines = lines_1 + lines_2 + lines_3 + lines_4_edited
    with open(file_name, 'w') as f:
        for line in initial_lines:
            f.write(line)


# Generate PCSP -> python3
def main():
    arguments = sys.argv[1:]
    if len(arguments) < 2:
        print("Usage -> python3 generate_pcsp.py <match_id> away")
        return
    generate_pcsp(arguments[0], arguments[1])


if __name__ == "__main__":
    main()
