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

# %% [markdown]
# ### 4.2 Análisis en el tiempo de las ventas de acuerdo a si se entregaron o no a tiempo.
# 
# Otra vertiente de análisis, es por supuesta la cantidad de ventas en función de si las órdenes llegaron en tiempo al domicilio del cliente.
# 
# Nuevamente calcularemos los valores agregados de las órdenes por dicho estatus.

# %%
sales_time = delivered.groupby(['quarter', 'delay_status'])['total_sales'].sum().reset_index()

sales_time['quarter'] = sales_time['quarter'].astype('str')

# %% [markdown]
# En este caso, aprovecharemos para introdución las gráficas de áreas de Plotly, que esencialmente se trata de series de tiempo con sobreados que permite entender la magnitun de una cantidad en el tiempo como el área bajo un curva.

# %%
fig = px.area(
    sales_time,
    x="quarter",
    y="total_sales",
    color="delay_status",
    title='Fig.3 Total de ventas de órdenes de Oilst por tipo de entrega'
    )
fig.show()

# %% [markdown]
# Del gráfico es claro que desde el ultimo trimestre de 2017 y hasta el segundo trimestre de 2018, la compañia enfrentó un crecimiento formidable en ventas, lo que podría indicar un sobre esfuerzo de los procedimientos logísticos al tener que lidiar con más pedidos de lo normal.
# 
# **Pregunta:**
# 
# * ¿Existe alguna relación entre este hecho y los retrasos reportados en las entregas?
# 
# Solo un aumento de probabilidad de entregar los pedidos con retraso mientras el volumen de pedidos aumenta.

# %% [markdown]
# Ahora bien, aunque la gráfica anterior es bastante ilustrativa, para transmitir la magnitud ecónomica que representaría que todas las órdenes con retrazo cancelaran, que es el peor de los escenarios posibles, se necesita un gráfico similar pero que muestre los valores en ventas como proporciones, pues tales cantidades son más sencillas de entender.
# 
# Ahora se consolidará un gráfica de ese estilo:
#     * Primero se cacularan los valores de ventas de acuerdo al estatus de llegada del pedido,
#     * Luego se calcularan como proporciones dentro de cada trimestre, usando la normalización de la función `crosstab` de Pandas,
#     * Después se podrán los datos en un formato alargado (https://pandas.pydata.org/docs/reference/api/pandas.melt.html), basicamente para poder graficar de forma más sencilla
#     * Y finalmente se usará el api de área de Plotly

# %%
# Ventas agregadas por tipo de entrega
sales_time_delay_status = delivered.groupby(['quarter', 'delay_status'])['total_sales'].sum().reset_index()

# Agrupación de ventas por tipo de entrega normalizando para 
# el calculo de proporciones
sales_time_delay_status_tab = pd.crosstab(
    index=sales_time_delay_status['quarter'],
    columns=sales_time_delay_status['delay_status'],
    values=sales_time_delay_status['total_sales'],
    aggfunc='sum',
    normalize='index'
    )

# Se manipula la data de forma alargada
sales_time_delay_status_tab_formated = pd.melt(
    sales_time_delay_status_tab.reset_index(),
    id_vars='quarter',
    value_vars=['long_delay', 'on_time', 'short_delay']
    )

# Multiplicamos por 100 la proporcion y definimos columna en texto para plotear
sales_time_delay_status_tab_formated['value'] = sales_time_delay_status_tab_formated['value']*100.0
sales_time_delay_status_tab_formated['quarter'] = sales_time_delay_status_tab_formated['quarter'].astype('str')

# %%

fig = px.area(
    sales_time_delay_status_tab_formated,
    x="quarter",
    y="value",
    color="delay_status",
    title="Fig. 4 Proporción de ventas de Oilst que representan las órdenes por tipo de entrega"
    )
fig.show()

