import pandas as pd
import numpy as np
import pickle
import statsmodels.api as sm

model_path = ""
weekly_data_path = ""

model = pickle.load(open(model_path, 'rb'))

################### Current #########################
current_df = pd.read_csv(weekly_data_path).reset_index(drop = True)

current_predict_df =  current_df[['Passing_Rate', 'Passing_TD', 'Rushing_TD', 'Power5', 'CPI']]
current_predict_df = sm.tools.add_constant(current_predict_df)
current_predict_df['Projected Voting Points'] = model.predict(current_predict_df)
current_predict_df = current_predict_df['Projected Voting Points']

current_df = pd.merge(current_df, current_predict_df, left_index=True, right_index=True)
current_df['CPI'] = current_df['CPI'].round(2)
current_df['Projected Voting Points'] = current_df['Projected Voting Points'].round(2)

current_df.to_csv("")