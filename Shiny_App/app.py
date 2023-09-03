from shiny import App, ui, render
import pandas as pd
import numpy as np
import pickle
import statsmodels.api as sm
from shinywidgets import output_widget, render_widget
import plotly.express as px
from pathlib import Path

model_path = Path(__file__).parent / "heisman_model.pkl"
model_data_path = Path(__file__).parent / "Model_Data.csv"
weekly_data_path = Path(__file__).parent / "Weekly_Data.csv"

model = pickle.load(open(model_path, 'rb'))
################### Historical #########################
model_data = pd.read_csv(model_data_path).reset_index(drop = True)

predict_data =  model_data[['Passing_Rate', 'Passing_TD', 'Rushing_TD', 'Power5', 'CPI']]
predict_data = sm.tools.add_constant(predict_data)
predict_data['Prediction'] = model.predict(predict_data)
predict_data = predict_data['Prediction']

model_data = pd.merge(model_data, predict_data, left_index=True, right_index=True)
model_data['CPI'] = model_data['CPI'].round(2)
model_data['Prediction'] = model_data['Prediction'].round(2)

################### Current #########################
current_df = pd.read_csv(weekly_data_path).reset_index(drop = True)

current_predict_df =  current_df[['Passing_Rate', 'Passing_TD', 'Rushing_TD', 'Power5', 'CPI']]
current_predict_df = sm.tools.add_constant(current_predict_df)
current_predict_df['Projected Voting Points'] = model.predict(current_predict_df)
current_predict_df = current_predict_df['Projected Voting Points']

current_df = pd.merge(current_df, current_predict_df, left_index=True, right_index=True)
current_df['CPI'] = current_df['CPI'].round(2)
current_df['Projected Voting Points'] = current_df['Projected Voting Points'].round(2)


# Part 1: ui ----
app_ui = ui.page_fluid(
    ui.navset_tab(
        ui.nav("Model Details", 
           
        ui.markdown(
            """
            # So how does this model work anyway?
            This is a project that I spent the summer of 2020 on in my free time.
            <br />

            Simply put, the model aims to predict the finals standings in Heisman voting for quarterbacks
            specifically. This is mostly because it is difficult to come up with a sample of metrics that apply
            to the different positions across college football.
            <br />

            The model itself is a linear regression with voting points as a response, and individual and team
            statitistics as the predictors. The model is built with training data from the 2006 to 2018 seasons.
            <br />

            The model is made up of the following 5 predictors;
            <br />
            
            **Passer Rating** : Passer efficency rating as according to pro-football-reference.com.
            <br />

            **Passing TDs** : Number of passing touchdowns thrown by a quarterback.
            <br />

            **Rushing TDs** : Number of rushing touchdowns ran by a quarterback.
            <br />

            **Power 5 Indicator** : A binary value of 0 or 1. Set equal to 1, 
            if the quarterback's team plays in a power 5 conference. Otherwise 0. Notre Dame is the only independent team 
            to receive a power 5 label.
            <br />

            **CPI** : A team strength of record metric involving the winning percentages of opponents. More details 
            of the metric can be found at www.cpiratings.com/about.html.
            """
        )
               ),
        ui.nav("Past Model Results", 
           
        ui.input_select("model_year", "Model Year", model_data['Year'].tolist()),
        ui.output_table("historical_data")
               ),

    ui.nav("Current Model Results", 
           
        ui.output_table("current_data")
               ),
    
    ui.nav("What If", 
           
        ui.input_numeric("what_if_QBR", "Passer Rating", value=0.0),
        ui.input_numeric("what_if_pass_TD", "Passing TDs", value=0),
        ui.input_numeric("what_if_rush_TD", "Rushing TDs", value=0),
        ui.input_radio_buttons("what_if_power_5", "Power 5 Conference",  {1 : "Yes", 0: "No"}),
        ui.input_numeric("what_if_CPI", "CPI", value=0.0),
        ui.output_text("what_if_analysis")
               ),
    
    ui.nav("Scatter",
           ui.div(
           output_widget("my_widget")
           )
           )
    )
)




# Part 2: server ----
def server(input, output, session):

    @output
    @render.table
    def historical_data():

        result_df = model_data[model_data['Year'] == int(input.model_year())]

        result_df['Actual_Rank'] = result_df['points_won'].rank(ascending = False).astype('int')
        result_df['Predicted_Rank'] = result_df['Prediction'].rank(ascending = False).astype('int')

        result_cols = ['Player', 'School', 'Actual_Rank', 'Predicted_Rank', 'Passing_Rate', 'Passing_TD', 'Rushing_TD', 'Power5', 'CPI']
        result_df = result_df[result_cols]

        return result_df
    
    @output
    @render.table
    def current_data():

        result_df = current_df

        result_cols = ['Player', 'School', 'Projected Voting Points', 'Passing_Rate', 'Passing_TD', 'Rushing_TD', 'Power5', 'CPI']
        result_df = result_df[result_cols]

        result_df = result_df.sort_values(by = 'Projected Voting Points', ascending = False)

        return result_df
    
    @output
    @render.text
    def what_if_analysis():

        what_if_df = pd.DataFrame({
            'Passing_Rate' : [float(input.what_if_QBR())],
            'Passing_TD' : [int(input.what_if_pass_TD())],
            'Rushing_TD' : [int(input.what_if_rush_TD())],
            'Power5' : [int(input.what_if_power_5())],
            'CPI' : [float(input.what_if_CPI())]
        })

        what_if_df = sm.tools.add_constant(what_if_df, has_constant='add')

        what_if_df['Prediction'] = model.predict(what_if_df)

        result = what_if_df.iloc[0]['Prediction']
        result = result.round(2)

        return f"A player with these statistics would have {result} projected voting points."
    
    @output
    @render_widget
    def my_widget():
        fig = px.scatter(
            model_data, x="Year", y="Prediction",
            hover_data=['Player']
        )
        return fig

# Combine into a shiny app.
# Note that the variable must be "app".
app = App(app_ui, server)