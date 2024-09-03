import pandas as pd
import numpy as np
import pickle
import statsmodels.api as sm

model_path = "C:\\Users\\noodl\\Repos\\heisman\\Shiny_App\\heisman_model.pkl"
weekly_data_path = "C:\\Users\\noodl\\Repos\\heisman\\Data\\Weekly_Data.csv"

model = pd.read_pickle(model_path)

################### Current #########################
current_df = pd.read_csv("Data\Weekly_Data.csv").reset_index(drop = True)

current_predict_df =  current_df[['Passing_Rate', 'Passing_TD', 'Rushing_TD', 'Power5', 'CPI']]
current_predict_df = sm.tools.add_constant(current_predict_df)
current_predict_df['Projected_Voting_Points'] = model.predict(current_predict_df)
current_predict_df = current_predict_df['Projected_Voting_Points']

current_df = pd.merge(current_df, current_predict_df, left_index=True, right_index=True)
current_df['CPI'] = current_df['CPI'].round(2)
current_df['Projected_Voting_Points'] = current_df['Projected_Voting_Points'].round(2)

#current_df.to_csv("C:\\Users\\noodl\\Repos\\heisman\\Data\\Weekly_Data_Predict.csv", index = False)

current_df.to_csv("Data\Weekly_Data_Predict.csv", index = False)