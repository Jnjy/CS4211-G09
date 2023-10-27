import pandas as pd

seasons = [1516, 1617, 1718, 1819, 1920, 2021]
unique_formations = []
for season in seasons:
    prob_df = pd.read_csv(f'./data_output/generated_probabilities/{season}.csv')
    match_df = pd.read_csv(f'./datasets/matches/epl_matches_20{str(season)[:2]}20{str(season)[2:]}.csv')
    error_dfs = prob_df[prob_df['low'] == 'error']
    error_analysis_df = pd.merge(error_dfs, match_df, on="match_url", how="inner")
    unique_formations.extend(error_analysis_df['home_formation'])
    unique_formations.extend(error_analysis_df['away_formation'])
    error_3511_df = error_analysis_df[error_analysis_df['home_formation'] == '5-3-2']
    error_3511_df.to_csv(f'error_3511_{season}.csv')
    # print(len(error_3511_df))
    error_analysis_df.to_csv(f'error_analysis_{season}.csv')

    prob_df['low'] = pd.to_numeric(prob_df['low'], errors='coerce')
    prob_df['high'] = pd.to_numeric(prob_df['high'], errors='coerce')
    less_than_zero_df = prob_df[prob_df['low'] < 0.0000]
    more_than_zero_df = prob_df[prob_df['high'] > 1.0000]
    more_than_zero_df.merge(less_than_zero_df).to_csv(f'err_more_less_than_zero_{season}.csv')
print(f"Unique Formations -> {set(unique_formations)}")
