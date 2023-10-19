import pandas as pd
from match_stats import process_lineup

formation_set = set()
for year in ["20152016", "20162017", "20172018", "20182019"]:
    df = pd.read_csv(f"./datasets/matches/epl_matches_{year}.csv")
    # print(df['home_formation'])

    for form in df['home_formation']:
        formation_set.add(form)

print(len(formation_set))