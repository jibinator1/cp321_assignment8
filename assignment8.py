import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
data = [
    {'Year': 1930, 'Host': 'Uruguay', 'Winner': 'Uruguay', 'Runner-up': 'Argentina'},
    {'Year': 1934, 'Host': 'Italy', 'Winner': 'Italy', 'Runner-up': 'Czechoslovakia'},
    {'Year': 1938, 'Host': 'France', 'Winner': 'Italy', 'Runner-up': 'Hungary'},
    {'Year': 1950, 'Host': 'Brazil', 'Winner': 'Uruguay', 'Runner-up': 'Brazil'},
    {'Year': 1954, 'Host': 'Switzerland', 'Winner': 'Germany', 'Runner-up': 'Hungary'},
    {'Year': 1958, 'Host': 'Sweden', 'Winner': 'Brazil', 'Runner-up': 'Sweden'},
    {'Year': 1962, 'Host': 'Chile', 'Winner': 'Brazil', 'Runner-up': 'Czechoslovakia'},
    {'Year': 1966, 'Host': 'England', 'Winner': 'England', 'Runner-up': 'Germany'},
    {'Year': 1970, 'Host': 'Mexico', 'Winner': 'Brazil', 'Runner-up': 'Italy'},
    {'Year': 1974, 'Host': 'Germany', 'Winner': 'Germany', 'Runner-up': 'Netherlands'},
    {'Year': 1978, 'Host': 'Argentina', 'Winner': 'Argentina', 'Runner-up': 'Netherlands'},
    {'Year': 1982, 'Host': 'Spain', 'Winner': 'Italy', 'Runner-up': 'Germany'},
    {'Year': 1986, 'Host': 'Mexico', 'Winner': 'Argentina', 'Runner-up': 'Germany'},
    {'Year': 1990, 'Host': 'Italy', 'Winner': 'Germany', 'Runner-up': 'Argentina'},
    {'Year': 1994, 'Host': 'United States', 'Winner': 'Brazil', 'Runner-up': 'Italy'},
    {'Year': 1998, 'Host': 'France', 'Winner': 'France', 'Runner-up': 'Brazil'},
    {'Year': 2002, 'Host': 'South Korea/Japan', 'Winner': 'Brazil', 'Runner-up': 'Germany'},
    {'Year': 2006, 'Host': 'Germany', 'Winner': 'Italy', 'Runner-up': 'France'},
    {'Year': 2010, 'Host': 'South Africa', 'Winner': 'Spain', 'Runner-up': 'Netherlands'},
    {'Year': 2014, 'Host': 'Brazil', 'Winner': 'Germany', 'Runner-up': 'Argentina'},
    {'Year': 2018, 'Host': 'Russia', 'Winner': 'France', 'Runner-up': 'Croatia'},
    {'Year': 2022, 'Host': 'Qatar', 'Winner': 'Argentina', 'Runner-up': 'France'},
]#make a list of dictionaries for the year. host winner and runnerup

df = pd.DataFrame(data)
wins = df['Winner'].value_counts().reset_index()
wins.columns = ['Country', 'Wins']
#initalize dash
app = Dash(__name__)

#use the wins df to get the locations of the countries, change colour by number of wins, when hovered show the country name,and find hte country by its name  to create a chjoropleth map
base_fig = px.choropleth(
    wins,
    locations="Country",
    color="Wins",
    hover_name="Country",
    locationmode='country names',
    color_continuous_scale=px.colors.sequential.Plasma
)

#title and type of map
base_fig.update_layout(title_text='FIFA World Cup Wins By the Country', geo=dict(projection_type='equirectangular'))

#set the layout
app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={'textAlign': 'center'}),#title header in the cetner
    
    #display graph set the id to choropleth
    dcc.Graph(id='choropleth', figure=base_fig, style={'height': '60vh'}),
    
    #new div
    html.Div([
        html.Label("Select Country:"),#label with the text Select Country
        dcc.Dropdown(id='country-dropdown',options=[{'label': i, 'value': i} for i in wins['Country']]),#create a drop down menu with the list of countries
        html.Div(id='country-output', style={'margin': '1rem'})#just to add spacing
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '1rem'}),
    
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(id='year-dropdown',options=[{'label': str(i), 'value': i} for i in df['Year']]),#same thing for year
        html.Div(id='year-output', style={'margin': '1rem'})
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '1rem'})
])

@app.callback(
    Output('choropleth', 'figure'),#map changes
    [Input('country-dropdown', 'value'),Input('year-dropdown', 'value')]#userinput
)
def update_map(selected_country, selected_year):
    fig = go.Figure(base_fig)
    
    if selected_country:#if country is slected
        #add a scattergeo to mark a country, and select the country by the country anme, and need the extra for some reason to remove the extra country name to repeat
        fig.add_trace(go.Scattergeo(locations=[selected_country],locationmode='country names',hovertemplate=f"<b>{selected_country}</b><extra></extra>"))
    
    if selected_year:#if the year is selected
        year_data = df[df['Year'] == selected_year]
        winner = year_data['Winner'].values[0]
        runner_up = year_data['Runner-up'].values[0]
        #same thing as selected country
        fig.add_trace(go.Scattergeo(locations=[winner],locationmode='country names', hovertemplate=f"<b>Winner {selected_year}: {winner}</b><extra></extra>"))
        
        fig.add_trace(go.Scattergeo(locations=[runner_up],locationmode='country names',hovertemplate=f"<b>Runner-up {selected_year}: {runner_up}</b><extra></extra>"))
    
    return fig

@app.callback(
    Output('country-output', 'children'),#add the country name to the div
    [Input('country-dropdown', 'value')]#userinput
)
def update_country_info(country):
    if not country:#if there is no country then return nothing
        return ""
    count = wins[wins['Country'] == country]['Wins'].values[0]#get the number of wins the slected country has
    return html.Div([html.H3(country),html.P(f"Total World Cup Wins: {count}"),], style={'padding': '1rem'})


@app.callback(
    Output('year-output', 'children'),#add the year to the div
    [Input('year-dropdown', 'value')]#userinput
)
def update_year_info(year):
    if not year:#if there is no year then return nothing
        return ""
    info_on_year = df[df['Year'] == year]
    return html.Div([
        html.H3(f"{year} World Cup"),#add a header to the eyar-output year-output
        html.P(f"Host: {info_on_year['Host'].values[0]}"),#get the host of the year
        html.P(f"Winner: {info_on_year['Winner'].values[0]}"),#winner
        html.P(f"Runner-up: {info_on_year['Runner-up'].values[0]}"),#and the runner up
    ], style={'padding': '1rem'})

if __name__ == '__main__':
    app.run(debug=True)