import pandas as pd
import numpy as np
import statsmodels.api as sm
import pickle


model_data = pd.read_csv("Data\Model_Data.csv")
model_data = model_data[model_data['Year'] <= 2018]
predictors = ['Passing_Rate', 'Passing_TD', 'Rushing_TD', 'Power5', 'CPI']
response = ['points_won']


heisman_model = sm.OLS(model_data[response], sm.tools.add_constant(model_data[predictors])).fit()

#print(heisman_model.summary())

#print(heisman_model.params)
with open('Modeling\heisman_model.pkl','wb') as f:
    pickle.dump(heisman_model,f)

#model = pickle.load(open('Modeling\heisman_model.pkl', 'rb'))

