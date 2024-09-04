from pathlib import Path

import pandas as pd
import statsmodels.api as sm

app_dir = Path(__file__).parent

################### Model Object #########################

model = pd.read_pickle(app_dir / "heisman_model.pkl")

################### Historical #########################
model_data = pd.read_csv(app_dir / "Model_Data.csv").reset_index(drop = True)

predict_data =  model_data[['Passing_Rate', 'Passing_TD', 'Rushing_TD', 'Power5', 'CPI']]
predict_data = sm.tools.add_constant(predict_data)
predict_data['Prediction'] = model.predict(predict_data)
predict_data = predict_data['Prediction']

model_data = pd.merge(model_data, predict_data, left_index=True, right_index=True)
model_data['CPI'] = model_data['CPI'].round(2)
model_data['Prediction'] = model_data['Prediction'].round(2)


################### Current #########################
current_df = pd.read_csv(app_dir / "Weekly_Data.csv").reset_index(drop = True)

current_predict_df =  current_df[['Passing_Rate', 'Passing_TD', 'Rushing_TD', 'Power5', 'CPI']]
current_predict_df = sm.tools.add_constant(current_predict_df)
current_predict_df['Projected Voting Points'] = model.predict(current_predict_df)
current_predict_df = current_predict_df['Projected Voting Points']

current_df = pd.merge(current_df, current_predict_df, left_index=True, right_index=True)
current_df['CPI'] = current_df['CPI'].round(2)
current_df['Projected Voting Points'] = current_df['Projected Voting Points'].round(2)


################### Top 10 HTML #########################

with open(app_dir / "weekly.html", 'r') as file:  # r to open file in READ mode
    html_top10_string = file.read()