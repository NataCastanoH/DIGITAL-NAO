# %% [markdown]
# ![title](./images/logo_nao_digital.png)

# %% [markdown]
# # Tema 4. Conocimientos sobre librerías de visualización interactiva
# 
# ## 1. Objetivo
# 
# Con el objeto de ampliar el análisis de Oilst y más interactivo hacia el público al que va dirigido, el equipo de `Brasil BI Consulting` decidió crear visualizaciones interactiva, es decir que incluyen animaciones o filtros interactivos, a partir de los datos de las órdenes de los clientes y algunos datos geográficos.
# 
# Con ello en mente, el objetivo de la presente sección será trabajar con el módulo `Plotly Express` de la librería `Plotly` de Python (https://plotly.com/python/). Ésta es una librería para realizar gráficos interactivos en Python de amplio espectro.
# 
# ## 2. Librerias de trabajo

# %%
# Instala libreria si no la tenemos
!pip install matplotlib pandas plotly-express -y

# %%
import os
import json
import plotly.express as px
import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

# %% [markdown]
# ## 3. Lectura de datos
# 
# Primero nos encargaremos de leer los datos, indicando a Python donde se encuentra la carpeta que se aloja los datos y los nombres de los archivos relevantes para el análisis.

# %%
# Primero indicamos la ruta a la carpeta de de tu computadora
# donde se ubican los datos del E-commerce
# Ejemplo: "C:\Usuarios\[tu nombre]\Descargas"

DATA_PATH = "C:\\Users\\Natalia\\Recursos DN_COM_58"


# %% [markdown]
# Además de la data procesada, leeremos el archivo **brasil_geodata.json**, el cual es información geográfica de los estados de Brasil que será útil para nuestro análisis. Dicho archivo es una versión procesada del archivo `Brasil.json` de Kaggle (https://www.kaggle.com/code/kerneler/starter-brazil-states-geojson-ca176cdb-a).
# 
# Adicionalmente, para enriquecer el análisis añadirá al archivo `brasil_regions.csv` que contiene una clasificiación de los estados de Brasil en 4 regiones geográficas (`north`, `northeast`, `south` y `center-west`):

# %%
FILE_GEODATA = 'brasil_geodata.json'
FILE_CONSOLIDATED_DATA = 'oilst_processed.csv'
FILE_REGIONS = 'brasil_regions.csv'

# %%
# Cargar archivo datos geográficos de Brasil
with open(os.path.join(DATA_PATH, FILE_GEODATA), 'r') as f:
    geojson = json.load(f)


# %%
regions = pd.read_csv(
    os.path.join(DATA_PATH, FILE_REGIONS),
)

# %%
# cargamos datos de órdenes procesadas
columns_dates = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]

oilst = pd.read_csv(
    os.path.join(DATA_PATH, FILE_CONSOLIDATED_DATA),
    parse_dates=columns_dates
)


# %%
# Agregamos la columna de región para los estadios de Brasil
oilst = oilst.merge(regions[['abbreviation', 'region']], on='abbreviation', how='left')

# %%
oilst.info()


# %% [markdown]
# A su vez transformaremos el nombre de la ciudades a un formato de título, es decir, las primeras letras de las palabras estarán en mayúsculas.

# %%
oilst['geolocation_city'] = oilst['geolocation_city'].str.title()

# %% [markdown]
# También definiremos un dataframe que contiene únicamente a las órdenes que tienen estatus de entrega completada, es decir, que satisfacen con la condición de que la columna `order_status` es igual al valor `delivered`.

# %%
delivered = oilst.query("order_status == 'delivered'")

# %% [markdown]
# ### 4. Usando el API de Plotly
# 
# Plotly es una librería de visualización de datos (https://plotly.com/python/) que te permite crear gráficos interactivos y con una estética llamativa a través de una interfaz sencilla para el usuario, que se basa en la libreria `D3.js` de Javascript pero con una interfaces en Python, R y otro.
# 
# Básicamente, con Plotly puedes tomar datos y crear gráficos de barras, líneas, áreas, dispersión, histogramas, y también algunos en 3D. Lo que hace que Plotly sea especial es que puedes personalizar tus gráficos fácilmente y hacerlos interactivos, lo que significa que puedes hacer clic en los elementos del gráfico para obtener más información o incluso modificarlos en tiempo real.
# 
# Por ejemplo, si tienes un conjunto de datos de ventas de diferentes productos, puedes usar Plotly para crear un gráfico de barras que muestre las ventas de cada producto en un período determinado. Luego, si un usuario hace clic en una barra específica, Plotly puede mostrar información detallada sobre esa venta en particular.
# 
# Esta sección exploraremos particularmente el módulo de `Plotly Express`, aprovechando que la sintaxis es muy similar a la que se emplea en Seaborn, pues es compatible con dataframes de Pandas.
# 
# 
# ### 4.1 Análisis en el tiempo de la cantidad de órdenes de acuerdo a si se entregaron o no a tiempo.
# 
# Para comenzar, podemos explorar nuevamente la cantidad de ordenes en función de si llegaron en tiempo al domicilio del cliente.
# 
# En este caso, primero calcularemos los valores agregados de las ordenes por dicho estatus.

