import pandas as pd

def set_col_names(df):

    result_df = df.copy()
    col_names = list(result_df.iloc[0])
    dash_indexes = [i for i, x in enumerate(col_names) if x == '-']

    for i, dash_index in enumerate(dash_indexes):
        col_names[dash_index] = col_names[dash_index] + '_' + str(i)
    
    result_df = result_df.iloc[1:]
    result_df.columns = col_names
    result_df.drop(columns = ['-_0', '-_1', '-_2'], inplace = True)
    
    return result_df

def calc_unrounded_ratings(df):

    result_df = df.copy()

    result_df['W'] = result_df['W'].astype('int')
    result_df['OW'] = result_df['OW'].astype('int')
    result_df['OOW'] = result_df['OOW'].astype('int')
    result_df['L'] = result_df['L'].astype('int')
    result_df['OL'] = result_df['OL'].astype('int')
    result_df['OOL'] = result_df['OOL'].astype('int')

    result_df['Win%'] = result_df['W']/(result_df['W'] + result_df['L'])
    result_df['OWin%'] = result_df['OW']/(result_df['OW'] + result_df['OL'])
    result_df['OOWin%'] = result_df['OOW']/(result_df['OOW'] + result_df['OOL'])
    result_df['CPI'] = (result_df['Win%'] ** 3) * (result_df['OWin%'] ** 2) * (result_df['OOWin%']) * 100

    return result_df

def get_cpi_df(year):

    cpi_tables = pd.read_html(f"http://www.cpiratings.com/archives/{year}post_table.html")
    cpi_df = cpi_tables[0]

    cpi_df = set_col_names(cpi_df)
    cpi_df = calc_unrounded_ratings(cpi_df)

    cpi_df = cpi_df[['Team', 'CPI', 'W', 'L', 'OW', 'OL', 'OOW', 'OOL']].reset_index(drop = True)
    cpi_df['Year'] = year
    cpi_df['Team'] = cpi_df['Team'].apply(lambda x: x.replace('CFP', ""))
    cpi_df['Team'] = cpi_df['Team'].apply(lambda x: x.replace('AP', ""))
    cpi_df['Team'] = cpi_df['Team'].apply(lambda x: x.replace('BCS', ""))
    cpi_df['Team'] = cpi_df['Team'].apply(lambda x: x.replace('(', ""))
    cpi_df['Team'] = cpi_df['Team'].apply(lambda x: x.replace(')', ""))
    cpi_df['Team'] = cpi_df['Team'].apply(lambda x: x.replace(',', ""))
    cpi_df['Team'] = cpi_df['Team'].apply(lambda x: x.strip())

    return cpi_df

def get_cpi_by_years(years):

    cpi_list = [get_cpi_df(year) for year in years]

    result_df = pd.concat(cpi_list, ignore_index=True,axis=0)
    result_df.reset_index(drop = True, inplace = True)

    return result_df

test = get_cpi_by_years([2018])

test[test['Year'] == 2018].head()

