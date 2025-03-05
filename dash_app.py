# Important Imports -------------------------------------------------------

from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd

# Data Prep ---------------------------------------------------------------

temp = pd.read_csv("./GDP_Data.csv")
gdp_df = temp[temp["PRICE_BASE"] == "V"]
temp = pd.read_csv("./Waste_Data.csv")
waste_df = temp[temp["Unit of measure"] == "Kilogrammes per person"]

# App & Layout ------------------------------------------------------------

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H1(
                        [
                            "Contrasting Global GDP and Municipal Waste",
                        ],
                        style={'textAlign': 'center'},
                    ),
                ],
                width=12,
            ),
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(
                            [
                                "Map Dataset:"
                            ]
                        )
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="dataset-dropdown",
                            options=[
                                {"label": "Global GDP", "value": "GDP"},
                                {"label": "Global Municipal Waste", "value": "Waste"},
                            ],
                            value="GDP"
                        )
                    ],
                    width=6,
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.H2(
                        [
                            "Global GDP in 1975",
                        ],
                        id="choropleth-title",
                        style={'textAlign': 'center'},
                    ),
                    dcc.Graph(id="choropleth", figure={}),
                ],
                width=12,
            ),
        ),
        dbc.Row(
            dbc.Col(
                [
                    dcc.Slider(
                        id="time-bar",
                        min=1975,
                        max=2020,
                        value=1975,
                        step=1,
                        marks={
                            1975: "1975",
                            1980: "1980",
                            1985: "1985",
                            1990: "1990",
                            1995: "1995",
                            2000: "2000",
                            2005: "2005",
                            2010: "2010",
                            2015: "2015",
                            2020: "2020",
                        },
                        tooltip={"always_visible": True, "placement": "top", },
                        updatemode="drag",
                    ),
                ],
                width=12,
            ),
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.H2(
                        [
                            "GDP Versus Municipal Waste in USA"
                        ],
                        id="comparison-title",
                        style={'textAlign': 'center'},
                    ),
                    dcc.Graph(id="comparison-line", figure={}),
                ],
            ),
        ),
    ],
    className="row"
)


# Callbacks --------------------------------------------------------------

@app.callback(
    Output("choropleth-title", "children"),
    Input("time-bar", "value"),
    Input("dataset-dropdown", "value")
)
def update_gdp_title(year, dataset):
    return "Global " + str(dataset) + " in " + str(year)


@app.callback(
    Output("choropleth", "figure"),
    Input("time-bar", "value"),
    Input("dataset-dropdown", "value")
)
def update_gdp_graph(year, dataset):
    if dataset == "GDP":
        df = gdp_df
        label = "GDP"
    else:
        df = waste_df
        label = "kg of waste per person"
    dff = df[df["TIME_PERIOD"] == year]
    fig = px.choropleth(
        data_frame=dff,
        locations="REF_AREA",
        color="OBS_VALUE",
        scope="world",
        hover_data={"REF_AREA": False, "Reference area": True},
        hover_name="Reference area"
    )
    fig.update_layout(
        coloraxis_colorbar_title=label,
        geo={"projection": {"type": "natural earth"}},
        margin=dict(l=50, r=50, t=50, b=50),
    )
    return fig


@app.callback(
    Output("comparison-title", "children"),
    Input("choropleth", "clickData")
)
def update_gdp_title(selected_area):
    if selected_area is None:
        return "GDP Versus Municipal Waste in United States of America"
    country = selected_area["points"][0]["hovertext"]
    return "GDP Versus Municipal Waste in " + str(country)


@app.callback(
    Output("comparison-line", "figure"),
    Input("choropleth", "clickData"),
    Input("time-bar", "value"),
)
def update_comparison(selected_area, year):
    if selected_area is None:
        country = "United States"
    else:
        country = str(selected_area["points"][0]["hovertext"])
    gdp_dff = gdp_df[gdp_df["Reference area"] == country]
    waste_dff = waste_df[waste_df["Reference area"] == country]
    combined_df = pd.merge(gdp_dff, waste_dff, on="TIME_PERIOD")
    combined_df = combined_df.sort_values("TIME_PERIOD")
    fig = go.Figure()
    fig.add_trace(
        go.Line(
            x=combined_df["TIME_PERIOD"],
            y=combined_df["OBS_VALUE_x"],
            name="GDP per capita (Dollars)",
            yaxis="y1",
        )
    )
    fig.add_trace(
        go.Line(
            x=combined_df["TIME_PERIOD"],
            y=combined_df["OBS_VALUE_y"],
            name="Waste per capita (kg)",
            yaxis="y2",
        )
    )
    fig.update_layout(
        shapes=[
            dict(
                type="line",
                x0=year,
                x1=year,
                y0=0,
                y1=1,
                xref="x",
                yref="paper",
                line=dict(color="gray", width=2, dash="dash")
            ),
        ],

        xaxis=dict(
            title="year",
            range=[combined_df["TIME_PERIOD"].min(),combined_df["TIME_PERIOD"].max()]
        ),
        yaxis=dict(
            title="GDP per capita (Dollars)",
            title_font=dict(size=16, color="blue"),
            tickfont=dict(size=12, color="darkblue"),
            side="left",
        ),
        yaxis2=dict(
            title="Waste per capita (kg)",
            title_font=dict(size=16, color="red"),
            tickfont=dict(size=12, color="darkred"),
            overlaying="y",
            side="right",
        ),
    )
    return fig


# Run  -------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
