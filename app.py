import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from tingmo import TingMo

# number of seconds between re-calculating the data
UPDATE_INTERVAL = 86400

def get_new_data():
    global tm
    tm = TingMo()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# get initial data
get_new_data()

server = app.server

app.layout = html.Div([
    html.H1('TingMo',style={'text-align':'center','font-size':'50px'}),
    html.Div(children=[
    html.Div(children=[
        html.Div(children=[

                html.H2('What is TingMo?'),
                html.P('TingMo is is powerful tool designed to quickly identify lookalike domains.'),
                html.Div(children=[html.Div(children=[html.H5('Number of Chunks')], className='four columns'),
                html.Div(children=[html.H5('Chunk Size')], className='four columns')],className='row'),
                html.Div(children=[html.Div(children=[dcc.Input(value='7',id='chunk_size')],className='four columns'),
                html.Div(children=[dcc.Input(value='5',id='n_chunks')],className='four columns')],className='row'),

        ], className='six columns'),
        html.Div(children=[
            html.H4('Query Options'),
            dcc.Checklist(id='brands',
            options=[
                {'label': 'Remove brand TLD matches', 'value': 'BRD'}
            ],
            values=['BRD']),
            html.H4('Enter Domains to Check (comma-separated)'),
            dcc.Textarea(value='google.com', id='dom_list',maxLength=20000,
                     style = {'width': '48%'}),
            html.Div(html.Button('Submit', id='button')),
            html.P(id='my-div',children='Results appear here.')],
        className='six columns',
        )])],className='row')])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input('button', 'n_clicks'),Input('brands','values')],
    [State('dom_list', 'value')]
)
def get_matches(n_clicks,values,domain_list):
    domain_list = [d.strip().lower() for d in domain_list.split(',')]
    print(domain_list)
    exclude = 'BRD' in values
    results = tm.query_LSH(domain_list,exclude)
    html_output = []
    for r in results:
        html_output.append(html.H3(children=r+':'))
        if len(results[r]) == 0:
            html_output.append(html.P(children='No results.'))
        for result in results[r]:
            html_output.append(html.P(children=result))
    return html_output

if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False)