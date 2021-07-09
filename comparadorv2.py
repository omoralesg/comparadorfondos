import pandas as pd
import numpy as np
import dash_table
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Scheme, Symbol, Group
import plotly.express as px
import plotly.graph_objects as go
import sys
from dash.dependencies import Input, Output, ClientsideFunction


archivo_carteras = "Cartera Principal.xlsx"
archivo_aums = "Otros datos.xlsx"
catalogotv = "Catálogo TV.xlsx"
catalogoetfs = "Catalogo2.xlsx"
historico_aums = "AUM_Fondos.xlsx"
historico_carteras = "Carteras_historico.xlsx"
estrategias = "estrategias.xlsx"
clasif = "clasificaciones_inviertele.xlsx"


# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

df_cartera = pd.read_excel(archivo_carteras, sheet_name="Cartera")
df_aums = pd.read_excel(archivo_aums, sheet_name="Activos Netos")
df_generales = pd.read_excel(archivo_aums, sheet_name="Generales")
df_fees = pd.read_excel(archivo_aums, sheet_name="Suma de Cuotas")
df_catalogotv = pd.read_excel(catalogotv, sheet_name="Catálogo TV")
df_catalogoetfs = pd.read_excel(catalogoetfs, sheet_name="Catálogo")
# df_historico_aums= pd.read_excel(historico_aums, sheet_name="AUMS")
# df_historico_carteras= pd.read_excel(historico_carteras, sheet_name="Carteras")
df_estrategias = pd.read_excel(estrategias, sheet_name="estrategias")
df_clasif = pd.read_excel(clasif, sheet_name="clasif")


df_generales.drop("Operadora", axis=1, inplace=True)
df_generales.drop("Calificación  del  Mes  Actual", axis=1, inplace=True)

df_aumstot = df_aums.groupby(["Fondo"]).sum().reset_index()
# df_histaumstot = df_historico_aums.groupby(["Fondo", "Fecha"]).sum().reset_index()

df_estrategias = df_estrategias.drop_duplicates(subset=["Fondo"])


df_analisiscartera = df_cartera.merge(df_aumstot, on=["Fondo"])
df_analisiscartera = df_analisiscartera.merge(df_catalogotv, on=["Tipo de valor"])
df_analisiscartera = df_analisiscartera.merge(df_generales, on=["Fondo"])
df_analisiscartera["% Portafolio"] = (
    df_analisiscartera["Valor razonable o contable total"]
    / df_analisiscartera["ACTIVOS  NETOS  CIERRE  MES  ACTUAL"]
)
df_analisiscartera.drop(
    "Bursatilidad instrumento de renta variable", axis=1, inplace=True
)
df_analisiscartera.drop("Calificación de Instrumento de Deuda", axis=1, inplace=True)
df_analisiscartera.drop("ID Mercado", axis=1, inplace=True)
df_analisiscartera = df_analisiscartera.merge(df_clasif, on=["Fondo"])

a = df_analisiscartera.loc[
    df_analisiscartera["Emisora"].isin(df_catalogoetfs["Emisora"])
    & df_analisiscartera["Serie"].isin(df_catalogoetfs["Serie"])
]
a["Asset"] = a["Emisora"].map(df_catalogoetfs.set_index("Emisora")["Asset"])
a["Tipo de Mercado"] = a["Emisora"].map(
    df_catalogoetfs.set_index("Emisora")["Tipo de Mercado"]
)

df_analisiscartera.update(a)


del a


dff = df_analisiscartera.copy()
dff.drop("Tipo de inversión", axis=1, inplace=True)
dff.drop("Tipo de valor", axis=1, inplace=True)
dff.drop("Cantidad de títulos operados", axis=1, inplace=True)
dff.drop("Valor razonable o contable total", axis=1, inplace=True)
dff.drop("Días por vencer", axis=1, inplace=True)
dff.drop("Emisora", axis=1, inplace=True)
dff.drop("Serie", axis=1, inplace=True)
dff.drop("Tipo de Mercado", axis=1, inplace=True)
# dff.drop("Tipo  de  Fondo", axis=1, inplace=True)
dff.drop("% Portafolio", axis=1, inplace=True)
dff.drop("Asset", axis=1, inplace=True)
dff.drop("Descripción", axis=1, inplace=True)

