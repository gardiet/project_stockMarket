# 2025-06-14
#
# TOP. Ejemplo personalizado para examinar la evolución de la acciones
#
# Link:  
#
# Dash with yfinance
# Por alguna razón, no se ven los datos en el gráfico. Solucionado, ver comentario en el código
# 

import yfinance as yf
import yfinance.shared as yfshared
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import datetime

app = Dash()

server = app.server

app.layout = html.Div(
    style={"background": "#111111", "color": "#FFFFFF", "padding": "20px"},
    children=[
        html.H1("Stock Market Tool", style={"texAlign": "center", "color": "#FFFFFF"}),
        html.Div([
            html.Label(children="Stock Ticker Simbol: ", style={"color": "#FFFFFF"}),
            dcc.Input(
                id="ticker-input", 
                type="text", 
                value="AAPL", 
                style={"backgroundColor": "#333333", "color": "#FFFFFF"})
        ], style={"padding": "10px"}),
        html.Div([
            html.Label(children="Start Date: ", style={"color": "#FFFFFF"}),
            dcc.DatePickerSingle(
                id="start-date-picker", 
                date="2025-03-01")
        ], style={"padding": "10px"}),        
        html.Div([
            html.Label(children="End Date: ", style={"color": "#FFFFFF"}),
            dcc.DatePickerSingle(
                id="end-date-picker", 
                date="2025-06-01")
        ], style={"padding": "10px"}),     
        html.Div([
            html.Button(children="Submit", id="submit-button", n_clicks=0, style={"backgroundColor": "#444444", "color": "#FFFFFF"})
        ], style={"padding": "10px", "textAlign": "center"}),    

        html.Div(
            id="chart-container",
            style={"visibility": "hidden"},
            children=[
                html.Div([
                    dbc.Container([
                        dbc.Row([
                            dbc.Col(
                                html.Div([
                                    html.Div([
                                        html.Label(children="Start: ", style={"color": "#A8A8A8"}),
                                        html.Label(id="start-value", children="", style={"color": "#A8A8A8"}),
                                    ]),
                                    html.Div([
                                        html.Label(children="End: ", style={"color": "#A8A8A8"}),
                                        html.Label(id="end-value", children="", style={"color": "#A8A8A8"})
                                    ]),
                                    html.Div([
                                        html.Label(children="Diff: ", style={"color": "#A8A8A8"}),
                                        html.Label(id="diff-start-end", children="", style={"color": "#A8A8A8"})
                                    ])                               
                                ]), style={
                                        'display': 'inline-block',
                                        'width': '25%',
                                        'padding': 10,
                                        'textAlign': 'center',
                                        "border": "2px black solid",
                                        "margin": "20px"
                                    }
                            ),
                            dbc.Col(
                                html.Div([
                                    html.Div([
                                        html.Label(children="Higher value: ", style={"color": "#A8A8A8"}),
                                        html.Label(id="higher-value-value", children="", style={"color": "#0B6623"}),
                                    ]),
                                    html.Div([
                                        html.Label(children="Date: ", style={"color": "#A8A8A8"}),
                                        html.Label(id="higher-value-date", children="", style={"color": "#0B6623"})
                                    ])
                                ]), style={
                                        'display': 'inline-block',
                                        'width': '25%',
                                        'padding': 10,
                                        'textAlign': 'center',
                                        "border": "2px black solid",
                                        "margin": "20px"
                                    }
                            ),                       
                            dbc.Col(
                                html.Div([
                                    html.Div([
                                        html.Label(children="Lower value: ", style={"color": "#A8A8A8"}),
                                        html.Label(id="lower-value-value", children="", style={"color": "#AA4A44"}),
                                    ]),
                                    html.Div([
                                        html.Label(children="Date: ", style={"color": "#A8A8A8"}),
                                        html.Label(id="lower-value-date", children="", style={"color": "#AA4A44"})
                                    ])
                                ]), style={
                                        'display': 'inline-block',
                                        'width': '25%',
                                        'padding': 10,
                                        'textAlign': 'center',
                                        "border": "2px black solid",
                                        "margin": "20px"
                                    }
                            ),
                        ])
                    ])     
                ]), 
                html.Div([
                    dcc.Graph(id="candlestick-chart", style={"backgroundColor": "#111111", "padding": "10px"})
                ])
            ]
        ),

        html.Div(
            children=[
                html.Label(id="status-text", children="", style={"color": "#FFFFFF"})
            ]
        )
    ]
)

