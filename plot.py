import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash.dependencies

import datetime

import dataimport
import dataprocessing

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

file_upload_dialogue = dcc.Upload(
    id='file_upload_dialogue',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select Files')
    ]),
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '0px'
    },
    # Allow multiple files to be uploaded
    multiple=True
)

transaction_input_dialogue = html.Div(
    children = [
        html.H5(children = "Enter new cash transaction."),
        dcc.DatePickerSingle(
            id = 'manual_transaction_date',
            date = datetime.date.today(),
            display_format = "DD.MM.YYYY"
        ),
        dcc.Input(
            id = 'manual_transaction_subject',
            placeholder = 'Enter a subject...',
            type = 'text'
        ),
        dcc.Input(
            id = 'manual_transaction_value',
            placeholder = 'Enter a value...',
            type = 'number'
        ),
        html.Button('Submit', id = 'manual_transaction_button')
    ]
)

save_to_file_dialogue = html.Div(
    children = [
        html.H5(children = "Save transactions as file."),
        dcc.Input(
            id = 'save_to_file_name',
            placeholder = 'my_transactions.csv',
            type = 'text'
        ),
        html.Button('Save', id = 'save_file_button')
    ]
)

def generate_wins_losses_figure():
    all_transactions = dataimport.get_transaction_database()
    wins = []
    losses = []
    dates_str = []

    if len(all_transactions) > 0:
        wins, losses, dates_str = \
            dataprocessing.calc_wins_losses_table(all_transactions)
    return {
        'data': [
            {
                'x': dates_str,
                'y': wins, 'type': 'bar', 'name': 'Wins'
            },
            {
                'x': dates_str,
                'y': losses, 'type': 'bar', 'name': 'Losses'
            },
        ],
        'layout': { 'title': 'Wins vs Losses by Month' }
    }

app.layout = html.Div(children=[
    html.H1(children = 'My Financial Overview'),
    file_upload_dialogue,
    dcc.Graph(id = 'wins_losses_graph'),
    transaction_input_dialogue,
    save_to_file_dialogue
    ]
)

def file_upload_callback(list_of_contents):
    if list_of_contents == None:
        return update_wins_losses_figure([])

    new_transactions = []

    for c in list_of_contents:
        content_type, content_string = c.split(',')
        csv_string = base64.b64decode(content_string).decode('utf-8')
        new_transactions += dataimport.parse_csv_string(csv_string)

    return new_transactions

def manual_transaction_callback(n_clicks, date, subject, value):
    new_transactions = []
    if date and value:
        # Expected format: 2020-02-01
        split_date = date.split("-")
        year = int(split_date[0])
        month = int(split_date[1])
        day = int(split_date[2])
        new_transactions = [{
            "day": day,
            "month": month,
            "year": year,
            "sum": int(value * 100)
        }]

    return new_transactions

@app.callback(
    dash.dependencies.Output('wins_losses_graph', 'figure'),
    [dash.dependencies.Input('file_upload_dialogue', 'contents'),
     dash.dependencies.Input('manual_transaction_button', 'n_clicks')
    ],
    [dash.dependencies.State('manual_transaction_date', 'date'),
     dash.dependencies.State('manual_transaction_subject', 'value'),
     dash.dependencies.State('manual_transaction_value', 'value')
    ]
)
def new_data_callback(file_list_of_contents,
                      manual_n_clicks,
                      manual_date,
                      manual_subject,
                      manual_value,
                      old_values = [None, None]):

    if file_list_of_contents != old_values[0]:
        old_values[0] = file_list_of_contents
        new_transactions = file_upload_callback(file_list_of_contents)
        dataimport.update_transaction_database(new_transactions)

    elif manual_n_clicks != old_values[1]:
        old_values[1] = manual_n_clicks
        new_transactions = manual_transaction_callback(
            manual_n_clicks,
            manual_date,
            manual_subject,
            manual_value)
        dataimport.update_transaction_database(new_transactions)

    return generate_wins_losses_figure()

app.run_server(debug=True)
