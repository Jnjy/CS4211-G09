import pandas as pd
import sys
import player_stats


def get_match_stats_by_id(file_path, match_id):
    df = pd.read_csv(file_path)
    url = f'https://www.premierleague.com/match/{match_id}'
    df = df[df['match_url'] == url]
    home_sofifa_ids = list(int(float(x)) for x in df['home_xi_sofifa_ids'].values[0].split(','))
    away_sofifa_ids = list(int(float(x)) for x in df['away_xi_sofifa_ids'].values[0].split(','))
    return home_sofifa_ids, away_sofifa_ids


def group_players_by_lineup(file_path, match_id):
    df = pd.read_csv(file_path)
    url = f'https://www.premierleague.com/match/{match_id}'
    df = df[df['match_url'] == url]
    home_line_up, away_line_up = process_lineup(df['home_formation'].values[0]), process_lineup(
        df['away_formation'].values[0])
    print(f"For match id: {match_id}\n", "Home line up -> ", home_line_up, "Away line up -> ", away_line_up)
    return home_line_up, away_line_up


def process_lineup(lineup):
    if len(lineup.split('-')) != 1:
        return list(int(x) for x in lineup.split('-'))
    else:
        result = []
        arr = lineup.split('/')
        result += list(int(x) for x in arr[:-1])
        result.append(int(arr[-1]) % 1000)
        return result


def read_match_and_generate_stats(match_id, year):
    file_path = f"./datasets/matches/epl_matches_{year}.csv"
    home_ids, away_ids = get_match_stats_by_id(file_path, match_id)
    h_lineup, a_lineup = group_players_by_lineup(file_path, match_id)

    # Start getting player stats
    home_stats = player_stats.get_player_stats_by_ids(year, home_ids, is_away_team=False, lineup=h_lineup)
    away_stats = player_stats.get_player_stats_by_ids(year, away_ids, is_away_team=True, lineup=a_lineup)
    return home_stats, away_stats


# Run from project root
# python ./scripts/match_stats.py ./datasets/matches/epl_matches_20152016.csv 12115
def __main__():
    arguments = sys.argv[1:]
    home_ids, away_ids = get_match_stats_by_id(arguments[0], int(arguments[1]))
    h_lineup, a_lineup = group_players_by_lineup(arguments[0], int(arguments[1]))

    # Start getting player stats
    player_stats.get_player_stats_by_ids("20172018", home_ids, is_away_team=False, lineup=h_lineup)
    player_stats.get_player_stats_by_ids("20172018", away_ids, is_away_team=True, lineup=a_lineup)


if __name__ == '__main__':
    __main__()
