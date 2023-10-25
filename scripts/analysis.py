import pandas as pd

seasons = [1516, 1617, 1718, 1819, 1920, 2021]

for season in seasons:
    prob_df = pd.read_csv(f'./data_output/generated_probabilities/{season}.csv')
    match_df = pd.read_csv(f'./datasets/matches/epl_matches_20{str(season)[:2]}20{str(season)[2:]}.csv')
    error_dfs = prob_df[prob_df['low'] == 'error']
    error_analysis_df = pd.merge(error_dfs, match_df, on="match_url", how="inner")
    print(error_analysis_df)
    error_analysis_df.to_csv(f'error_analysis_{season}.csv')
