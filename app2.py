############################################
# WisdomML                           #
# https://www.youtube.com/c/WisdomML         #
# https://github.com/wisdomml2020          #
# https://wisdomml.in        #


from shiny import App, render, ui,reactive
import numpy as np
import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
# Note that if the window is narrow, then the sidebar will be shown above the
# main content, instead of being on the left.
MODEL_PATH = 'model/logreg.pkl'
NORM_PATH = 'model/minmax.pkl'

model = joblib.load(MODEL_PATH)

normalizer = joblib.load(NORM_PATH)
assert isinstance(normalizer, MinMaxScaler)
normalizer.clip = False  # add this line

# UI section starts from here 
app_ui = ui.page_fluid(
    ui.markdown(
        """
        ## Early Diabetes Detection Shiny Web App
        """
    ),
    ui.layout_sidebar(
        ui.panel_sidebar(ui.input_select("polyuria", "Polyuria", {0: "No", 1: "Yes"}),
                         ui.input_select("polydipsia", "Polydipsia", {0: "No", 1: "Yes"}),
                         ui.input_slider("age", "Age in years", 0, 100, 20),
                         ui.input_select("gender", "Gender", {0: "Male", 1: "Female"}),
                         ui.input_select("partial_paresis", "Partial Paresis", {0: "No", 1: "Yes"}),
                         ui.input_select("sudden_weight_loss", "Sudden Weight Loss", {0: "No", 1: "Yes"}),
                         ui.input_select("irritability", "Irritability", {0: "No", 1: "Yes"}),
                         ui.input_select("del_healing", "Delayed Healing", {0: "No", 1: "Yes"}),
                         ui.input_select("alopecia", "Alopecia", {0: "No", 1: "Yes"}),
                         ui.input_select("itching", "Itching", {0: "No", 1: "Yes"}),
                         ui.input_action_button("btn", "Predict"),
                         ),
        
        ui.panel_main(ui.markdown(
        """
        ## Model Output
        """
    ),
                      ui.output_text_verbatim("txt", placeholder=True),),
    ),
)


## server section -> model prediction

def server(input, output, session):
    # The @reactive.event() causes the function to run only when input.btn is
    # invalidated.
    @reactive.Effect
    @reactive.event(input.btn)
    def _():
        # Input data
    
        testset = pd.DataFrame([[input.polyuria(),input.polydipsia(),input.age(),input.gender(),input.partial_paresis(),input.sudden_weight_loss(),input.irritability(),input.del_healing(),input.alopecia(),input.itching()]],columns=['Polyuria', 'Polydipsia', 'Age', 'Gender', 'partial paresis',
        'sudden weight loss', 'Irritability', 'delayed healing', 'Alopecia',
        'Itching'],dtype=float)
        
        # normalize age variables
        
        testset[['Age']] =normalizer.transform(testset[['Age']])
        
        # getting prediction
        prediction_proba = model.predict_proba(testset)
        output1 = round(prediction_proba[0, 1] * 100, 2)
        pred = str(output1) + "%"
        
        # This output updates only when input.btn is invalidated.
        @output
        @render.text
        @reactive.event(input.btn)
        def txt():
            return f'Probability of Diabetes is: "{pred}"'
    
 

app = App(app_ui, server)
