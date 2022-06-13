import dash_html_components as html


def banner(title: str, logo_url: str, link):
    return html.Div(
        className="banner",
        children=[
            html.Div(
                className="container scalable",
                children=[
                    html.H2(
                        title, style={"text-decoration": "none", "color": "inherit"}
                    ),
                    html.A(html.Img(src=logo_url), href=link),
                ],
            ),
        ],
    )