dff = dff.groupby(["Fondo"]).max().reset_index()
dff["id"] = dff["Fondo"]
dff.set_index("id", inplace=True, drop=False)
dff = dff.reindex(
    columns=[
        "Operadora",
        "Fondo",
        "Tipo  de  Fondo",
        "Clasificación INVIERTELE",
        "ACTIVOS  NETOS  CIERRE  MES  ACTUAL",
        "id",
    ]
)
# print(dff.dtypes)


dffb = df_analisiscartera.copy()
dffb.drop("Tipo de inversión", axis=1, inplace=True)
dffb.drop("Tipo de valor", axis=1, inplace=True)
dffb.drop("Cantidad de títulos operados", axis=1, inplace=True)
dffb.drop("Valor razonable o contable total", axis=1, inplace=True)
dffb.drop("Días por vencer", axis=1, inplace=True)
dffb.drop("Tipo  de  Fondo", axis=1, inplace=True)
dffb.drop("Clasificación  del  Fondo", axis=1, inplace=True)
dffb.drop("ACTIVOS  NETOS  CIERRE  MES  ACTUAL", axis=1, inplace=True)
# dffb.to_excel("analisis_total.xlsx")

dffest = dff.copy()
dffest.drop("Tipo  de  Fondo", axis=1, inplace=True)



# def table_type(df_column):
#     # Note - this only works with Pandas >= 1.0.0

#     if sys.version_info < (3, 0):  # Pandas 1.0.0 does not support Python 2
#         return "any"

#     if isinstance(df_column.dtype, pd.DatetimeTZDtype):
#         return ("datetime",)
#     elif (
#         isinstance(df_column.dtype, pd.StringDtype)
#         or isinstance(df_column.dtype, pd.BooleanDtype)
#         or isinstance(df_column.dtype, pd.CategoricalDtype)
#         or isinstance(df_column.dtype, pd.PeriodDtype)
#     ):
#         return "text"
#     elif (
#         isinstance(df_column.dtype, pd.SparseDtype)
#         or isinstance(df_column.dtype, pd.IntervalDtype)
#         or isinstance(df_column.dtype, pd.Int8Dtype)
#         or isinstance(df_column.dtype, pd.Int16Dtype)
#         or isinstance(df_column.dtype, pd.Int32Dtype)
#         or isinstance(df_column.dtype, pd.Int64Dtype)
#     ):
#         return "numeric"
#     else:
#         return "any"


money = FormatTemplate.money(2)


options=[{"label": x, "value": x} for x in sorted(df_clasif["Clasificación INVIERTELE"].unique())],



def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H3("Comparador de Fondos de Inversión"),
            html.H6("Bienvenido al comparador de Fondos, una herramienta para evaluar alternativas de inversión"),
            html.Div(
                id="intro",
                children=" Primero podrás seleccionar el tipo de fondo del primer vehículo, después en la primer tabla podrás seleccionar el primer fondo, después puedes repetir el proceso para el segundo fondo en el seleccionador de abajo. Cada tabla la puedes filtrar por Operadora o por Fondo, una vez que haya seleccionado los fondos de click en el botón de comparar",
            ),
        ],
    )

def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Seleccione el tipo del Fondo 1 que quieres comparar"),
            dcc.Dropdown(
                id="c_dropdown",
                options=[{"label": x, "value": x} for x in sorted(df_clasif["Clasificación INVIERTELE"].unique())],
                multi=False,
                placeholder="Selecciona el tipo de fondo que deseas comparar",
            ),
            
            html.Br(),
            # html.Div(
            #     id="reset-btn-outer",
            #     children=html.Button(id="reset-btn", children="Comparar Fondos", n_clicks=0),
            # ),
        ],
    )

