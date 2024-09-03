
import pandas as pd
from great_tables import GT, html, style, loc
import sportsdataverse as sdv
import cfbd_json_py as cfbd_json
from html2image import Html2Image



#print(weekly_data_df.head())

def get_player_headshot_lookup(season):

    roster_df = sdv.cfb_loaders.load_cfb_rosters(seasons = [season], return_as_pandas = True)

    roster_df['player'] = roster_df.apply(lambda df: str(df['first_name']) + ' ' + str(df['last_name']), axis = 1)
    roster_df['school'] = roster_df['team']

    return roster_df[['player', 'school', 'headshot_url']]

def get_team_id_lookup(api_key):

    team_json = cfbd_json.teams.get_cfbd_team_information(api_key = api_key)
    team_df = pd.DataFrame(team_json)
    
    return team_df[['school', 'team_id']]

def append_image_urls(performance_df, api_key, season):

    player_headshot_df = get_player_headshot_lookup(season)
    team_id_df = get_team_id_lookup(api_key)
    result_cols = ['player', 'headshot_html', 'school_logo_html',
                   'Passing_Rate', 'Passing_TD', 'Rushing_TD', 'Power5', 'CPI', 'Projected Voting Points']

    performance_df = performance_df.rename(columns = {"Player" : "player", "School" : "school"})
    performance_df = performance_df.merge(player_headshot_df, on = ['player', 'school'], how = 'left')
    performance_df = performance_df.merge(team_id_df, on = ['school'], how = 'left')

    performance_df['team_id'] = performance_df['team_id'].astype(int)

    performance_df["headshot_html"] = performance_df['headshot_url'].apply(lambda row: f'<img src="{row}" height = 40;/>')
    performance_df["school_logo_html"] = performance_df['team_id'].apply(lambda row: f'<img src="https://github.com/CFBD/cfb-web/blob/master/public/logos/{row}.png?raw=true" height = 40;>')

    return performance_df[result_cols]

def apply_538_cell_formatting(df, cols):

  google_font = '<link href="https://fonts.googleapis.com/css?family=Chivo" rel="stylesheet">'

  html_pre = f"{google_font}<p style='font-family: Chivo; bottom: 0; font-size: 14px; weight: 200'> "
  html_post = "</p>"

  result_df = df.copy()

  for col in cols:
    result_df[col] = result_df[col].apply(lambda row: f"{html_pre}{row}{html_post}")

  return result_df

def apply_hulk_formatting(great_table, cols, reverse = False):
   
   color_palette = ["#1b7837", "#7fbf7b", "#d9f0d3", "#f7f7f7", "#e7d4e8", "#af8dc3", "#762a83"]

   if reverse:
      color_palette = ["#762a83", "#af8dc3", "#e7d4e8", "#f7f7f7", "#d9f0d3", "#7fbf7b", "#1b7837"]

   return great_table.data_color(columns = cols, palette = color_palette)

def get_538_column_name_styling(col_name):
   
   google_font = '<link href="https://fonts.googleapis.com/css?family=Cairo" rel="stylesheet">'
   html_pre = f"{google_font}<p style='font-family: Cairo; weight: 400'> "
   html_post = "</p>"

   return f"{html_pre}{col_name}{html_post}"

def get_538_header_styling(header_text):
   
   google_font = '<link href="https://fonts.googleapis.com/css?family=Cairo" rel="stylesheet">'
   html_pre = f"{google_font}<p style='font-family: Chivo; weight: 700'> "
   html_post = "</p>"

   return f"{html_pre}{header_text}{html_post}"


def get_538_header_styling(subheader_text):
   
   google_font = '<link href="https://fonts.googleapis.com/css?family=Cairo" rel="stylesheet">'
   html_pre = f"{google_font}<p style='font-family: Chivo; weight: 300'> "
   html_post = "</p>"

   return f"{html_pre}{subheader_text}{html_post}"


def apply_538_formatting(great_table):

    return great_table.tab_options(column_labels_background_color = "white",
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

def create_report_table(performance_df, api_key, season, columns_538):

    performance_df = append_image_urls(performance_df, api_key, season)
    performance_df = apply_538_cell_formatting(performance_df, columns_538)
    performance_df = performance_df.rename(columns = {"Projected Voting Points" : "Projected_Voting_Points"})
    report_table = GT(performance_df)

    report_table = report_table.fmt_markdown(columns = ['headshot_html', 'school_logo_html'])
    report_table = report_table.fmt_markdown(columns = columns_538)
    report_table = apply_538_formatting(report_table)
    report_table = apply_hulk_formatting(report_table, cols = ['Passing_Rate', 'Rushing_TD', 'Passing_TD', 'CPI'])
    report_table = apply_hulk_formatting(report_table, cols = ['Projected_Voting_Points'], reverse = True)
    #report_table = apply_538_column_name_styling(report_table, cols = ['Passing_Rate'])

    report_table = report_table.cols_label(player = html(get_538_column_name_styling("Player")),
                                           headshot_html = "",
                                           school_logo_html = html(get_538_column_name_styling("School")),
                                           Passing_Rate = html(get_538_column_name_styling("Passing Rate")),
                                           Passing_TD = html(get_538_column_name_styling("Passing TD")),
                                           Rushing_TD = html(get_538_column_name_styling("Rushing TD")),
                                           CPI = html(get_538_column_name_styling("CPI")),
                                           Projected_Voting_Points = html(get_538_column_name_styling("Projected Voting Points")))
    
    report_table = report_table.cols_hide(['Power5'])

    report_table = report_table.tab_header(title=html(get_538_header_styling("Predictive Heisman Votes")), 
                                           subtitle=html(get_538_header_styling("Top 10 Through Week X")))



    return report_table


weekly_data_df = pd.read_csv("Data\Weekly_Data_Predict.csv")
weekly_data_df = weekly_data_df.sort_values(by = 'Projected Voting Points', ascending = False)
weekly_data_df = weekly_data_df.head(10)

#weekly_data_df = apply_538_cell_formatting(weekly_data_df, ['Passing_Rate'])

#test_df = append_image_urls(weekly_data_df, '1a2veryeQ/v2jym/fJI3+8jFi76uCW0oXYsh001Imq5EkwblVw4n8rSPqR0UKq4N', 2023)

#test_df = get_team_id_lookup('1a2veryeQ/v2jym/fJI3+8jFi76uCW0oXYsh001Imq5EkwblVw4n8rSPqR0UKq4N')
#print(test_df.head(50))

test_table = create_report_table(weekly_data_df, '1a2veryeQ/v2jym/fJI3+8jFi76uCW0oXYsh001Imq5EkwblVw4n8rSPqR0UKq4N', 2023,
                                 ['player', 'Passing_Rate', 'Power5', 'CPI', 'Projected Voting Points'])
hti = Html2Image(output_path = 'C:\\Repos\\heisman\\heisman_visual\\')
hti.screenshot(html_str=test_table.as_raw_html(), save_as= 'test.png')

#print(table)

#print(weekly_data_df.head())