from shiny import App, ui, render

# Part 1: ui ----
app_ui = ui.page_fluid(

    ui.h1("Hello World")         
)




# Part 2: server ----
def server(input, output, session):
    return None

# Combine into a shiny app.
# Note that the variable must be "app".
app = App(app_ui, server)