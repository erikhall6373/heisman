from great_tables import GT, html, style, loc
import sportsdataverse as sdv
import cfbd_json_py as cfbd
import pandas as pd
from html2image import Html2Image

def get_team_info(api_key):

  team_json = cfbd.teams.get_cfbd_team_information(api_key = api_key)
  team_df = pd.DataFrame(team_json)

  team_df['School'] = team_df['school']
  team_df = team_df[['School', 'team_id', 'school_primary_color']]

  team_df["school_logo_html"] = team_df['team_id'].apply(lambda row: f'<img src="https://github.com/CFBD/cfb-web/blob/master/public/logos/{row}.png?raw=true" height = 40;>')

  return team_df


def get_athlete_info(year):

  analysis_cols = ['athlete_id', 'Player', 'School', 'headshot_html', 'Year']

  roster_df = sdv.cfb_loaders.load_cfb_rosters(seasons = [year], return_as_pandas = True)

  roster_df['Player'] = roster_df['first_name'].astype('str') + ' ' + roster_df['last_name'].astype('str')
  roster_df["headshot_html"] = roster_df['headshot_url'].apply(lambda row: f'<img src="{row}" height = 40;/>')

  roster_df = roster_df.rename(columns = {'team' : 'School', 'season' : 'Year'})

  roster_df = roster_df[analysis_cols]

  return roster_df

def get_athlete_team_info(year, api_key):

  analysis_cols = ['athlete_id', 'Player', 'School', 'headshot_html', 'school_logo_html', 'Year', 'school_primary_color']

  athlete_df = get_athlete_info(year)
  team_df = get_team_info(api_key)

  result_df = pd.merge(athlete_df, team_df, on = ['School'])
  result_df = result_df[analysis_cols]
  result_df = result_df.rename(columns = {'athlete_id' : 'player_id'})

  return result_df


def create_viz_dataframe(top_n, year, api_key, weekly_name_replace = None):

  weekly_data_df = pd.read_csv("Data\Weekly_Data_Predict.csv")
  weekly_data_df = weekly_data_df.sort_values(by = 'Projected_Voting_Points', ascending = False)
  weekly_data_df = weekly_data_df.iloc[0:top_n]

  #weekly_data_df = weekly_data_df.rename(columns = {'Projected_Voting_Points': 'Projected_Voting_Points'})

  athlete_df = get_athlete_team_info(year, api_key)
  passing_df = cfbd.get_cfbd_player_season_stats(season = year, api_key = api_key, stat_category = 'passing')
  rushing_df = cfbd.get_cfbd_player_season_stats(season = year, api_key = api_key, stat_category = 'rushing')

  passing_df = passing_df[['player_id', 'player_name', 'team_name', 'passing_COMP', 'passing_ATT', 'passing_YDS', 'passing_TD', 'passing_INT']]
  rushing_df = rushing_df[['player_id', 'player_name', 'team_name', 'rushing_CAR', 'rushing_YDS', 'rushing_TD']]

  cfbd_df = pd.merge(passing_df, rushing_df, on = ['player_id', 'player_name', 'team_name'], how = 'left').drop(columns = 'player_id')
  cfbd_df = cfbd_df.rename(columns = {'player_name' : 'Player', 'team_name' : 'School'})

  if weekly_name_replace is not None:
    weekly_data_df['Player'] = weekly_data_df['Player'].replace(weekly_name_replace)
    cfbd_df['Player'] = cfbd_df['Player'].replace(weekly_name_replace)

  result_df = pd.merge(weekly_data_df, athlete_df, on = ['Player', 'School'])
  result_df = pd.merge(result_df, cfbd_df, on = ['Player', 'School'])
  result_df = result_df.reset_index(drop = True)

  result_df = result_df[['Player', 'headshot_html', 'school_logo_html', 'school_primary_color', 'passing_COMP', 'passing_ATT', 'passing_YDS', 'passing_TD', 'passing_INT',
                         'rushing_CAR', 'rushing_YDS', 'rushing_TD', 'Projected_Voting_Points']]

  for col in ['passing_COMP', 'passing_ATT', 'passing_YDS', 'passing_TD', 'passing_INT', 'rushing_CAR', 'rushing_YDS', 'rushing_TD', 'Projected_Voting_Points']:

    result_df[col] = pd.to_numeric(result_df[col])


  return result_df