def generate_control_card2():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card2",
        children=[
            html.P("Seleccione el tipo del Fondo 2 que quieres comparar"),
            dcc.Dropdown(
                id="c_dropdown2",
                options=[{"label": x, "value": x} for x in sorted(df_clasif["Clasificación INVIERTELE"].unique())],
                multi=False,
                placeholder="Selecciona el tipo de fondo que deseas comparar",
            ),
            
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Comparar Fondos", n_clicks=0),
            ),
        ],
    )


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

app.title = "Comparador de Fondos"


app.layout = dbc.Container([
    
        
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([description_card()
                ])
            ]),
            dbc.Card([
                dbc.CardBody([generate_control_card(), generate_control_card2()
                ])
            ]),
            
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dash_table.DataTable(
                            id="tabla1",
                            columns=[
                                   {'id': 'Operadora', 'name': 'Operadora'},
                                   {'id': 'Fondo', 'name': 'Fondo'},
                                   {'id': 'ACTIVOS  NETOS  CIERRE  MES  ACTUAL', 'name': 'Activos Netos',"type" :'numeric',  "format": FormatTemplate.money(2) },
                                                               
                                
                                
                            ],
                            data=[],
                            filter_action="native",
                            style_cell={"textAlign": "left", "maxWidth": "250px"},
                            sort_action="native",
                            sort_mode="multi",
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            row_selectable="single",
                            selected_rows=[],
                            tooltip_header={
                                "Operadora": "Filtrar por Operadora",
                                "Fondo": "Filtrar por Fondo",
                            },
                            # style_data={  # overflow cells' content into multiple lines
                            #     'whiteSpace': 'normal',
                            #     'height': 'auto'
                            # },
                            tooltip_delay=0,
                            tooltip_duration=None,
                            #                                    style_table={
                            #     'maxHeight': '500px',
                            #     'overflowY': 'scroll'
                            # },
                            # style_as_list_view=True,
                            #  style_data_conditional=(
                            # data_bars(dff, 'ACTIVOS  NETOS  CIERRE  MES  ACTUAL')
                            #      ),
                            style_data_conditional=[
                                {
                                    "if": {
                                        "column_id": "ACTIVOS  NETOS  CIERRE  MES  ACTUAL",
                                    },
                                    "textAlign": "right",
                                    "type": "numeric",
                                    "format": FormatTemplate.money(2)
                                    # 'format' : FormatTemplate.money(2)
                                },
                                {
                                    "if": {
                                        "column_id": "ACTIVOS  NETOS  CIERRE  MES  ACTUAL",
                                    },
                                    "type": "numeric",
                                    "format": FormatTemplate.money(2),
                                },
                            ],
                        )
                    
                    
                    
                ])
            ]),
            
                        dbc.Card([
                dbc.CardBody([
                    dash_table.DataTable(
                            id="tabla2",
                            columns=[
                                   {'id': 'Operadora', 'name': 'Operadora'},
                                   {'id': 'Fondo', 'name': 'Fondo'},
                                   {'id': 'ACTIVOS  NETOS  CIERRE  MES  ACTUAL', 'name': 'Activos Netos',"type" :'numeric',  "format": FormatTemplate.money(2) },
                                                               
                                
                                
                            ],
                            data=[],
                            filter_action="native",
                            style_cell={"textAlign": "left", "maxWidth": "250px"},
                            sort_action="native",
                            sort_mode="multi",
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            row_selectable="single",
                            selected_rows=[],
                            tooltip_header={
                                "Operadora": "Filtrar por Operadora",
                                "Fondo": "Filtrar por Fondo",
                            },
                            # style_data={  # overflow cells' content into multiple lines
                            #     'whiteSpace': 'normal',
                            #     'height': 'auto'
                            # },
                            tooltip_delay=0,
                            tooltip_duration=None,
                            #                                    style_table={
                            #     'maxHeight': '500px',
                            #     'overflowY': 'scroll'
                            # },
                            # style_as_list_view=True,
                            #  style_data_conditional=(
                            # data_bars(dff, 'ACTIVOS  NETOS  CIERRE  MES  ACTUAL')
                            #      ),
                            style_data_conditional=[
                                {
                                    "if": {
                                        "column_id": "ACTIVOS  NETOS  CIERRE  MES  ACTUAL",
                                    },
                                    "textAlign": "right",
                                    "type": "numeric",
                                    "format": FormatTemplate.money(2)
                                    # 'format' : FormatTemplate.money(2)
                                },
                                {
                                    "if": {
                                        "column_id": "ACTIVOS  NETOS  CIERRE  MES  ACTUAL",
                                    },
                                    "type": "numeric",
                                    "format": FormatTemplate.money(2),
                                },
                            ],
                        )
                    
                    
                    
                    
                    
                ])
            ]),
            
            
        ], width=8),
       
    ],className='mb-2  mt-2' ),
    
    
      dbc.Row([
        dbc.Col([
             dbc.Card([
                 dbc.CardBody([
                     html.Br(),
                     html.Div("Estrategia Fondo 1"),
                     html.Div( id ="labelest1"),
                               html.Br(),
                               html.Br(),
                               html.Div("Estrategia Fondo 2"),
                               html.Div( id ="labelest2", children=[])
                 ])
             ]),
        ], width=4),
        dbc.Col([
            
                dbc.Card([
                dbc.CardBody([ 
                    dcc.Graph( id='graficacomp')
                ])
             ]),

        ], width=8),
        
                      
        
        
    ],className='mb-2  text-lg-center'),
    
    
    dbc.Row([
        dbc.Col([
            # dbc.Card([
            #     dbc.CardBody([generate_control_card()
            #     ])
            # ]),
        ], width=4),
        dbc.Col([
            
                dbc.Card([
                dbc.CardBody([
                    html.Div(id='labeltop10a'),
                ])
             ]),

        ], width=4),
        
               dbc.Col([
            
                dbc.Card([
                dbc.CardBody([
                    html.Div(id='labeltop10b', children=[]),
                ])
             ]),

        ], width=4),
        
        
        
    ],className='mb-2 font-weight-bold text-lg-center'),
    
    
    
    dbc.Row([
                dbc.Col([
            # dbc.Card([
            #     dbc.CardBody([generate_control_card()
            #     ])
            # ]),
        ], width=4),
         
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    
                    dash_table.DataTable(
                            id="tabla1a",
                            
                            columns=[
                                
                                {'id': 'Emisora', 'name': 'Activo'},
                                {'id': '% Portafolio', 'name': '% Portafolio',  "type" :'numeric' , "format": Format(precision=2, scheme=Scheme.percentage_rounded)},
                            ],
                            
                            # columns=[{"Tipode Mercado","Asset", "% Portafolio" }],
                            data=[],
                            
                            style_cell_conditional=[
        {
            'if': {'column_id': 'Emisora'},
            'textAlign': 'left'
        }
    ],
                            
                            
                            )
                    
                    
                    
                    
                ])
            ]),
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    
                     dash_table.DataTable(
                            id="tabla2a",
                            
                            columns=[
                                
                                {'id': 'Emisora', 'name': 'Activo'},
                                {'id': '% Portafolio', 'name': '% Portafolio',  "type" :'numeric' , "format": Format(precision=2, scheme=Scheme.percentage_rounded)},
                            ],
                            
                            # columns=[{"Tipode Mercado","Asset", "% Portafolio" }],
                            data=[],
                            
                            style_cell_conditional=[
        {
            'if': {'column_id': 'Emisora'},
            'textAlign': 'left'
        }
    ],
                            
                            
                            )
                    
                    
                    
                    
                ])
            ]),
        ], width=4),
        
    ],className='mb-2'),
], fluid=False)







