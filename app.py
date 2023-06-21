import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, dash_table, dcc, html

df = pd.read_excel("sales_data.xlsx")

sales_by_customer = (
    df.groupby("Customer")["Total Sales"].sum().sort_values(ascending=False)
)
profit_by_sales_rep = (
    df.groupby("SalesRep")["Profit"].sum().sort_values(ascending=False)
)
sales_by_sales_rep = (
    df.groupby("SalesRep")["Total Sales"].sum().sort_values(ascending=False)
)
sales_by_product = (
    df.groupby("ProductName")["Total Sales"].sum().sort_values(ascending=False)
)

sales_by_product_quantity = (
    df.groupby("ProductName")["Quantity"].sum().sort_values(ascending=False)
)
sales_by_time = df.groupby(df.OrderDate.dt.strftime("%Y-%m"))["Total Sales"].sum()

profit_by_customer = df.groupby("Customer")["Profit"].sum().sort_values(ascending=False)

profit_by_product = (
    df.groupby("ProductName")["Profit"].sum().sort_values(ascending=False)
)

profit_by_time = df.groupby(df.OrderDate.dt.strftime("%Y-%m"))["Profit"].sum()

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Kiwis", className="display-4"),
        html.Hr(),
        html.P("Business Dashboard", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Sales", href="/", active="exact"),
                dbc.NavLink("Profits", href="/profits", active="exact"),
                dbc.NavLink("All Data", href="/alldata", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

home_page = dbc.Container(
    [
        dbc.Row(
            [
                html.Div(
                    "Sales Analytics",
                    className="text-primary text-center fs-3",
                )
            ]
        ),
        dcc.Graph(
            figure=px.histogram(
                sales_by_customer,
                y="Total Sales",
                x=sales_by_customer.index,
                title="Sales by Customer",
                text_auto=True,
            ).update_layout(xaxis_title="Customer Name", yaxis_title="Total Sales")
        ),
        dcc.Graph(
            figure=px.histogram(
                sales_by_product,
                y="Total Sales",
                x=sales_by_product.index,
                title="Sales by Product",
                text_auto=True,
            ).update_layout(xaxis_title="Product Name", yaxis_title="Total Sales")
        ),
        dcc.Graph(
            figure=px.line(
                sales_by_time,
                y="Total Sales",
                x=sales_by_time.index,
                title="Sales by Time",
            ).update_layout(xaxis_title="Time", yaxis_title="Total Sales")
        ),
        dcc.Graph(
            figure=px.histogram(
                sales_by_sales_rep,
                y="Total Sales",
                x=sales_by_sales_rep.index,
                title="Sales by SalesRep",
                text_auto=True,
            ).update_layout(xaxis_title="SalesRep Name", yaxis_title="Total Sales")
        ),
        dcc.Graph(
            figure=px.histogram(
                sales_by_product_quantity,
                y="Quantity",
                x=sales_by_product_quantity.index,
                title="Quantities sold by product",
                text_auto=True,
            ).update_layout(xaxis_title="Product Name", yaxis_title="Quantity Sold")
        ),
    ]
)

profits = html.Div(
    children=[
        dbc.Row(
            [
                html.Div(
                    "Profit Analytics",
                    className="text-primary text-center fs-3",
                )
            ]
        ),
        dcc.Graph(
            figure=px.histogram(
                profit_by_customer,
                y="Profit",
                x=profit_by_customer.index,
                title="Profit by Customer",
                text_auto=True,
            ).update_layout(xaxis_title="Customer Name", yaxis_title="Profit")
        ),
        dcc.Graph(
            figure=px.histogram(
                profit_by_product,
                y="Profit",
                x=profit_by_product.index,
                title="Profit by Product",
                text_auto=True,
            ).update_layout(xaxis_title="Product Name", yaxis_title="Profit")
        ),
        dcc.Graph(
            figure=px.line(
                profit_by_time,
                y="Profit",
                x=profit_by_time.index,
                title="Profit by Time",
            ).update_layout(xaxis_title="Time", yaxis_title="Profit")
        ),
        dcc.Graph(
            figure=px.histogram(
                profit_by_sales_rep,
                y="Profit",
                x=profit_by_sales_rep.index,
                title="Profit by SalesRep",
                text_auto=True,
            ).update_layout(xaxis_title="SalesRep Name", yaxis_title="Profit")
        ),
    ]
)

all_data = html.Div(
    children=[
        dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
            filter_action="native",
            sort_action="native",
            style_table={"overflowX": "auto"},
            page_size=15,
        )
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home_page
    elif pathname == "/profits":
        return profits
    elif pathname == "/alldata":
        return all_data
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(debug=True)
