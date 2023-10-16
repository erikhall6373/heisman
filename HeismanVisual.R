library(cfbfastR)
library(dplyr)
library(gt)
library(gtExtras)
library(cfbplotR)

#This is your CFB Data .com website key
Sys.setenv(CFBD_API_KEY = "")


predictions <- read.csv('Data/Weekly_Data_Predict.csv')

player_stats <- cfbd_stats_season_player(2023)
players <- cfbd_team_roster(2023)

pred_stat_join <- predictions |>
  merge(player_stats, by.x = 'Player', by.y = 'player', all.x = TRUE) |>
  merge(players, by = 'athlete_id')

pred_stat_to_use <- pred_stat_join |>
  select(first_name, last_name, team.x, athlete_id, passing_completions, passing_att,
         passing_yds, passing_td, passing_int, rushing_car, rushing_yds, 
         rushing_td, Projected.Voting.Points)

top_10 <- pred_stat_to_use |>
  arrange(-Projected.Voting.Points) |>
  top_n(10)


table <- top_10 |> 
  gt() |>
  tab_header(title = "Predictive Heisman Votes",
                                        subtitle = "Top 10 - Through Week 7") |>
  cols_label(first_name = 'Player',
             team.x = "",
             athlete_id = "",
             passing_completions = 'Completions',
             passing_att = 'Attempts',
             passing_yds = 'Yards',
             passing_td = 'TDs', 
             passing_int = 'Ints',
             rushing_car = 'Carries',
             rushing_yds = 'Yards',
             rushing_td = 'TD',
             Projected.Voting.Points = 'Predicted Votes') |>
  gt_merge_stack_team_color(first_name, last_name, team.x) |>
  tab_spanner(label = 'Passing',
              columns = starts_with('passing')) |>
  tab_spanner(label = 'Rushing',
              columns = starts_with('rushing')) |>
  gt_fmt_cfb_logo(columns = team.x) |>
  gt_fmt_cfb_headshot(athlete_id) |>
  fmt_number(columns = 4:11, decimals = 0) |>
  fmt_number(columns = 12, decimals = 1) |>
  gt_hulk_col_numeric(passing_completions:rushing_td, trim = TRUE) |>
  gt_hulk_col_numeric(Projected.Voting.Points) |>
  tab_source_note("Model by @DjDataScience, Table by @arbitanalytics, Data from @cfbfastR, stylying from cfbplotR and gtExtras")
table

gt_theme_538(table)
gtsave(gt_theme_538(table), "HeismanPredictions.png")