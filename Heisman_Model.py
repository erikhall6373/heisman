import pandas as pd
import requests
from bs4 import BeautifulSoup


sampleVotes = requests.get("https://www.sports-reference.com/cfb/awards/heisman-2006.html")
soup = BeautifulSoup(sampleVotes.content, 'html.parser')
parsed_table = soup.find_all('table', id = 'heisman')[0]
player_data = parsed_table.find_all('tr')[0: 11]

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

    
heisman_df = pd.DataFrame(playerdict)
qb_df = heisman_df[heisman_df['pos'] == 'QB'].reset_index(drop = True)

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

qb_df.drop(columns= ['summary']).head(10)