# %%
# Calcula la cantidad de ordenes en el tiempo
orders_time = delivered.groupby(['year_month']).\
    aggregate({'order_id':'count',}).\
        reset_index().\
            rename(columns={'order_id':'orders',})

# Crea una variable temporal en texto para graficar
orders_time['period'] =  orders_time['year_month'].astype(str)

# %% [markdown]
# Visualmente ello construye la siguiente tabla:

# %%
orders_time.tail()

# %% [markdown]
# Para realizar un gráfico de barras interactivo, basta usar la función `.bar` (https://plotly.com/python/bar-charts/), cuya sintaxis es análoga a la de Seaborn

# %%
# Crea la visualizacion
fig = px.bar(
    orders_time,
    x="period",
    y="orders",
    title='Fig.1 Número de órdenes de Oilst'
)

# Muestra la figura
fig.show()

# %% [markdown]
# Notas:
# 
#     * Si se pasa el mouse sobre la visualización, se verá que esta despliega la información interactiva de los valores de la grafica,
#     * Ademas permite hacer zoom, crear recortes, seleccionar regiones con un lazo, moverse y otras.

# %% [markdown]
# Similarmente a lo que se exploró en Seaborn, las visualizaciones se pueden segmentar usando otras variables. En este caso introduciremos un segmentación de acuerdo a si la orden se entregó o no en tiempo.

# %%
# Calcula la cantidad de ordenes en el tiempo
orders_time_delay_status = delivered.groupby(['year_month','delay_status']).\
    aggregate({'order_id':'count',}).\
        reset_index().\
            rename(columns={'order_id':'orders',})

# Crea una variable temporal en texto para graficar
orders_time_delay_status['period'] =  orders_time_delay_status['year_month'].astype(str)

# %% [markdown]
# Esto nos arroja la tabla:

# %%
orders_time_delay_status

# %% [markdown]
# Dicha información se puede analizar mejor a través del siguiente gráfico de barras:

# %%
# Crea la visualizacion
fig = px.bar(
    orders_time_delay_status,
    x="period",
    y="orders",
    color='delay_status',
    title='Fig.2 Número de órdenes de Oilst por tipo de entrega'
)

# Muestra la figura
fig.show()

# %% [markdown]
# Notas:
# 
#     * El gráfico anterior se puede filtra activando los colores del cuadro superior derecho para esconder o mostrar cada grupo. Prueba dando click en el cuadrado rojo con la etiqueta `on_time`
#     * También se pueden desagrupar las barras usando el parámetro ` barmode='group'`

# %% [markdown]
# **Preguntas:**
# 
# * ¿Cuándo sucede el periodo mas alto de retrazos prolongados?
# 
# En el periodo Q1 del 2018, exactamente en el mes de marzo
# 
# * ¿Existe alguna relación con el incremento de órdenes totales que el e-commerce empezó a recibir o no?
# 
# Si existe una realción pero no es muy fuerte, tampoco es lineal, solo a mayor número de pedidos, mayor probabbilidad de retrasos. Es un asunto que se puede explicar desde el punto de vista de estadìstica y probabilidad.

# %% [markdown]
# **Entregable:**
# 
# D. Programa que cree una visualización interactiva de un gráfico de barras que por cada mes y años, donde la altura de cada barra cuente la cantidad de órdenes con retraso prolongado que sucedieron en dicho periodo. Además, dentro cada barra se deberá tener un desglose de la cantidad de órdenes que tuvieron retraso en cada uno de los periodos. Éste script se llamará `3_d_evolution_delayed_orders_by_region.py` y la imagen interactiva deberá nombrase como `3_d_evolution_delayed_orders_by_region.html`.
# 
# **Hints:** 1) Primero realize conteo agrupados de las órdenes completadas mediante las variables `delay_status`,`year_month` y `geolocation_state`, 2) después explore la documentación de la utilidad `.bar` de Plotly para construir la visualización.

# %%
# Agrupar las órdenes con retraso prolongado
delayed_orders = delivered[delivered['delay_status'] == 'long_delay'].groupby(['year_month', 'geolocation_state']).size().reset_index(name='count')

# Visualización interactiva con Plotly
fig = px.bar(
    delayed_orders,
    x='year_month',
    y='count',
    color='geolocation_state',
    title='Órdenas con Retraso prolongado por cada mes, año y región',
    labels={'year_month': 'Mes y Año', 'count': 'Cantidad de Órdenes'},
    hover_name='geolocation_state'
)

# Personaliza la visualización
fig.update_layout(
    barmode='stack',  # Apila las barras
    xaxis_title='Mes y año',
    yaxis_title='Cantidad de órdenes',
    legend_title='Estado',
    showlegend=True,
    xaxis_tickangle=-45  # No cabían los nombres, entonces los giré un poquito
)

# Guarda la visualización en un archivo HTML
fig.write_html('3_d_evolution_delayed_orders_by_region.html')



