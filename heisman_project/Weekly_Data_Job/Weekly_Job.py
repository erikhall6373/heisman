import sys
import os
import pandas as pd
import numpy as np
import shutil

#project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#sys.path.append(project_path)

from heisman_project.heisman_model.Data_Wrangling import Quarterback_Stats
from heisman_project.heisman_model.Data_Wrangling import CPI_Ratings
from heisman_project.heisman_model.Data_Cleaning import model_data_clean
from heisman_project.heisman_model.Data_Wrangling import Get_Weekly_Win_Percent

if os.path.exists('./Data/Weekly_Data.csv'):
    os.remove('./Data/Weekly_Data.csv')

if os.path.exists('./Shiny_App/Weekly_Data.csv'):
    os.remove('./Shiny_App/Weekly_Data.csv')

if os.path.exists('./docs'):
    shutil.rmtree('./docs')

analysis_cols = ['Player', 'School', 'Passing_Rate', 'Passing_TD', 'Rushing_TD', 'Power5', 'CPI']
power5 = ['ACC', 'Big 12', 'Big Ten', 'Pac-10', 'Pac-12', 'SEC']

qb_stats_df = Quarterback_Stats.create_qb_model_features(2024)
qb_stats_df = qb_stats_df[qb_stats_df['School'] != 'School']
#cpi_df = CPI_Ratings.current_cpi_df(2023)

#cpi_df = model_data_clean.cpi_cleaning(cpi_df)

cpi_df = Get_Weekly_Win_Percent.calculate_winning_percent(2024)
cpi_df['CPI'] = (cpi_df['Winning_Percent'] * 0.25) * 100
cpi_df = cpi_df[['School', 'Year', 'CPI']]

weekly_df = qb_stats_df.merge(cpi_df, how = 'inner', on = ['School', 'Year'])
weekly_df['Player'] = weekly_df['Player'].apply(lambda x: x.replace("*", ""))
weekly_df['Power5'] = weekly_df['Conf'].apply(lambda x: 1 if x in power5 else 0)

weekly_df['Power5'] = np.where(weekly_df['School'] == 'Notre Dame', 1, weekly_df['Power5'])
weekly_df['Power5'] = np.where(weekly_df['School'] == 'Washington State', 0, weekly_df['Power5'])
weekly_df['Power5'] = np.where(weekly_df['School'] == 'Oregon State', 0, weekly_df['Power5'])
weekly_df = weekly_df[analysis_cols]

weekly_df.to_csv(os.path.join('./Data/Weekly_Data.csv'), index = False)
weekly_df.to_csv(os.path.join('./Shiny_App/Weekly_Data.csv'), index = False)


