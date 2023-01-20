import pandas as pd

def clean_cfb_ref_passing_data(ref_df):

    cfb_ref_columns = ['Rk', 'Player', 'School', 'Conf', 'G',
    'Passing_Cmp', 'Passing_Att', 'Passing_Pct', 'Passing_Yds',
    'Passing_Y/A', 'Passing_AY/A', 'Passing_TD', 'Passing_Int', 'Passing_Rate',
    'Rushing_Att', 'Rushing_Yds', 'Rushing_Avg', 'Rushing_TD']

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

    return result_df

def get_qb_stats_by_years(years):

    stats_list = [get_cfb_ref_passing_data(year) for year in years]

    result_df = pd.concat(stats_list, ignore_index=True,axis=0)
    result_df.reset_index(drop = True, inplace = True)

    return result_df

test = get_qb_stats_by_years([2018, 2019])

test['Year'].value_counts()

