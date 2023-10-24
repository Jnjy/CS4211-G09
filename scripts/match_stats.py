import pandas as pd
import sys
import player_stats


def get_match_stats_by_id(df, match_id):
    # df = pd.read_csv(file_path, engine='pyarrow')
    home_sofifa_ids = list(int(float(x)) for x in df['home_xi_sofifa_ids'].split(','))
    away_sofifa_ids = list(int(float(x)) for x in df['away_xi_sofifa_ids'].split(','))
    return home_sofifa_ids, away_sofifa_ids


def group_players_by_lineup(df, match_id):
    # df = pd.read_csv(file_path, engine='pyarrow')
    url = f'https://www.premierleague.com/match/{match_id}'
    home_line_up, away_line_up = process_lineup(df['home_formation']), process_lineup(
        df['away_formation'])
    print(f"For match id: {match_id}\n", "Home line up -> ", home_line_up, "Away line up -> ", away_line_up)
    return home_line_up, away_line_up


def process_lineup(lineup):
    if len(lineup.split('-')) != 1:
        result = list(int(x) for x in lineup.split('-'))
        return result
    else:
        result = []
        arr = lineup.split('/')
        result += list(int(x) for x in arr[:-1])
        result.append(int(arr[-1]) % 1000)
        return result


def read_match_and_generate_stats(df, match_id, year, team):
    assert team in ('away', 'home'), "team has to be either 'away' or 'home' !"
    if team == 'away':
        home_ids, away_ids = get_match_stats_by_id(df, match_id)
        h_lineup, a_lineup = group_players_by_lineup(df, match_id)

        # Start getting player stats
        home_stats = player_stats.get_player_stats_by_ids(year, home_ids, is_away_team=False, lineup=h_lineup)
        away_stats = player_stats.get_player_stats_by_ids(year, away_ids, is_away_team=True, lineup=a_lineup)
        return home_stats, away_stats, h_lineup, a_lineup
    if team == 'home':
        away_ids, home_ids = get_match_stats_by_id(df, match_id)
        a_lineup, h_lineup = group_players_by_lineup(df, match_id)

        # Start getting player stats
        home_stats = player_stats.get_player_stats_by_ids(year, home_ids, is_away_team=False, lineup=h_lineup)
        away_stats = player_stats.get_player_stats_by_ids(year, away_ids, is_away_team=True, lineup=a_lineup)
        return home_stats, away_stats, h_lineup, a_lineup


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
