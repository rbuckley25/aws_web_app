from DB import Database
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


def read_df(name):
    db = Database()
    df_read = lambda x: db.read_db(name)
    df = df_read(name)
    return df


stat = read_df('Rainfall')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server


app.layout = html.Div(children=[
    html.H1(children='Rainfall Data in Ireland from 1958-2020'),

    html.Div(children='''
        Retrived from Central Statistics Office using StatBank API: https://statbank.cso.ie/webserviceclient/  
    '''),

    html.Div([
            dcc.Dropdown(
                id='diff_graphs',
                options=[{'label': i, 'value': i} for i in ['Rainfall','Sunshine','Temperature']],
                value='Rainfall'
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),
    
    html.Div([
            dcc.Dropdown(
                id = 'diff_stats',
                value = 'Most Rainfall in a Day'
            )
        ],style={'width': '49%', 'display': 'inline-block'}),

    dcc.Graph(id='rainfall_plot'),


])

@app.callback(dash.dependencies.Output('diff_stats','options'),
            dash.dependencies.Output('diff_stats','value'),
            dash.dependencies.Input('diff_graphs','value'))
def update_dropdown(name):
    df = read_df(name)
    x = [{'label':i, 'value':i} for i in df['Statistic'].unique()]
    value = list(x[0].values())
    return x,value[0]

 
@app.callback(dash.dependencies.Output('rainfall_plot', 'figure'),
                [dash.dependencies.Input('diff_graphs', 'value'),
                dash.dependencies.Input('diff_stats', 'value')])
def Update_Graph(name,stat):
    df = read_df(name)
    in_stat = df[df['Statistic']==stat]
    fig = px.bar(in_stat, x="Year", y="value", color='Meteorological Weather Station', barmode="group",  labels = {"Statistic":"Average Yearly Values","value":name})
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=False, port=8080)
    