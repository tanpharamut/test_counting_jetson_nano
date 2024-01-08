from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP
from dash.dependencies import Input, Output, State
import pandas as pd

from src.components import ids
from src.components.layout import create_layout
from src.data.loader import load_test_data, load_duration_data

DATA_PATH = "./static/final-result-csv/uploaded_video.csv"
DATA_DURATION_PATH = "./static/duration.csv"
STATUS_CLIENT_SIDE = "./static/status_client_side.csv"
NEW_DATA_DURATION_PATH = "./static/final-result-csv/new_duration.csv"
DATA2 = "./static/data2.csv"

def create_dash_application(flask_app) -> Dash:
    dash_app = Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/", external_stylesheets=[BOOTSTRAP])
    
    # load the data and create the data manager
    data = load_test_data(DATA_PATH)
    duration_data = load_duration_data(NEW_DATA_DURATION_PATH)
    client_side_data = pd.read_csv(STATUS_CLIENT_SIDE)
    existing_data = pd.read_csv(DATA2)
    duration_text = None
    ip = None
    name = None
    ip_c1 = existing_data.loc[0, 'IP'] if not existing_data.empty else None
    ip_c2 = existing_data.loc[1, 'IP'] if len(existing_data) >= 2 else None
    ip_c3 = existing_data.loc[2, 'IP'] if len(existing_data) >= 3 else None
    ip_c4 = existing_data.loc[3, 'IP'] if len(existing_data) >= 4 else None
    ip_c5 = existing_data.loc[4, 'IP'] if len(existing_data) >= 5 else None
    name_c1 = existing_data.loc[0, 'Name'] if not existing_data.empty else None
    name_c2 = existing_data.loc[1, 'Name'] if len(existing_data) >= 2 else None
    name_c3 = existing_data.loc[2, 'Name'] if len(existing_data) >= 3 else None
    name_c4 = existing_data.loc[3, 'Name'] if len(existing_data) >= 4 else None
    name_c5 = existing_data.loc[4, 'Name'] if len(existing_data) >= 5 else None
    num_of_row = client_side_data['row_num'].loc[0] if not client_side_data.empty else None
    print(ip_c1,ip_c2,ip_c3,ip_c4,ip_c5)
    print(name_c1,name_c2,name_c3,name_c4,name_c5)
    print(num_of_row)
    if num_of_row == 0:
            duration_text = 'Camera1'
            ip = ip_c1
            name = name_c1
    elif num_of_row == 1:
            duration_text = 'Camera2'
            ip = ip_c2
            name = name_c2
    elif num_of_row == 2:
            duration_text = 'Camera3'
            ip = ip_c3
            name = name_c3
    elif num_of_row == 3:
            duration_text = 'Camera4'
            ip = ip_c4
            name = name_c4        
    elif num_of_row == 4:
            duration_text = 'Camera5'
            ip = ip_c5
            name = name_c5                        
    #dash_app.process = process(duration_data)
    dash_app.layout = create_layout(dash_app, data, duration_data)
    
    # Callback to update data every second
    @dash_app.callback(Output('total-count', 'children'),  # Update 'total-count' component
              Output(ids.MEN_WOMEN_TOTAL_COUNT_PLACEHOLDER, 'children'),  # Update men count component
              Output(ids.CATEGORY_COUNT_PLACEHOLDER, 'children'),
              Output(ids.DURATION_COUNT_PLACEHOLDER, "children"),
              Output(ids.CLIENTSIDE_TYPE_GRAPH, "value"),
              Output('title-text', 'children'),       
              Input('interval-component', 'n_intervals'),
              Input(ids.GENDER_DROPDOWN, "value"),
              Input(ids.CATEGORY_DROPDOWN, "value"),
              Input(ids.DURATION_DROPDOWN, "value"))
    
    def update_data(n_intervals, genders: list[str], categories: list[str], selected_duration: str
    ) -> tuple:
        duration_data = pd.read_csv(NEW_DATA_DURATION_PATH)
        client_side_data = pd.read_csv(STATUS_CLIENT_SIDE)
        data = pd.read_csv(DATA_PATH).query(
            "gender in @genders and category in @categories and duration == @selected_duration and count == 'yes'"
        )
        
        # Calculate updated values for various components
        updated_total_count = data[data['count'] == 'yes'].shape[0]
        total_count_text = f"{updated_total_count}"
        
        updated_men_count = data[data['gender'] == 'Men'].shape[0]
        updated_women_count = data[data['gender'] == 'Women'].shape[0]
       # Apply different colors to different parts of the text
        men_women_count_text = html.Span([
            html.Span(f"{updated_men_count}", style={'color': '#0070FE'}),
            html.Span(" / ", style={'color': 'black'}),
            html.Span(f"{updated_women_count}", style={'color': '#F786D3'})
        ])
         
        children_count = data[data['category'] == 'Children'].shape[0]
        student_count = data[data['category'] == 'Student'].shape[0]
        working_count = data[data['category'] == 'Working'].shape[0]
        disabled_count = data[data['category'] == 'Disabled'].shape[0]
        updated_category_count = f"Children {children_count}<br>Disabled {disabled_count}<br>Student {student_count}<br>Working {working_count}"
        category_count_text = f"{updated_category_count}"
        category_count_text = html.P(
            id=ids.CATEGORY_COUNT_PLACEHOLDER,
            children=[
                html.P(line, style={'margin': '0',
                        'color': '#496AFA' if 'Children' in line else
                                 '#14E49D' if 'Student' in line else
                                 '#AD62F1' if 'Working' in line else
                                 '#FA6249' if 'Disabled' in line else
                                 None}) for line in category_count_text.split('<br>')
            ],
            style={
                'textAlign': 'center',
                'color': '#0070FE',
                'fontSize': 20}
        )
        total_duration = len(data[['duration', 'hour']].drop_duplicates())
        number_of_days = total_duration // 12
        unique_dates = pd.to_datetime(data['duration'], format='%b %d %p').dt.date.unique()
        number_of_days_ = len(unique_dates)
        
        filtered_video_duration = duration_data.query("duration == @selected_duration")
        sum_video_duration = filtered_video_duration['video_duration'].sum()
        
        def convert_to_days_hours_minutes(total_sec):
            hours = total_sec // 3600
            minutes = (total_sec % 3600) // 60
            return f"{int(hours)} hr {int(minutes)} min"
        
        formatted_duration = convert_to_days_hours_minutes(sum_video_duration)
        updated_duration_count = f"{number_of_days_} day<br>({formatted_duration})"
        duration_count_text = f"{updated_duration_count}"
        
        if number_of_days == 0:
            duration_text = html.P(
                id=ids.DURATION_COUNT_PLACEHOLDER,
                children=[
                    html.P(line, style={'margin': '0'}) for line in duration_count_text.split('<br>')
                    ]
            )
        else:
            duration_text = html.P(
                id=ids.DURATION_COUNT_PLACEHOLDER,
                children=[
                    html.P(line, style={'margin': '0'}) for line in duration_count_text.split('<br>')
                ]
            )
    
        client_side = client_side_data['cs'].loc[0] if not client_side_data.empty else None
        
        existing_data = pd.read_csv(DATA2)
        duration_text = None
        ip = None
        name = None
        ip_c1 = existing_data.loc[0, 'IP'] if not existing_data.empty else None
        ip_c2 = existing_data.loc[1, 'IP'] if len(existing_data) >= 2 else None
        ip_c3 = existing_data.loc[2, 'IP'] if len(existing_data) >= 3 else None
        ip_c4 = existing_data.loc[3, 'IP'] if len(existing_data) >= 4 else None
        ip_c5 = existing_data.loc[4, 'IP'] if len(existing_data) >= 5 else None
        name_c1 = existing_data.loc[0, 'Name'] if not existing_data.empty else None
        name_c2 = existing_data.loc[1, 'Name'] if len(existing_data) >= 2 else None
        name_c3 = existing_data.loc[2, 'Name'] if len(existing_data) >= 3 else None
        name_c4 = existing_data.loc[3, 'Name'] if len(existing_data) >= 4 else None
        name_c5 = existing_data.loc[4, 'Name'] if len(existing_data) >= 5 else None
        num_of_row = client_side_data['row_num'].loc[0] if not client_side_data.empty else None
        print(ip_c1,ip_c2,ip_c3,ip_c4,ip_c5)
        print(name_c1,name_c2,name_c3,name_c4,name_c5)
        print(num_of_row)
        if num_of_row == 0:
                duration_text = 'Camera1'
                ip = ip_c1
                name = name_c1
        elif num_of_row == 1:
                duration_text = 'Camera2'
                ip = ip_c2
                name = name_c2
        elif num_of_row == 2:
                duration_text = 'Camera3'
                ip = ip_c3
                name = name_c3
        elif num_of_row == 3:
                duration_text = 'Camera4'
                ip = ip_c4
                name = name_c4        
        elif num_of_row == 4:
                duration_text = 'Camera5'
                ip = ip_c5
                name = name_c5                        
        #dash_app.process = process(duration_data)
        title = f'{duration_text}_{ip}_{name}'
    
        # Return the updated text for each component
        return total_count_text, men_women_count_text, category_count_text, duration_text, client_side, title
    
    return dash_app
