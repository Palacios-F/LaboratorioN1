import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def pie_com(weights: "dataframe of weights with Tickers"):
    fig = px.pie(weights, values='Weights (%)', names=weights.index, title='Portofolio Composition',
            template='plotly_dark')
    fig.show()
    return

def returns_plot(table_returns):
    fig = px.line(table_returns.Capital, title = "Amount in portfolio")
    fig.show()
    return