import os
import PIL.Image
from PIL import Image
import dash
from dash import dcc, ctx, html
import os
from PIL import Image
import dash
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd

PIL.Image.MAX_IMAGE_PIXELS = None
global df
df = pd.DataFrame(columns=['File Name', 'Grading', 'Cytoplasma', 'Capliraity'])

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server 

# List to hold image paths
image_paths = []


# Function to load images from a folder
def load_images_from_folder(folder_path):
    global image_paths
    image_paths = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if
                   img.endswith(".jpg") or img.endswith(".png")]


# Layout of the Dash app
app.layout = html.Div([
    dcc.Input(id='folder-input', type='text', placeholder='Enter folder path'),
    html.Button('Load Images', id='load-images-btn', n_clicks=0, style={'background': 'linear-gradient(to right, #ff9966, #ff5e62)', 'border-radius': '20px', 'color': 'white'}),
    html.Button('Next', id='next-btn', n_clicks=0, disabled=True),
    html.Button('Previous', id='prev-btn', n_clicks=0, disabled=True),
    html.Div(id="image"),
    html.Br(),
    html.Img(id='image-display', style={'height': '550px', 'width': 'auto', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Div(id='image-info'),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H4('Grading:'),
            html.Div(id="grading"),
            dcc.RadioItems(id="grading_radio", options=['Improve', 'Not Improve'], value='Improve')]),
        dbc.Col([
            html.Br(),
            html.H4('Cytoplasma:'),
            html.Div(id="cytoplasma"),
            dcc.RadioItems(id="cytoplasma_radio", options=['Improve', 'Not Improve'], value='Improve')]),
        dbc.Col([
            html.Br(),
            html.H4('Capliraity:'),
            html.Div(id="capilarity"),
            dcc.RadioItems(id="capilarity_radio", options=['Improve', 'Not Improve'], value='Improve')]),
        dbc.Col([
            html.Br(),
            html.Button('Submit', id='submit-btn', n_clicks=0, style={'background': 'linear-gradient(to right, #008CBA, #04AA6D)', 'border-radius': '30px', 'color': 'white', 'font-size': '24px'})])
    ])
])


# Combined callback to handle loading images and navigation
@app.callback(
    Output('image-display', 'src'),
    Output('next-btn', 'disabled'),
    Output('prev-btn', 'disabled'),
    Input('load-images-btn', 'n_clicks'),
    Input('next-btn', 'n_clicks'),
    Input('prev-btn', 'n_clicks'),
    Input('grading_radio', 'value'),
    Input('cytoplasma_radio', 'value'),
    Input('capilarity_radio', 'value'),
    Input('submit-btn', 'n_clicks'),
    State('folder-input', 'value'),
    State('image-display', 'src')
)
def handle_images(load_n_clicks, next_n_clicks, prev_n_clicks, grading_val,
                  cytoplasma_val, capilarity_val, submit_n_clicks, folder_path, current_image_src):
    global index, df
    if ctx.triggered_id == 'load-images-btn':
        index = 0
        load_images_from_folder(folder_path)
        return Image.open(image_paths[0]), False, True
    elif ctx.triggered_id == 'next-btn' and len(image_paths) > 1:
        if index < len(image_paths):
            index += 1
            return Image.open(image_paths[index]), False, False
        else:
            return Image.open(image_paths[-1]), True, False
    elif ctx.triggered_id == 'prev-btn' and len(image_paths) > 1:
        if index >= 0:
            index -= 1
            return Image.open(image_paths[index]), False, False
        else:
            return Image.open(image_paths[0]), False, True
    elif ctx.triggered_id == 'submit-btn':
        new_row = {'File Name': image_paths[index], 'Grading': str(grading_val), 'Cytoplasma': str(cytoplasma_val), 'Capliraity': str(capilarity_val)}
        df = df._append(new_row, ignore_index=True)
        df.to_excel('results.xlsx', index=False)
        return Image.open(image_paths[index]), False, False
    else:
        raise PreventUpdate


# if __name__ == '__main__':
#     app.run_server(debug=True)