@app.callback(
    dash.dependencies.Output("tabla1", "data"),
    [dash.dependencies.Input("c_dropdown", "value")],
    prevent_initial_call=True,
)
def tablafondos(val_chosen):

    dffestrat = dffest[dffest["Clasificación INVIERTELE"] == val_chosen]
    return dffestrat.to_dict("records")


@app.callback(
    dash.dependencies.Output("tabla2", "data"),
    [dash.dependencies.Input("c_dropdown2", "value")],
    prevent_initial_call=True,
)
def tablafondos(val_chosen):

    dffestrat2 = dffest[dffest["Clasificación INVIERTELE"] == val_chosen]
    return dffestrat2.to_dict("records")




@app.callback(
    [dash.dependencies.Output("tabla1a", "data"),
     dash.dependencies.Output("labeltop10a", "children"),
     dash.dependencies.Output(component_id='labelest1', component_property='children')],
    [dash.dependencies.Input(component_id='tabla1', component_property="derived_virtual_data"),
    dash.dependencies.Input(component_id='tabla1', component_property='derived_virtual_selected_rows'),
    dash.dependencies.Input(component_id='tabla1', component_property='derived_virtual_selected_row_ids')],
    prevent_initial_call=True,
    
    )

def tablatop10 ( all_data, slctd_row_indices,  slctd_rows) :
     
    
        dffcomp1 = dffb[dffb["Fondo"].isin(slctd_rows)]
        dffcomp1 = dffcomp1.groupby(["Emisora"]).sum().reset_index()
        dffcomp1 = dffcomp1.sort_values(["% Portafolio"], ascending=False).head(10)
        tablatop = dffcomp1.to_dict("records") 
        label    =  [" Top 10 instrumentos del fondo {}".format(slctd_rows)]
        dfflabel1 = df_estrategias[df_estrategias["Fondo"].isin(slctd_rows)]
        dfflabel1.to_dict("records")
        label1a = html.Div(dfflabel1["Estrategia"])
    
      
        return tablatop , label, label1a
    

    


    
