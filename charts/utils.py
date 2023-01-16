import csv
import plotly.express as px
import pandas as pd

def get_delimiter(file_path):
    with open(file_path, 'r') as csvfile:
        delimiter = str(csv.Sniffer().sniff(csvfile.read()).delimiter)
        return delimiter  

def createchart(x, y, data, chart_type):
    df = pd.read_csv(data.workingfile.path)
    width = 450
    height = 350
    if chart_type == 'bar':
        fig = px.bar(df, x=x, y=y, width=width, height = height)
    elif chart_type == 'line':
        fig = px.line(df, x=x, y=y, markers=True, width=width, height = height)
    elif chart_type == 'pie':
        fig = px.pie(df, values=y, names=x, width=width, height = height)
    elif chart_type == 'doughnut':
        fig = px.pie(df, values=y, names=x, hole=0.4, width=width, height = height)
    fig_html = fig.to_html()
    return fig_html