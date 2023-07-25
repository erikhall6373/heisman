import time
import pandas as pd
from Data_Wrangling import Quarterback_Stats


for i in range(2006, 2020, 1):

    if i == 2006:

        quarterback_stats_df = Quarterback_Stats.get_qb_stats_by_years([i])
    
    elif i > 2006:

        time.sleep(5)
        current_df = Quarterback_Stats.get_qb_stats_by_years([i])
        quarterback_stats_df = pd.concat([quarterback_stats_df, current_df], ignore_index=True ,axis=0)


quarterback_stats_df.to_csv("Data\QB_Stats_Data.csv", index = False)