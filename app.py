import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_auth

VALID_USERNAME_PASSWORD_PAIRS = {
    "username": "password",
}

app = Dash(__name__)
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

try:
    df_bitcoin = pd.read_csv("bitcoin_dataset.csv", 
                            delimiter=',', 
                            quotechar='"',  
                            on_bad_lines='warn')
    print("Bitcoin data loaded successfully")
except Exception as e:
    print(f"Error loading Bitcoin data: {e}")
    df_bitcoin = pd.DataFrame()  

try:
    df_tesla = pd.read_csv("tesla.csv", 
                            delimiter=',', 
                            quotechar='"',  
                            on_bad_lines='warn')
    print("Tesla data loaded successfully")
except Exception as e:
    print(f"Error loading Tesla data: {e}")
    df_tesla = pd.DataFrame()  

df_bitcoin.columns = df_bitcoin.columns.str.lower()
df_tesla.columns = df_tesla.columns.str.lower()

df_bitcoin['date'] = pd.to_datetime(df_bitcoin['date'])
df_tesla['date'] = pd.to_datetime(df_tesla['date'])

df_combined = pd.merge(df_bitcoin[['date', 'btc_market_price']],
                       df_tesla[['date', 'close']],
                       on='date')

print("Missing values in combined DataFrame:")
print(df_combined.isna().sum())

df_long = pd.melt(df_combined, id_vars=['date'], value_vars=['btc_market_price', 'close'], 
                  var_name='asset', value_name='price')

fig = px.line(df_long, x='date', y='price', color='asset', 
              labels={
                  'price': 'Price (USD)', 
                  'asset': 'Asset'
              },
              title='Bitcoin vs Tesla Prices Over Time')

app.layout = html.Div([
    html.H4('Bitcoin vs Tesla Prices Over Time'),
    dcc.Graph(id='graph', figure=fig),  # Set the figure directly here
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)