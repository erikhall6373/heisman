import sys
import os
import pandas as pd
import numpy as np

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)

from heisman_project.heisman_model.Data_Wrangling import Quarterback_Stats
from heisman_project.heisman_model.Data_Wrangling import CPI_Ratings
from heisman_project.heisman_model.Data_Cleaning import model_data_clean

os.remove('./Data/Weekly_Data.csv')

analysis_cols = ['Player', 'School', 'Passing_Rate', 'Passing_TD', 'Rushing_TD', 'Power5', 'CPI']
power5 = ['ACC', 'Big 12', 'Big Ten', 'Pac-10', 'Pac-12', 'SEC']

qb_stats_df = Quarterback_Stats.get_cfb_ref_passing_data(2022)
qb_stats_df = qb_stats_df[qb_stats_df['School'] != 'School']
cpi_df = CPI_Ratings.get_cpi_df(2022)

cpi_df = model_data_clean.cpi_cleaning(cpi_df)


weekly_df = qb_stats_df.merge(cpi_df, how = 'inner', on = ['School', 'Year'])
weekly_df['Player'] = weekly_df['Player'].apply(lambda x: x.replace("*", ""))
weekly_df['Power5'] = weekly_df['Conf'].apply(lambda x: 1 if x in power5 else 0)

weekly_df['Power5'] = np.where(weekly_df['School'] == 'Notre Dame', 1, weekly_df['Power5'])
weekly_df = weekly_df[analysis_cols]

weekly_df.to_csv(os.path.join('./Data/Weekly_Data.csv'), index = False)

