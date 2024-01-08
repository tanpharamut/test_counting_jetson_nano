import pandas as pd
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from src.components import ids
from src.components import (
    bar_chart1,
    bar_chart2,
    bar_chart3,
   gender_dropdown,
   category_dropdown,
   duration_dropdown,
   link_sheets,
)


def create_layout(app: Dash, data: pd.DataFrame, duration_data: pd.DataFrame) -> html.Div:

    sidebar = html.Div(
        [
            dbc.Row(
                [
                    html.H5('Settings',
                            style={'margin-top': '12px', 'margin-left': '24px'})
                    ],
                style={"height": "5vh"},
                className='bg-primary text-white font-italic'
                ),
            dbc.Row(
                [
                    html.Div([
                        gender_dropdown.render(app, data),
                        category_dropdown.render(app, data),
                        duration_dropdown.render(app, data),
                        html.Hr()
                    ]),
                     html.Div([
                        dcc.RadioItems(
                            id=ids.CLIENTSIDE_TYPE_GRAPH, value='',
                            options=[
                                {'label': ' Show day', 'value': 'day'},
                                {'label': ' Show hour', 'value': 'hour'}
                            ],
                            labelStyle={'display': 'block'},
                            style={'textAlign': 'center', 'fontSize': 15}, 
                            className="radio_container radio columns")
                     ])
                ],
                style={'margin': '8px'}),
            dbc.Row(
                [
                    html.Div(bar_chart2.render(app, data), className='bar2 column_b')
                    ],
                style={'margin': '8px'}
                )
            ]
        )
 
    content = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div([
                                html.H6(children='Count total',
                                       style={'textAlign': 'center','color': 'black'}),
                                html.P(id='total-count',
                                       style={'textAlign': 'center','color': '#03FFE4', 'fontSize': 30})], 
                                       className="card_container total columns"),
                            html.Div([
                                html.H6(children='Men / Women',
                                       style={'textAlign': 'center','color': 'black'}),
                                html.P(id=ids.MEN_WOMEN_TOTAL_COUNT_PLACEHOLDER, children="",  
                                       style={'textAlign': 'center','fontSize': 30})],
                                       className="card_container gender columns"),
                            html.Div([
                                html.H6(children='Category',
                                       style={'textAlign': 'center','color': 'black'}),
                                html.P(id=ids.CATEGORY_COUNT_PLACEHOLDER, children="",
                                       style={'textAlign': 'center','color': '#0070FE','fontSize': 25})],
                                       className="card_container category columns"),
                            html.Div([
                                html.H6(children='Duration',
                                       style={'textAlign': 'center','color': 'black'}),
                                html.P(id=ids.DURATION_COUNT_PLACEHOLDER, children="", 
                                       style={'textAlign': 'center', 'color': '#6E3305', 'fontSize': 25})], 
                                       className="card_container duration columns"),
                          ]),
                    dbc.Col(
                        [
                            html.Div(bar_chart1.render(app, data), className='bar1 column_b')
                            ])
                    ],
                    style={
                        'margin-top': '50px', 'margin-left': '8px',
                        'margin-bottom': '8px', 'margin-right': '8px'}),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(bar_chart3.render(app, data), className='bar3 column_b')
                            ])
                    ],
                    style={'margin': '8px','margin-top': '70px'})
        ]
    )
                             
    return dbc.Container(
        [
            html.Div(
                className="app-div",
                children=[
                    html.H1(id='title-text'),
                    html.A(html.Button('Refresh Data'),href='/dash/'),
                    html.Div(link_sheets.render(app, data)),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(sidebar, width=3, className='bg-light'),
                    dbc.Col(content, width=9)
                    ]
                ),
            ]),
            dcc.Interval(
                id='interval-component', 
                interval=600000, 
                n_intervals=0)
            ],
            fluid=True
    ) 
