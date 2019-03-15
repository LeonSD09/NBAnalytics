#from importlib import reload
#scu = reload(scu)
##########################################################################################
# Imports and Setup

import statcrosser_utils as scu
import pandas as pd
from datetime import date, timedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.offline as pyo
import plotly.graph_objs as go

# Instantiate the StatCrosser Utilities object
utils = scu.StatCrosser_Utils()
#utils.__dict__

##########################################################################################
# Create the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

##########################################################################################
# Create all of the dashboard elements (from top to bottom)

# Header Text
header_md = """
**NBA StatCrosser, 2018-19**
_by Leon D'Angio_
"""

# Top Controls
# Choose Date Range, Measure Types, X-Axis, Y-Axis, Update Chart

""" DATE RANGE
DatePickerRange: https://dash.plot.ly/dash-core-components/datepickerrange
"""
dts = pd.date_range('2018-10-16', (date.today() - timedelta(1)).strftime('%Y-%m-%d'))
date_range_slider = html.Div([
    dcc.Markdown("**Date Range**"),
    dcc.DatePickerRange(id='dt-range',
                    start_date=dts[0],
                    end_date=dts[-1],
                    display_format='MMM Do, YYYY'
                   )
], style={'width': '50%', 'display':'inline-block', 'padding': '20px'})

""" MEASURE TYPE
Checklist: https://dash.plot.ly/dash-core-components/checklist
"""
mt_options = [{'label': k, 'value': v} for k, v in utils.measure_type_opts.items()]
measure_type_select = html.Div([
    dcc.Markdown("**Measure Type**"),
    dcc.Checklist(id='measure-type-check',
                  options=mt_options,
                  values=['Base'],
                  labelStyle={'display': 'inline-block',
                              'font-size': '20px',
                              'padding': '10px'}
                 )
], style={'width': '50%', 'display':'inline-block', 'padding': '20px'})

##########################################################################################
# Create the layout

app.layout = html.Div([
    dcc.Markdown(header_md),
    html.Hr(),
    html.Div([
        date_range_slider,
        measure_type_select
        ], style={'display': 'inline-block'}),
])

##########################################################################################
# Main
if __name__ == '__main__':
    app.run_server()