@app.callback(
    [dash.dependencies.Output("tabla2a", "data"),
    dash.dependencies.Output("labeltop10b", "children"),
    dash.dependencies.Output(component_id='labelest2', component_property='children')],
    [dash.dependencies.Input(component_id='tabla2', component_property="derived_virtual_data"),
    dash.dependencies.Input(component_id='tabla2', component_property='derived_virtual_selected_rows'),
    dash.dependencies.Input(component_id='tabla2', component_property='derived_virtual_selected_row_ids')],
    prevent_initial_call=True,
    
    )

def tablatop10a ( all_data, slctd_row_indices,  slctd_rows) :
     
    
        dffcomp2 = dffb[dffb["Fondo"].isin(slctd_rows)]
        dffcomp2 = dffcomp2.groupby(["Emisora"]).sum().reset_index()
        dffcomp2 = dffcomp2.sort_values(["% Portafolio"], ascending=False).head(10)
        tablatopb = dffcomp2.to_dict("records") 
        label2    =  [" Top 10 instrumentos del fondo {}".format(slctd_rows)]
        dfflabel2 = df_estrategias[df_estrategias["Fondo"].isin(slctd_rows)] 
        dfflabel2.to_dict("records")
        label12a = html.Div(dfflabel2["Estrategia"])
      
        
        return tablatopb , label2,  label12a




@app.callback(
    dash.dependencies.Output("graficacomp", "figure"),     
    [dash.dependencies.Input(component_id='tabla1', component_property="derived_virtual_selected_row_ids"),
    dash.dependencies.Input(component_id='tabla2',  component_property='derived_virtual_selected_row_ids'),],
    prevent_initial_call=True,
    
    )

def graficacomp (fondo1, fondo2): 
    
    dffcomp1 = dffb[dffb["Fondo"].isin(fondo1)]
    dffcomp2 = dffb[dffb["Fondo"].isin(fondo2)]
    dffcomp3 = (dffcomp1, dffcomp2)
    dffcompg = pd.concat(dffcomp3)                
    dffcompg = dffcompg.groupby(["Fondo" ,"Asset"]).sum().reset_index()
    fig = px.bar(dffcompg, x="Fondo", y="% Portafolio" , color ="Asset" )
   
    
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-0.5,
    xanchor="right",
    x=1
))
    
    

       
       
    return fig





if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_hot_reload=True)