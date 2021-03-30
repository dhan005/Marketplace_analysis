import pandas as pd 
import numpy as np 
import seaborn as sns 
import warnings 
warnings.filterwarnings('ignore')
from datetime import datetime 
import plotly.graph_objs as go 
#dash plotly libraries 
import dash    
import dash_core_components as dcc 
import dash_html_components as html 
import dash_table as dt 
import dash_auth 
from dash.dependencies import Input, Output, State 

#pull data from local desktop 
pd.set_option('display.max.columns', 30)
pd.options.display.float_format="{:,.2f}".format
df = pd.read_csv(r'/Users/Dhan004/Desktop/supermarket_sales - Sheet1.csv', low_memory=False)
#rename column names
df2 = df.rename(columns={'Invoice ID': 'Invoice ID', 'Branch': 'Branch', 'City': 'City', 'Customer type': 'Customer Type', 'Gender': 'Gender', 'Product line': 'Product Line', 'Unit price': 'Unit Price','cogs': 'COGS', 'gross margin percentage': 'Gross Margin Percentage', 'gross income': 'Gross Income', 'Total': 'Net Revenue'})
df2.sort_values(by='Date', ascending=True, inplace=True)
df2['Date'] = pd.to_datetime(df2['Date'])

#pre define data samples 
#get net revenue by city and customer type and gender 
Total_sales = df2.groupby(['Branch'])[['City', 'Customer Type', 'Gender', 'Net Revenue']].sum().reset_index()
#bar horozontal - product ratings 
product_ratings = df2.groupby('Product Line')[['Product Line','Rating']].mean().reset_index() 
#figures - 1, 2, 3, 4 
#Total Sales by Revenue - Fig1 - will need to add dates 2019 - 2021
fig1 = go.Figure(data=[go.Bar(x=Total_sales['Branch'], y=Total_sales['Net Revenue'])],layout=go.Layout({'paper_bgcolor': 'black', 'plot_bgcolor': 'black', 'font_color':'white'})) 
#Get average Ratings on Product Line 
fig2 = go.Figure(data=[go.Bar(x=product_ratings['Product Line'], y=product_ratings['Rating'], orientation='h')],layout=go.Layout({'paper_bgcolor': 'black', 'plot_bgcolor': 'black', 'font_color':'white'})) 
#Interactive pie chart on product lines 
products = df2['Product Line'].value_counts()
labels = df2['Product Line'].unique()
fig3 = go.Figure(data=[go.Pie(values=products, labels=labels)], layout=go.Layout({'paper_bgcolor': 'black', 'plot_bgcolor': 'black', 'font_color':'white'})) 
#Interactive LineChart 
gender = df2[['City', 'Quantity', 'Date', 'Rating', 'Invoice ID', 'Net Revenue']]
grouped_genders = gender.groupby('Date')['Quantity'].sum().reset_index()
fig4 = go.Figure(data=[go.Scatter(x=grouped_genders['Date'], y=grouped_genders['Quantity'], mode='lines+markers', marker={'color': 'firebrick', 'size': 2}, name='Quantities purchased by gender')], layout=go.Layout({'paper_bgcolor': 'black', 'plot_bgcolor': 'black', 'font_color':'white'}))
fig4

Branch = ['A', 'B', 'C']
#set up apps 
app = dash.Dash() 

#basic authentication 
valid_username_ids = {
    'dhan': 'dashboard9091!'
}

auth = dash_auth.BasicAuth(
    app, 
    valid_username_ids
)
#layout 
app.layout = html.Div(style={'backgroundColor': 'black'}, children=[
    html.Div([
        html.H3('Marketplace Analysis - 2019')
    ], style={'textAlign': 'center', 'font': 18, 'color': 'white'}), 
    html.Div([
        html.H4('Revenue by Branch'), 
        dcc.Graph(id='barchart1', figure=fig1)
    ], style={'textAlign': 'center', 'width': '33%', 'display': 'inline-block', 'color': 'white'}), 
    html.Div([
        html.H4('Product Line Purchase - Percentage'), 
        dcc.Graph(id='piechart1', figure=fig3)
    ],style={'textAlign': 'center', 'width': '33%', 'display': 'inline-block', 'color': 'white'}),
    html.Div([
        html.H4('Product Rating - Average'), 
        dcc.Graph(id='barchart2', figure=fig2)
    ],style={'textAlign': 'center', 'width': '33%', 'display': 'inline-block', 'color': 'white'}),
    html.Div([
        html.H4('Net Revenue - Year 2019'), 
        dcc.Graph(id='lineChart1',figure=fig4)
    ],style={'textAlign': 'center', 'width': '100%', 'display': 'inline-block', 'color': 'white'}),
    html.Div([
        html.H4('Data Reference - Download'), 
        dt.DataTable(id='dataTable', 
        columns = [{'labels': i, 'data': i} for i in df2.columns], 
        data=df2.to_dict('records'), 
        editable=True,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=False,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=6,                # number of rows visible per page
        export_format='csv',
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
            }
        )
    ])


])


if __name__ == "__main__":
    app.run_server(port=8050, host='0.0.0.0')