# %% [markdown]
# **Preguntas**
# 
# * Fuera de los primeros meses del e-commerce, ¿Cuándo exisitió una mayor proporción de ventas con retraso?
# 
# Dentro del Q3 del año 2017 hasta el Q2 de 2018
# 
# * ¿Cómo puede explicarse en relación con las etapas de crecimiento en ventas totales de la empresa?
# 
# Puede explicarse con el aumento de la probabilidad, y el aumento del volumen de trabajo, si no había refuerzos en el departamento de logística, las cosas podían salirse de control.

# %% [markdown]
# ### 5. Análisis regionales

# %% [markdown]
# ### 5.1 Análisis regional sobre los retrasos en órdenes
# 
# Hasta ahora no se ha explorar la relación que existe entre la ubicación geográfica de los clientes con los retrasos en entrega. 
# 
# Abordaremos la relación entre ambos puntos usando visualizaciones interactivas. Para ellos se debe mencionar que se ha incorporado a los datos un clasificación de los estados de Brasil en regiones, descritar por la tabla siguiente:

# %%
oilst.columns.to_list()

# %%
oilst[
    ['region', 'abbreviation','state_name']
    ].drop_duplicates().sort_values(['region','abbreviation'],).dropna()

# %% [markdown]
# Para aquellas ordenes con retrazos prolongados, las distribuciones tiempos de retrazo por región pueden visualar con diagramas de caja:

# %%
fig = px.box(delivered.query("delay_status == 'long_delay'"),
    x="region",
    y="delta_days",
    title="Fig. 5 Distribución de los tiempos de entrega de órdenes con retrazo, por región"
)

fig.show()


# %%
fig = px.violin(delivered.query(
    "delay_status == 'long_delay'"
),
    x="region",
    y="delta_days",
    color="region",
    box=True, points="all",
    title="Fig. 6 Gráfico de violín de los tiempos de entrega de órdenes con retrazo, por región"
)

fig.show()

# %% [markdown]
# De lo anterior, se desprende que la región noreste tiene muchos valores atípicos en los tiempos de entrega. Esta es una hipótesis interesante de análisis.
# 
# Para complementarla, se puede segmentar aun más la visualización a nivel estado:

# %%
fig = px.box(delivered.query(
    "delay_status == 'long_delay'"
),
    x="state_name",
    y="delta_days",
    color="region",
    title="Fig. 7 Distribución de los tiempos de entrega de órdenes con retrazo, por estado y región"
)

fig.show()

# %% [markdown]
# En los diagramas de caja anterior, se aprecia que los estados de Sao Paolo y Rio de Janeiro son los que tienen valores más llamativas de tiempos de entrega altos en esa región. Sin embargo, al desagregar los resultados también notramos que hay anomalís en estados como el Amazonas y Roraima.

# %% [markdown]
# ### 5. 2 Visualizaciones Geográficas

# %% [markdown]
# Uno de lo puntos más interesantes de Ploty es la posibilidad de realizar gráficos completos usando data de otros sistemas, como los de origen geográfico.
# 
# En esta sección se mostrarán visualizaciones de los tiempos promedios por entrega en cada estado. Para ello se estimará el valor medio de los retrazos.

# %%
# Calcula el valor promedio de retrazos en el estado

delay_by_state = delivered.query(
    "delay_status == 'long_delay'"
).groupby(['state_name', 'geolocation_state'])['delta_days'].mean().reset_index()


# %% [markdown]
# Estos derivan en la tabla siguiente, donde se aprecia que Amapá, el Amazona y Roraima tienen los valores más altos:

# %%
delay_by_state.sort_values(['delta_days'], ascending=False)


# %% [markdown]
# Esta información se puede pasar a la función `.choropleth` de Plotly para construir un mapa. Cabe destaca que el archivo `geojson` es un archivo externo que contiene información de un sistema cartográfico que `Ploty` puede leer e interpretar para cronstruir la visualización:

# %%
# Crear figura con el mapa de Brasil y el choropleth
fig = px.choropleth(
    data_frame=delay_by_state,
    geojson=geojson,
    featureidkey='properties.UF',
    # featureidkey='properties.ESTADO',
    locations='geolocation_state',
    color='delta_days',
    # https://plotly.com/python/builtin-colorscales/
    color_continuous_scale="bluyl",
    scope='south america',
    labels={'delta_days': 'Retraso (en días)'},
    width=800,
    height=400,
    title="Fig 8. Mapa del tiempo retraso promedio a nivel estatal"
)

