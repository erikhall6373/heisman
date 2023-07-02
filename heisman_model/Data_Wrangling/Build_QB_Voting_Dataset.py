import time
import pandas as pd
from Data_Wrangling import Quarterback_Voting


for i in range(2006, 2020, 1):

    if i == 2006:

        quarterback_voting_df = Quarterback_Voting.get_quarterback_voting_data([i])
    
    elif i > 2006:

        time.sleep(5)
        current_df = Quarterback_Voting.get_quarterback_voting_data([i])
        quarterback_voting_df = pd.concat([quarterback_voting_df, current_df], ignore_index=True ,axis=0)


quarterback_voting_df.to_csv("Data\QB_Voting_Data.csv", index = False)