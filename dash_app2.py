#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from device_info import get_recommended_list, get_device_list

# Set directory to where the data is
os.chdir("C:/Users/pcle008/Box Sync/IOT Trial/DashApp/data")

minute_data = pd.read_csv(
    "StanfordMedicalSchool_power_data.csv",
    skiprows=7,
    low_memory=False)

# df = get_recommended_list()
df = get_device_list()
device_options = []
for i in range(0, len(df)):
    device_options.append(
        {'label': df['Device'][i], 'value': df['socket_ids'][i]})


def to_datetime(timestamp):
    return dt.strptime(timestamp, '%Y-%m-%d %H:%M:%S %Z')


def get_socket(socket, dataset=minute_data):
    df = pd.DataFrame(columns=['Timestamp', 'Power'])
    df['Timestamp'] = dataset.iloc[4:, 0].apply(to_datetime)
    df['Power'] = dataset[socket][4:]
    return df


app = dash.Dash()

app.layout = html.Div([
    html.H1('Stanford Medical School - IBIS Data Exploration'),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt(2019, 4, 28),
        max_date_allowed=dt(2019, 6, 12),
        # initial_visible_month=dt(2019, 4, 28),
        start_date=dt(2019, 4, 29, 0, 0, 0),
        end_date=dt(2019, 4, 30, 0, 0, 0),
        with_portal=True),
    dcc.Graph(id='graph'),
    dcc.Dropdown(
        id='device_picker',
        options=device_options,
        value=df['socket_ids'][0])
])


@app.callback(Output('graph', 'figure'),
              [Input('device_picker', 'value'),
               Input('my-date-picker-range', 'start_date'),
               Input('my-date-picker-range', 'end_date')])
def update_figure(socket, start, end):
    filtered = get_socket(socket)
    filtered = filtered[
        (filtered['Timestamp'] >= start)
        & (filtered['Timestamp'] <= end)
    ]
    traces = []
    traces.append(go.Scatter(
        x=filtered['Timestamp'],
        y=filtered['Power'],
        mode='lines')
    )

    return {
        'data': traces,
        'layout': go.Layout(
            title=socket,
            xaxis=dict(
                title='Time'  # , rangeslider=dict(visible=True)
            ),
            yaxis=dict(title='Power (Watts)')
        )
    }


if __name__ == "__main__":
    app.run_server()
