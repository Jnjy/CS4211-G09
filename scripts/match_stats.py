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

# Run from project root
# python ./scripts/match_stats.py ./datasets/matches/epl_matches_20152016.csv 12115
def __main__():
  arguments = sys.argv[1:]
  home_ids, away_ids = get_match_stats_by_id(arguments[0], int(arguments[1]))
  _, _ = player_stats.get_player_stats_by_ids("20152016", home_ids, is_away_team=False), player_stats.get_player_stats_by_ids("20152016", away_ids, is_away_team=True)

if __name__ == '__main__':
  __main__()  