def font_538_formatting(df, cols):

  google_font = '<link href="https://fonts.googleapis.com/css?family=Chivo" rel="stylesheet">'

  html_pre = f"{google_font}<p style='font-family: Chivo; bottom: 0; font-size: 14px; weight: 200'> "
  html_post = "</p>"

  result_df = df.copy()

  for col in cols:
    result_df[col] = result_df[col].apply(lambda row: f"{html_pre}{row}{html_post}")

  return result_df


def stack_player_name(viz_df, player_col, color_col):

  first_name_html_pre = "<div style='line-height:14px'><span style='font-weight:bold;font-variant:small-caps;color:black;font-size:14px'>"
  first_name_html_post = "</div>"

  last_name_html_pre_color = "<div style='line-height:12px'><span style ='font-weight:bold;color:"
  last_name_html_post_color = ";font-size:12px'>"
  last_name_html_post = "</span></div>"

  result_df = viz_df.copy()
  result_df['space_location'] = result_df[player_col].apply(lambda row: row.find(' '))
  result_df['first_name'] = result_df[player_col].apply(lambda row: row[0:row.find(' ')])
  result_df['first_name'] = result_df['first_name'].apply(lambda row: f"{first_name_html_pre}{row}{first_name_html_post}")

  result_df['last_name'] = result_df[player_col].apply(lambda row: row[row.find(' ')+1:])
  result_df['last_name'] = result_df.apply(lambda df: f"{last_name_html_pre_color}{df[color_col]}{last_name_html_post_color}{df['last_name']}{last_name_html_post}", axis = 1)

  result_df[player_col] = result_df['first_name'] + result_df['last_name']

  result_df = result_df.drop(columns = [color_col, 'first_name', 'last_name', 'space_location'])

  return result_df


def formatting_538(great_table_obj):
  great_table_obj = great_table_obj.tab_options(column_labels_background_color = "white",
                          data_row_padding = "3px",
                          heading_border_bottom_style = None,
                          table_border_top_width = "3px",
                          table_border_top_style = None,
                          table_border_bottom_style = None,
                          column_labels_font_weight = "normal",
                          column_labels_border_top_style = None,
                          column_labels_border_bottom_width = "2px",
                          column_labels_border_bottom_color = "black",
                          row_group_border_top_style = None,
                          row_group_border_top_color = "black",
                          row_group_border_bottom_width = "1px",
                          row_group_border_bottom_color = "white",
                          stub_border_color = "white",
                          stub_border_width = "px",
                          source_notes_font_size = 12,
                          source_notes_border_lr_style = None,
                          table_font_size = 16,
                          heading_align = "left")

  return great_table_obj


def hulk_color_formatting(cols, table, green_good = False, trim = False):

  color_palette = ["#1b7837", "#7fbf7b", "#d9f0d3", "#f7f7f7", "#e7d4e8", "#af8dc3", "#762a83"]

  if green_good:
    color_palette = ["#762a83", "#af8dc3", "#e7d4e8", "#f7f7f7", "#d9f0d3", "#7fbf7b", "#1b7837"]

  if trim:
    color_palette = color_palette[1:len(color_palette) - 1]


  result_table = table.data_color(columns = cols, palette = color_palette)

  return result_table


