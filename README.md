# CS4211-G09

## How to use the scripts to extract informatin on a player?
1. Get the player sofifa_id
2. In the project root directory, run `python ./scripts/player_stats.py ./datasets/ratings/epl_ratings_20152016.csv <player_id>`
3. Unlike match stats, player stats will be printed to console.

## How to use the scripts to extract information on a match?
1. Get the match id e.g. `12115`
2. In the project root directory, run `python ./scripts/match_stats.py ./datasets/matches/epl_matches_20152016.csv 12115`
3. Data of the match based on Home and Away teams will be output to the respective text files contained in `./data_output` folder.