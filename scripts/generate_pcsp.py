import sys


def generate_pcsp(match_id, side):
    team_side = "away"
    if side != "away":
        team_side = "home"
    file_name = f"{match_id}_{team_side}.pcsp"
    file_path = "./scripts/init_definitions/"
    player_positions = file_path+"player_positions.txt"
    ball_receive_positions_and_player_actions = \
        file_path+"ball_receive_positions_and_player_actions.txt"

    with open(player_positions) as f:
        lines_1 = f.readlines()
    with open(ball_receive_positions_and_player_actions) as f:
        lines_2 = f.readlines()
    initial_lines = lines_1 + lines_2
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
