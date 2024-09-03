import pandas as pd

def clean_cfb_ref_passing_data(ref_df):

    #cfb_ref_columns = ['Rk', 'Player', 'School', 'Conf', 'G',
    #'Passing_Cmp', 'Passing_Att', 'Passing_Pct', 'Passing_Yds',
    #'Passing_Y/A', 'Passing_AY/A', 'Passing_TD', 'Passing_Int', 'Passing_Rate',
    #'Rushing_Att', 'Rushing_Yds', 'Rushing_Avg', 'Rushing_TD']

    cfb_ref_columns = ['Rk', 'Player', 'School', 'Conf', 'G',
    'Passing_Cmp', 'Passing_Att', 'Passing_Pct', 'Passing_Yds', 'Passing_TD', 'Passing_TD_Percent',
    'Passing_Int', 'Passing_Int_Percent', 'Passing_Y/A', 'Passing_AY/A', 'Passing_Y/C',
    'Passing_Y/G', 'Passing_Rate', 'Awards']

    power5 = ['ACC', 'Big 12', 'Big Ten', 'Pac-10', 'Pac-12', 'SEC']

    result_df = ref_df.copy()

    result_df.columns = cfb_ref_columns
    result_df['Player'] = result_df['Player'].apply(lambda x: x.replace("*", ""))
    result_df['Power5'] = result_df['Conf'].apply(lambda x: 1 if x in power5 else 0)

    return result_df

def clean_cfb_ref_scoring_data(ref_df):

    cfb_ref_columns = ['Rk', 'Player', 'School', 'Conf', 'G',
    'Rushing_TD', 'Receiving_TD', 'Int_TD', 'FR_TD',
    'PR_TD', 'KR_TD', 'Oth_TD', 'Total_TD',
    'Kicking_XPM', 'Kicking_FGM', 'Other_2PM', 'Other_Sfty', 'Total_Points']

    power5 = ['ACC', 'Big 12', 'Big Ten', 'Pac-10', 'Pac-12', 'SEC']

    result_df = ref_df.copy()

    result_df.columns = cfb_ref_columns
    result_df['Player'] = result_df['Player'].apply(lambda x: x.replace("*", ""))
    result_df['Power5'] = result_df['Conf'].apply(lambda x: 1 if x in power5 else 0)

    return result_df

def get_cfb_ref_passing_data(year):

    data = pd.read_html(f"https://www.sports-reference.com/cfb/years/{year}-passing.html")
    result_df = data[0]

    result_df = clean_cfb_ref_passing_data(result_df)
    result_df['Year'] = year
    result_df = result_df[result_df['Player'] != 'Player']
    result_df = result_df[result_df['Player'] != 'League Average']

    return result_df

def get_cfb_ref_scoring_data(year):

    data = pd.read_html(f"https://www.sports-reference.com/cfb/years/{year}-scoring.html")
    result_df = data[0]

    result_df = clean_cfb_ref_scoring_data(result_df)
    result_df['Year'] = year
    result_df = result_df[result_df['Player'] != 'Player']
    result_df = result_df[result_df['Player'] != 'League Average']

    return result_df


def get_school_games(year):

  cfb_ref_columns = ['Rk', 'School', 'Conf', 'Overall_W', 'Overall_L', 'Overall_Pct'
    'Conf_W', 'Conf_L', 'Conf_Pct', 'Off_Points', 'Def_Points', 'SRS', 'SOS', 'AP_Pre', 'AP_High', 'AP_Rank', 'Notes', 'Blank']

  data = pd.read_html(f"https://www.sports-reference.com/cfb/years/{year}-standings.html")
  result_df = data[0]

  result_df.columns = cfb_ref_columns

  result_df = result_df[result_df['Overall_W'] != 'W']
  result_df = result_df[result_df['Overall_W'] != 'Overall']



  result_df = result_df.astype({'School' : 'str', 'Conf' : 'str', 'Overall_W' : 'float64', 'Overall_L' : 'float64'})

  result_df['School_Games'] = result_df['Overall_W'] + result_df['Overall_L']
  result_df['School_Games'] = result_df['School_Games'].fillna(0)
  result_df = result_df.astype({'School_Games' : 'int64'})

  result_df['Year'] = year
  result_df = result_df[['School', 'Conf', 'Year', 'School_Games']]


  return result_df


def create_qb_model_features(year):

  passing_cols = ['Player', 'School', 'Conf', 'G', 'Passing_Rate', 'Passing_TD', 'Power5', 'Year', 'Passing_Att']
  rushing_cols = ['Player', 'School', 'Conf', 'G', 'Rushing_TD', 'Power5', 'Year']

  passing_df = get_cfb_ref_passing_data(year)
  scoring_df = get_cfb_ref_scoring_data(year)
  games_df = get_school_games(year)

  passing_df = passing_df[passing_cols]
  rushing_df = scoring_df[rushing_cols]

  passing_df = passing_df.astype({'Player': 'str', 'School' : 'str', 'Conf' : 'str',
                                  'G' : 'float64', 'Passing_Rate' : 'float64', 'Passing_TD' : 'float64',
                                  'Power5' : 'int64', 'Year' : 'int64', 'Passing_Att' : 'float64'})
  rushing_df = rushing_df.astype({'Player': 'str', 'School' : 'str', 'Conf' : 'str',
                                  'G' : 'float64', 'Rushing_TD' : 'float64',
                                  'Power5' : 'int64', 'Year' : 'int64'})

  passing_df = pd.merge(passing_df, games_df, on = ['School', 'Conf', 'Year'])
  passing_df['Majority_Games'] = passing_df['School_Games'] * 0.75
  passing_df = passing_df[passing_df['G'] >= passing_df['Majority_Games']].drop(columns = ['School_Games', 'Majority_Games'])

  passing_df['ATT/G'] = passing_df['Passing_Att'] / passing_df['G']
  passing_df = passing_df[passing_df['ATT/G'] >= 14].drop(columns = ['ATT/G', 'Passing_Att'])
  qb_df = pd.merge(passing_df, rushing_df, on=['Player', 'School', 'Conf', 'G', 'Power5', 'Year'], how = 'left')
  qb_df['Rushing_TD'] = qb_df['Rushing_TD'].fillna(0)

  return qb_df

def get_qb_stats_by_years(years):

    stats_list = [create_qb_model_features(year) for year in years]

    result_df = pd.concat(stats_list, ignore_index=True,axis=0)
    result_df.reset_index(drop = True, inplace = True)

    return result_df


#test = get_qb_stats_by_years([2016])



