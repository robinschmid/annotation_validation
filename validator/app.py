from pathlib import Path
import uuid
import dash
import dash_uploader as du
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO
from dash import html, Output
from dash.dash_table import DataTable
from dash.html import Div
from utils import pandas_utils as pu
import annotation_validator

df = pu.read_dataframe("../example_data/casmi2022.tsv")
issues_df = annotation_validator.validate_submission(df)

dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ, dbc_css])  # colorful
theme_change = ThemeChangerAIO(aio_id="theme", radio_props={"value": dbc.themes.QUARTZ})

# configure upload
UPLOAD_FOLDER_ROOT = Path("../tmp") / "uploads"
du.configure_upload(
    app,
    str(UPLOAD_FOLDER_ROOT),
    use_upload_id=True,
)


def get_upload_component(id):
    return du.Upload(
        id=id,
        text='Drag and Drop csv or tsv file here to upload!',
        max_file_size=50,  # 50 Mb
        chunk_size=4,  # 4 MB
        filetypes=["csv", "tsv"],
        upload_id=uuid.uuid1(),  # Unique session id
    )


issues_table = Div(
    DataTable(
        id='issues_table',
        columns=[{"name": i, "id": i} for i in issues_df.columns],
        data=issues_df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
    ),
    id='issues_div',
    className="dbc-row-selectable",
)

data_table = Div(
    DataTable(
        id='data_table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.head(5).to_dict('records'),
        page_size=15,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
    ),
    id='data_div',
    className="dbc-row-selectable",
)

header_box_style = "bg-primary text-white p-1 mt-2 mb-0 text-center"

def get_app_layout():
    return dbc.Container(
        [
            theme_change,
            html.H4("Upload metadata", className=header_box_style),
            get_upload_component("upload_data"),
            html.Div(id='current_file', className='dbc'),
            html.H4("Issues with input metadata table", className=header_box_style),
            issues_table,
            # html.Br(),
            html.H4("Parsed input metadata", className=header_box_style),
            data_table,
            Div(id='upload_output')
        ],
        fluid=True,
        className="dbc",
    )


# get_app_layout is a function
# This way we can use unique session id's as upload_id's
app.layout = get_app_layout()


@du.callback(
    output=
    [
        Output("data_table", "metadata"),
        Output("issues_table", "metadata"),
        Output("current_file", "children"),
    ],
    id="upload_data",
)
def callback_on_completion(filenames):
    file = filenames[-1]
    df = pu.read_dataframe(file)
    issues_df = annotation_validator.validate_submission(df)

    cfile_html = html.P(f"Current file: {Path(file).name}")
    return df.to_dict('records'), issues_df.to_dict('records'), cfile_html


if __name__ == '__main__':
    app.run_server(debug=True)
