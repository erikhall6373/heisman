import pandas as pd
from Data_Wrangling import CPI_Ratings

def build_2011_cpi_df():

    cpi_tables_2011 = pd.read_html(f"http://www.cpiratings.com/archives/2011post_table.html")

    cpi_2011_df = cpi_tables_2011[0]
    col_names = list(cpi_2011_df.iloc[0])

    cpi_2011_df = cpi_2011_df.iloc[1:].copy()
    cpi_2011_df.columns = col_names

    cpi_2011_df['W'] = cpi_2011_df['W - L'].apply(lambda x : x[0 : x.find('-')].strip())
    cpi_2011_df['L'] = cpi_2011_df['W - L'].apply(lambda x : x[x.find('-') + 1 : len(x)].strip())
    cpi_2011_df['OW'] = cpi_2011_df['OW - OL'].apply(lambda x : x[0 : x.find('-')].strip())
    cpi_2011_df['OL'] = cpi_2011_df['OW - OL'].apply(lambda x : x[x.find('-') + 1 : len(x)].strip())
    cpi_2011_df['OOW'] = cpi_2011_df['OOW - OOL'].apply(lambda x : x[0 : x.find('-')].strip())
    cpi_2011_df['OOL'] = cpi_2011_df['OOW - OOL'].apply(lambda x : x[x.find('-') + 1 : len(x)].strip())

    cpi_2011_df = CPI_Ratings.calc_unrounded_ratings(cpi_2011_df)

    cpi_2011_df = cpi_2011_df[['Team', 'CPI', 'W', 'L', 'OW', 'OL', 'OOW', 'OOL']].reset_index(drop = True)
    cpi_2011_df['Year'] = 2011
    cpi_2011_df['Team'] = cpi_2011_df['Team'].apply(lambda x: x.replace('CFP', ""))
    cpi_2011_df['Team'] = cpi_2011_df['Team'].apply(lambda x: x.replace('AP', ""))
    cpi_2011_df['Team'] = cpi_2011_df['Team'].apply(lambda x: x.replace('BCS', ""))
    cpi_2011_df['Team'] = cpi_2011_df['Team'].apply(lambda x: x.replace('(', ""))
    cpi_2011_df['Team'] = cpi_2011_df['Team'].apply(lambda x: x.replace(')', ""))
    cpi_2011_df['Team'] = cpi_2011_df['Team'].apply(lambda x: x.replace(',', ""))
    cpi_2011_df['Team'] = cpi_2011_df['Team'].apply(lambda x: x.strip())

    return cpi_2011_df

    

cpi_06_10_df = CPI_Ratings.get_cpi_by_years(range(2006, 2011,1))
cpi_2011_df = build_2011_cpi_df()
cpi_12_19_df = CPI_Ratings.get_cpi_by_years(range(2012, 2020,1))

cpi_df = pd.concat([cpi_06_10_df, cpi_2011_df, cpi_12_19_df], ignore_index=True,axis=0)
cpi_df.reset_index(drop = True, inplace = True)

cpi_df.to_csv("Data\CPI_Data.csv", index = False)





