import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash import dash

from bootcamp_2021_01.domain.dash_components.banner import banner
from bootcamp_2021_01.domain.feature_engineering.target_definition import COMPANY_NAME_COLUMN, COUNTRY_CODE_COLUMN, \
    CITY_COLUMN, SUCCESSFUL_SERIES_A_COLUMN
from bootcamp_2021_01.gui.ekilibr8_state import Ekilibr8, SCORE_COLUMN

SCORE_COLOR_COLUMN = 'score_color'

PREDICTED_SCORES_COLUMN_TITLE = 'Scores'
SUCCESS_STATUS_COLUMN_TITLE = 'Success'
CITY_COLUMN_TITLE = 'City'
COUNTRY_NAME_COLUMN_TITLE = 'Country'
COMPANY_NAME_COLUMN_TITLE = 'Company Name'

RGB_WHITE = 'rgba(256,256,256,1)'


def layout(state: Ekilibr8, app: dash.Dash) -> html.Div:
    colored_score_column = state.input_data_with_features_and_scores[SCORE_COLUMN].apply(_define_score_color)
    displayed_data = state.input_data_with_features_and_scores \
        .assign(**{SCORE_COLOR_COLUMN: colored_score_column})

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=[
                    COMPANY_NAME_COLUMN_TITLE,
                    COUNTRY_NAME_COLUMN_TITLE,
                    CITY_COLUMN_TITLE,
                    SUCCESS_STATUS_COLUMN_TITLE,
                    PREDICTED_SCORES_COLUMN_TITLE
                ]),
                cells=dict(
                    values=[
                        displayed_data[COMPANY_NAME_COLUMN],
                        displayed_data[COUNTRY_CODE_COLUMN],
                        displayed_data[CITY_COLUMN],
                        displayed_data[SUCCESSFUL_SERIES_A_COLUMN],
                        displayed_data[SCORE_COLUMN].apply(_percentage_display)
                    ],
                    fill=dict(color=[
                        RGB_WHITE,
                        RGB_WHITE,
                        RGB_WHITE,
                        RGB_WHITE,
                        displayed_data[SCORE_COLOR_COLUMN],
                    ])
                )
            )
        ]
    )

    graph = dcc.Graph(figure=fig)

    html_div = html.Div(
        children=[
            banner(title="EKILIBR8", logo_url=app.get_asset_url("logo.jpeg"), link="https://ekinox.io", ),
            html.Div(id="body", className="container scalable", children=[
                graph
            ]),
        ],
    )

    return html_div


def _percentage_display(real_value: float) -> str:
    return str(round(real_value * 100)) + "%"


def _define_score_color(score: float) -> str:
    if score >= 0.75:
        return 'lightgreen'
    elif score >= 0.5:
        return 'rgba(255, 212, 116, 1)'
    else:
        return 'lightcoral'
