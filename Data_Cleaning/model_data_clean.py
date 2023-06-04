import pandas as pd
import numpy as np

cpi_data = pd.read_csv("Data\CPI_Data.csv")
voting_data = pd.read_csv("Data\QB_Voting_Data.csv")
stats_data = pd.read_csv("Data\QB_Stats_Data.csv")

def stats_cleaning(stats_df):
    
    keepcols = ['Player', 'School', 'Passing_Rate', 'Passing_TD', 'Rushing_TD', 'Power5', 'Year']

    stats_df = stats_df[keepcols]

    kReynolds_data = {
        'Player' : ['Keenan Reynolds'],
        'School' : ['Navy'],
        'Passing_Rate' : [162.1],
        'Passing_TD' : [8],
        'Rushing_TD' : [24],
        'Power5' : [0],
        'Year' : [2015]
    }

    stats_df = stats_df[keepcols]
    stats_df = pd.concat([stats_df, pd.DataFrame(kReynolds_data)], axis = 0)
    stats_df.reset_index(drop = True, inplace= True)

    return stats_df

def voting_cleaning(voting_df):

    voting_df = voting_df.rename(columns = {'player' : 'Player', 
                                          "school_name" : "School",
                                          "year" : "Year"})
    
    keepcols = ['Player', 'School', 'Year', 'points_won']

    voting_df = voting_df[keepcols]

    return voting_df[keepcols]

def cpi_cleaning(cpi_df):

    cpi_df = cpi_df.rename(columns = {'Team' : 'School'})

    school_recode = {
        'Ball St' : 'Ball State',
        'Boise St' : 'Boise State',
        'Southern Cal' : 'USC',
        'Central Florida' : 'UCF',
        'Oklahoma St' : 'Oklahoma State',
        'Mississippi St' : 'Mississippi State',
        'Florida St' : 'Florida State',
        'Kansas St' : 'Kansas State',
        "Hawai`i" : "Hawaii",
        'Fresno St' : 'Fresno State',
        'Ohio State*' : 'Ohio State',
        'Michigan St' : 'Michigan State',
        'Washington St' : 'Washington State'
    }
    
    keepcols = ['School', 'Year', 'CPI']

    cpi_df = cpi_df[keepcols].replace(school_recode)

    return cpi_df

stats_data = stats_cleaning(stats_data)
voting_data = voting_cleaning(voting_data)
cpi_data = cpi_cleaning(cpi_data)

model_data = voting_data.merge(stats_data, on = ['Player', 'School', 'Year'], how = 'left')
model_data = model_data.merge(cpi_data, on = ['School', 'Year'], how = 'left')

model_data.to_csv("Data\Model_Data.csv", index = False)