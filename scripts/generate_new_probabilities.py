import pandas as pd
import numpy as np


def update_season_probabilities(year_range: int):
    df_new = pd.read_csv(f"./betting_simulation/original_probabilities/{year_range}.csv")
    df_generated_prob = pd.read_csv(f"./data_output/generated_probabilities/{year_range}.csv", encoding="utf-8")
    print(len(df_new), len(df_generated_prob))
    for index, row in df_generated_prob.iterrows():
        if row['team'] == 'home':
            match_url = row['match_url']
            try:
                home_away_midpt_probs = process_prob([float(row['low']), float(row['high'])],
                                                 [float(df_generated_prob.at[index - 1, 'low']),
                                                  float(df_generated_prob.at[index - 1, 'high'])])
            except:
                print("error, using old values")
                continue
            softmax_val = softmax(home_away_midpt_probs)
            df_new.loc[df_new['match_url'] == match_url, 'home_prob_softmax'] = softmax_val[0]

    print(len(df_new))
    df_new.to_csv(f"./betting_simulation/new_probabilities/{year_range}.csv", mode='w', index=False)


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def process_prob(home_prob_range, away_prob_range):
    home_midpoint = sum(home_prob_range) / 2
    away_midpoint = sum(away_prob_range) / 2
    return [home_midpoint, away_midpoint]


if __name__ == '__main__':
    seasons = [1516, 1617, 1718, 1819, 1920, 2021]  # 1617, 1718, 1819, 1920, 2021
    for season in seasons:
        update_season_probabilities(season)
