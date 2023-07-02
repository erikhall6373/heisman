import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_player_voting_data(year):
    sampleVotes = requests.get(f"https://www.sports-reference.com/cfb/awards/heisman-{year}.html")
    soup = BeautifulSoup(sampleVotes.content, 'html.parser')
    parsed_table = soup.find_all('table', id = 'heisman')[0]
    player_data = parsed_table.find_all('tr')[0: 11]

    return player_data

def get_position_data(year, position):

    player_data = get_player_voting_data(year)

    playerdict = {
        'player' : [],
        'school_name' : [],
        'class' : [],
        'pos' : [],
        'votes_first' : [],
        'votes_second' : [],
        'votes_third' : [],
        'points_won' : [],
        'summary' : []
    }

    for i in range(1, 10, 1):
        playerdict['player'].append(player_data[i].find('td', attrs={'data-stat': 'player'}).get_text())
        playerdict['school_name'].append(player_data[i].find('td', attrs={'data-stat': 'school_name'}).get_text())
        playerdict['class'].append(player_data[i].find('td', attrs={'data-stat': 'class'}).get_text())
        playerdict['pos'].append(player_data[i].find('td', attrs={'data-stat': 'pos'}).get_text())
        playerdict['votes_first'].append(player_data[i].find('td', attrs={'data-stat': 'votes_first'}).get_text())
        playerdict['votes_second'].append(player_data[i].find('td', attrs={'data-stat': 'votes_second'}).get_text())
        playerdict['votes_third'].append(player_data[i].find('td', attrs={'data-stat': 'votes_third'}).get_text())
        playerdict['points_won'].append(player_data[i].find('td', attrs={'data-stat': 'points_won'}).get_text())
        playerdict['summary'].append(player_data[i].find('td', attrs={'data-stat': 'summary'}).get_text())

    
    player_df = pd.DataFrame(playerdict)
    position_df = player_df[player_df['pos'] == position].reset_index(drop = True)

    return position_df

def clean_quarterback_data(year):

    qb_df = get_position_data(year, 'QB')

    summary_stats = list(qb_df['summary'])
    qbs = list(qb_df['player'])

    statsdict = {
        'player' : [],
        'Cmp' : [],
        'Att' : [],
        'Yds' : [],
        'TD' : [],
        'Int' : []
    }

    stats = [item.split(', ') for item in summary_stats]

    for i in range(len(qbs)):

        statsdict['player'].append(qbs[i])
        statsdict['Cmp'].append(int(stats[i][0][0:stats[i][0].find(' ')].strip()))
        statsdict['Att'].append(int(stats[i][1][0:stats[i][1].find(' ')].strip()))
        statsdict['Yds'].append(int(stats[i][2][0:stats[i][2].find(' ')].strip()))
        statsdict['TD'].append(int(stats[i][3][0:stats[i][3].find(' ')].strip()))
        statsdict['Int'].append(int(stats[i][4][0:stats[i][4].find(' ')].strip()))

    qb_stats_df = pd.DataFrame(statsdict)

    qb_df = qb_df.merge(qb_stats_df, how = 'inner', on = ['player'])

    qb_df.drop(columns= ['summary'], inplace = True)

    qb_df['player'] = qb_df['player'].apply(lambda x: x.replace("*", ""))
    qb_df['year'] = year

    return qb_df

def get_quarterback_voting_data(years):

    voting_list = [clean_quarterback_data(year) for year in years]

    result = pd.concat(voting_list, ignore_index=True,axis=0)
    result.reset_index(drop = True, inplace = True)

    return result

#test = get_quarterback_voting_data(range(2006, 2019, 1))

#test[test['year'] == 2014].head(10)