def build_heisman_gt(viz_df, player_col, analysis_cols_dict, picture_cols, rank_col_dict):

  analysis_col_names = list(analysis_cols_dict.keys())
  analysis_cols_green_good = [analysis_col for analysis_col in list(analysis_cols_dict.keys()) if analysis_cols_dict[analysis_col] == 'good']
  analysis_cols_green_bad = [analysis_col for analysis_col in list(analysis_cols_dict.keys()) if analysis_cols_dict[analysis_col] == 'bad']

  rank_col_name = list(rank_col_dict.keys())[0]
  rank_col_list = [rank_col_name]


  order_cols = player_col + picture_cols + analysis_col_names + rank_col_list

  #viz_df = font_538_formatting(viz_df, analysis_col_names)
  viz_df = stack_player_name(viz_df, 'Player', 'school_primary_color')
  result_table = GT(viz_df[order_cols])
  result_table = formatting_538(result_table)
  result_table = hulk_color_formatting(analysis_cols_green_good, result_table, green_good = True, trim = True)
  result_table = hulk_color_formatting(analysis_cols_green_bad, result_table, trim = True)
  result_table = hulk_color_formatting(rank_col_list, result_table, green_good = rank_col_dict[rank_col_name] == "good")
  result_table = result_table.fmt_markdown(columns = player_col + picture_cols)

  return result_table


def cleanup_gt_formatting(heisman_gt_object, top_n, week):

  result_gt = heisman_gt_object.tab_header(title = "Predictive QB Heisman Votes", subtitle = f"Top {top_n} - Through Week {week}")
  result_gt = result_gt.tab_source_note("Model by @DjDataScience, Table inspiration by @arbitanalytics, Data from sports-reference.com and CFBD")

  result_gt = result_gt.tab_spanner(label = 'Passing', columns = ['passing_COMP', 'passing_ATT', 'passing_YDS', 'passing_TD', 'passing_INT'])
  result_gt = result_gt.tab_spanner(label = 'Rushing', columns = ['rushing_CAR', 'rushing_YDS', 'rushing_TD'])

  result_gt = result_gt.fmt_integer(columns=["passing_YDS", "rushing_YDS"], use_seps = True)
  result_gt = result_gt.fmt_number(columns=["rushing_CAR"], decimals = 0)



  result_gt = result_gt.cols_label(Player = 'Player', headshot_html = "", school_logo_html = "", passing_COMP = 'Completions',
                                   passing_ATT = 'Attempts', passing_YDS = 'Yards', passing_TD = 'TDs', passing_INT = 'Interceptions',
                                   rushing_CAR = 'Attempts', rushing_YDS = 'Yards', rushing_TD = 'TDs',
                                   Projected_Voting_Points = 'Predicted Voting Points')

  return result_gt


viz_df = create_viz_dataframe(top_n = 10, year = 2024, 
                              api_key = ,
                              weekly_name_replace = {'Joey Labas' : 'Joe Labas',
                                                     'K.J. Jefferson' : 'KJ Jefferson'})

weekly_GT = build_heisman_gt(viz_df = viz_df, player_col = ['Player'],
 analysis_cols_dict = {'passing_COMP' : 'good', "passing_ATT" : 'good', "passing_YDS" : 'good', "passing_TD" : "good", "passing_INT" : "bad",
                       "rushing_CAR" : "good", "rushing_YDS" : "good", "rushing_TD" : "good"},
 picture_cols = ['headshot_html', 'school_logo_html'],
 rank_col_dict = {"Projected_Voting_Points" : "good"})

weekly_GT = cleanup_gt_formatting(weekly_GT, 10, 1)


#weekly_GT.save(file = r'C:/Repos/heisman/heisman_visual/test2.png')
#hti.screenshot(html_str=weekly_GT.as_raw_html(), save_as= 'test.png')

#hti.screenshot(url='https://www.python.org', save_as='python_org.png')


#weekly_GT.save(file = "heisman_visual\\test.jpg")

weekly_GT.as_raw_html()


with open("C:\\Repos\\heisman\\heisman_visual\\weekly.html", "w") as text_file:
  text_file.write(weekly_GT.as_raw_html())