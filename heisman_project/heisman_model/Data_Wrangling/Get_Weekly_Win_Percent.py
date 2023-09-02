import pandas as pd
import numpy as np


def calculate_winning_percent(year):

    win_loss_list = pd.read_html(f"https://www.sports-reference.com/cfb/years/{year}-standings.html")
    win_loss_df = win_loss_list[0]

    win_loss_df.columns = ['Rk', 'School', 'Conf', 'Overall_W', 'Overall_L', 'Overall_Pct', 'Conference_W', 
                           'Conference_L', 'Conference_Pct', 'Points_Per_Game_Off', 'Points_Per_Game_Def', 
                           'SRS_SRS', 'SRS_SOS', 'Polls_AP_Curr', 'Polls_AP_Pre', 'Polls_AP_High', 'Notes']
    
    win_loss_df = win_loss_df[['School', 'Overall_W', 'Overall_L']]
    win_loss_df = win_loss_df[win_loss_df['School'] != 'School']
    win_loss_df = win_loss_df[win_loss_df['Overall_W'] != 'Overall']

    win_loss_df ['Overall_W'] = pd.to_numeric(win_loss_df ['Overall_W'])
    win_loss_df ['Overall_L'] = pd.to_numeric(win_loss_df ['Overall_L'])

    win_loss_df['Winning_Percent'] = win_loss_df['Overall_W']/(win_loss_df['Overall_W'] + win_loss_df['Overall_L'])

    win_loss_df['Year'] = year

    return win_loss_df[['School', 'Winning_Percent', 'Year']]