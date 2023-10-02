import sys
import pandas as pd

def get_player_stats_by_id(file_path, player_id):
  df = pd.read_csv(file_path)
  df = df[df['sofifa_id'] == player_id]
  return df

def get_player_stats_by_ids(year="20152016", player_ids=[], is_away_team=False):
  file_path=f"./datasets/ratings/epl_ratings_{year}.csv"
  target_file = "./data_output/match_player_stats_away.txt" if is_away_team else "./data_output/match_player_stats_home.txt"
  with open(target_file, "w") as file:
    sys.stdout = file
    for player_id in player_ids:
      output_player_stats(get_player_stats_by_id(file_path, player_id))
    
    sys.stdout = sys.__stdout__
    

def output_player_stats(df):
  print("Player Name -> ", df['long_name'].values[0])
  print("Club Name -> ", df['club_name'].values[0])
  print("Short Pass -> ", df['attacking_short_passing'].values[0])
  print("Long Pass -> ", df['skill_long_passing'].values[0])
  print("Dribble -> ", df['skill_dribbling'].values[0])
  print("Attacking Crossing -> ", df['attacking_crossing'].values[0])
  print("Attacking Finishing -> ", df['attacking_finishing'].values[0])
  print("Attacking Heading -> ", df['attacking_heading_accuracy'].values[0])
  print("Attacking Volleys -> ", df['attacking_volleys'].values[0])
  print("Attacking FK Accuracy -> ", df['skill_fk_accuracy'].values[0])
  
  print("\n###### Goal Keeping Stats ######")
  print("Goal Keeping Diving -> ", df['goalkeeping_diving'].values[0])
  print("Goal Keeping Handling -> ", df['goalkeeping_handling'].values[0])
  print("Goal Keeping Kicking -> ", df['goalkeeping_kicking'].values[0])
  print("Goal Keeping Positioning -> ", df['goalkeeping_positioning'].values[0])
  print("Goal Keeping Reflexes -> ", df['goalkeeping_reflexes'].values[0], "\n")

# run from project root
# python ./scripts/player_stats.py ./datasets/ratings/epl_ratings_20152016.csv 9014
def __main__():
  arguments = sys.argv[1:]
  output_player_stats(get_player_stats_by_id(arguments[0], int(arguments[1])))
  

if __name__ == '__main__':
  __main__()