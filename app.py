from shiny import App, ui, render





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

            The model itself a linear regression with voting points as a response, and individual and team
            statitistics as the predictors.
            <br />

            The model is made up the following 5 predictors;
            <br />
            
            **Passer Rating** : Passer efficency rating as according to pro-football-reference.com.
            <br />

            **Passing TDs** : Number of passing touchdowns thrown by a quarterback.
            <br />

            **Rushing TDs** : Number of rushing touchdowns thrown by a quarterback.
            <br />

            **Power 5 Indicator** : A binary value of 0 or 1. Set equal to 1, 
            if the quarterback's team plays in a power 5 conference. Otherwise 0.
            <br />

            **CPI** : A team strength of record metric involving the winning percentages of opponents. More details 
            of the metric can be found at www.cpiratings.com/about.html.
            """
        )
               )
)
)



# Part 2: server ----
def server(input, output, session):

    return None

# Combine into a shiny app.
# Note that the variable must be "app".
app = App(app_ui, server)