# Actualizar diseño de la figura
fig.update_geos(
    showcountries=False,
    showcoastlines=True,
    showland=True,
    fitbounds='locations',
    visible=True
)

fig.update_layout(
    margin=dict(l=20, r=20, t=66, b=20),
    width=800,
    height=800,
)

# Mostrar figura
fig.show()


# %% [markdown]
# **Pregunta:**
# 
# * ¿Existe algun patrón en los estados donde se reportaron mayores retrazos?
# 
# Los retrasos aumentaron hacia los estados del norte del país: especialmente Amapá, Amazonas y Roraima.
# 
# * ¿La operación de Oilst debería tomar alguna medida a raíz de lo anterior en su opeación para alcanzar destinos en los estados más notorios del mapa?
# 
# Debería ubicar un centro de distribución en el norte del país, en una ubicación cercana a estas regiones. Es importante estudiar costos de la inversión y compararla con un aumento de la logística en algún centro de distribución existente.

# %%
# Agrupar los datos necesarios en delay_by_state 
# Calcular la cantidad de pedidos retrasados

sum_long_delays_by_state = delivered.query(
    "delay_status == 'long_delay'"
    ).groupby(['state_name', 'geolocation_state'])['delay_status'].count().reset_index()


# %%
sum_long_delays_by_state.sort_values(['delay_status'], ascending=False)

# %%
# Crear figura con el mapa de Brasil y el choropleth
fig = px.choropleth(
    data_frame=sum_long_delays_by_state,
    geojson=geojson,
    featureidkey='properties.UF',
    # featureidkey='properties.ESTADO',
    locations='geolocation_state',
    color='delay_status',
    # https://plotly.com/python/builtin-colorscales/
    color_continuous_scale="bluyl",
    scope='south america',
    labels={'delay_status': 'Cantidad de pedidos retrasados'},
    width=800,
    height=400,
    title="Mapa de la cantidad de órdenes con entregas de restraso prolongado a nivel estatal"
)

# Actualizar diseño de la figura
fig.update_geos(
    showcountries=False,
    showcoastlines=True,
    showland=True,
    fitbounds='locations',
    visible=True
)

fig.update_layout(
    margin=dict(l=20, r=20, t=66, b=20),
    width=800,
    height=800,
)

# Mostrar figura
#fig.show()

# Guardar la figura interactiva como un archivo HTML
fig.write_html('3_e_map_long_delays_by_state.html')

# Mostrar figura
fig.show()

# %% [markdown]
# ## 5. Entregables
# 
# Los entregables de ésta sección consisten en un script en Python junto con un imagen interactiva en formato `.html` (https://plotly.com/python/interactive-html-export/) en un archivo en formato específico:
# 
# D. Programa que cree una visualización interactiva de un gráfico de barras que por cada mes y años, donde la altura de cada barra cuente la cantidad de órdenes con retraso prolongado que sucedieron en dicho periodo. Además, dentro cada barra se deberá tener un desglose de la cantidad de órdenes que tuvieron retraso en cada uno de los periodos. Éste script se llamará `3_d_evolution_delayed_orders_by_region.py` y la imagen interactiva deberá nombrase como `3_d_evolution_delayed_orders_by_region.html`.
# 
# **Hints:** 1) Primero realize conteo agrupados de las órdenes completadas mediante las variables `delay_status`,`year_month` y `geolocation_state`, 2) después explore la documentación de la utilidad `.bar` de Plotly para construir la visualización.
# 
# E. Script que construya un mapa interactivo que indique con una escala de colores a la cantidad de casos de órdenes con retrazos prolongados que ocurrieron en cada estado. Dicho script se llamará `3_e_map_long_delays_by_state.py` y la imagen interactiva deberá tener el nombre `3_e_map_long_delays_by_state.html`.