@app.callback(
    [Output("candlestick-chart", "figure"),
     Output("chart-container", "style"),
     Output("start-value", "children"),
     Output("end-value", "children"),
     Output("diff-start-end", "children"),
     Output("higher-value-value", "children"),
     Output("higher-value-date", "children"),
     Output("lower-value-value", "children"),
     Output("lower-value-date", "children"),
     Output("status-text", "children")],
    [Input("submit-button", "n_clicks")],
    [State("ticker-input", "value"),
     State("start-date-picker", "date"),
     State("end-date-picker", "date")]
)
def update_ticker(n_clicks, ticker, start_date, end_date):
    dNow = datetime.datetime.now()
    dNowf = dNow.strftime("%Y-%m-%d %H:%M:%S")

    if n_clicks > 0:
        df= yf.download(ticker, start=start_date, end=end_date)
        
        if yfshared._ERRORS:
            errorText = list(yfshared._ERRORS.items())
            return go.Figure(), {"visibility": "hidden"}, "", "", "", "", "", "", "", f"{dNowf} - Yfinance ERROR - {errorText}"
        else:
            tickerInfo = yf.Ticker(ticker)
            info = tickerInfo.info

            df.columns = df.columns.droplevel(1)   # Solution: https://stackoverflow.com/questions/79311930/empty-plotly-candlestick-chart-with-yfinance-download

            dfp1 = pd.DataFrame(df)            # Convert to pandas format
            dfp = dfp1.reset_index(['Date'])   # Convert date index in a column
            
            dfp_start = dfp.head(1)
            start_value = dfp_start["Open"].iloc[0]
            dfp_end = dfp.tail(1)
            end_value = dfp_end["Close"].iloc[0]
            diff_values = f"{(end_value - start_value)/start_value*100:+.2f} %"

            dfp_higher_value = dfp[dfp['High']==dfp['High'].max()]
            hmaxValue = dfp_higher_value["High"].iloc[0]
            hmaxValueF = hmaxValue
            hmaxDate = dfp_higher_value["Date"].iloc[0]
            hmaxDateF = hmaxDate.date()

            dfp_lower_value = dfp[dfp['Low']==dfp['Low'].min()]
            hlowValue = dfp_lower_value["Low"].iloc[0]
            hlowValueF = hlowValue
            hlowDate = dfp_lower_value["Date"].iloc[0]
            hlowDateF = hlowDate.date()

            fig = go.Figure(data=[
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    close=df["Close"],
                    high=df["High"],
                    low=df["Low"]
                )
            ])

            fig.update_layout(
                title=f"Candlestick Char of {ticker}",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                xaxis_rangeslider_visible=False,
                template="plotly_dark"
            )

            return fig, {"visibility": "visible"}, start_value, end_value, diff_values, hmaxValueF, hmaxDateF, hlowValueF, hlowDateF, f"{dNowf} - {info.get('shortName', 'N/A')} - {info.get('market', 'N/A')} - {info.get('sector', 'N/A')}"
    else:
        return go.Figure(), {"visibility": "hidden"}, "", "", "", "", "", "", "", ""
        
        # To test the upper boxes
        # return go.Figure(), {"visibility": "visible"}, "", "", "", "", "", "", "", ""



if __name__ == "__main__":
    app.run(debug=True)
