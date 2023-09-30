# %% [markdown]
# ![title](./images/logo_nao_digital.png)

# %% [markdown]
# # Tema 2. Conceptos de estadística y probabilidad usando Python
# 
# ## 1. Objetivo
# 
# Ahora que se ha integrado la data de Olist, el equipo de `Brasil BI Consulting` puede analizar de los retrazos las órdenes de los cliente, así el objetivo de esta sección será comenzar dicho análisis incorporando elementos de estadística y probabilidad usando Python.
# 
# ## 2. Librerías de trabajo

# %%
# Instala libreria si no la tenemos
!pip install pandas -y
!pip install openpyxl -y
!pip install matplotlib.pyplot -y
!pip install pillow

# %%
import os
import numpy as np
import pandas as pd
import openpyxl

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

# %% [markdown]
# ## 3. Lectura de datos
# 
#  Leeremos los datos, indicando a Python donde se encuentra la carpeta que se aloja los datos y los nombres de los archivos relevantes para el análisis.

# %%
# Primero indicamos la ruta a la carpeta de de tu computadora 
# donde se ubican los datos del E-commerce
# Ejemplo: "C:\Usuarios\[tu nombre]\Descargas"

DATA_PATH="C:\\Users\\Natalia\\Recursos DN_COM_58"

# %% [markdown]
# También usaremos el archivo consolidado de la lectura anterior:

# %%
FILE_CONSOLIDATED_DATA = 'oilst_processed.csv'

# %% [markdown]
# Recordemos que algunas de las columnas que contienen fechas deben ser convertidas al formato correspondiente, lo cual se puede llevar a cabo de forma automática usando el parámetro de `parse_dates`:

# %%
# Lista de columnas a interpretar como fecha
columns_dates=[
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
    ]

# Lectura del archivo csv
oilst = pd.read_csv(
    os.path.join(DATA_PATH, FILE_CONSOLIDATED_DATA),
    parse_dates=columns_dates
    )

# %% [markdown]
# ## 4. Análisis Exploratorio De Datos
# 
# ### 4.1 Generalidades sobre la tabla

# %% [markdown]
# Nuevamente podemos ver la información de la tabla con el comando `.info`

# %%
oilst.info()

# %% [markdown]
# Podemos revisar las columnas de nuestra tabla el comando `.columns`, que devuelve las columnas como un array:

# %%
oilst.columns

# %% [markdown]
# **Pregunta:**
# 
# * ¿Cuantas columnas tiene la tabla?
# 
# La tabla tiene 28 columnas
# 
# * ¿Cuánto espacio ocupa en memoria?
# 
# Ocupa 21.2+ MB

# %% [markdown]
# ### 4.2 Explorando columnas
# 
# #### 4.2.1 Una sola columna
# 
# Las columnas individuales de un dataframe de Pandas se pueden acceder de dos formas distintas: 1) usando el nombre la columna con corchetes después del nombre de dataframe, es decir `oilst['nombre_columna']` , 2) o bien, separando el nombre del dataframe y su columna por un punto `oilst.nombre_columna`. Como se puede ver a continuación:

# %%
oilst['total_sales']

# %%
oilst.total_sales

# %% [markdown]
# En ambos casos se pueden realizar operaciones con ellas como arreglos tradicionales de Python. Es decir con sumas, restas, multiplicaciones y divisiones. Por ejemplo,se puede expresar las ventas en miles:

# %%
# Ventas expresadas en miles
oilst['total_sales']/1000

# %% [markdown]
# Además se pueden aplicar operaciones sobre las columnas, con los operadores `.sum, .mean, .std, .min, .max` y muchos más. Por ejemplo, la siguiente operación calcula la cantidad total de ventas de Oislt millones:

# %%
oilst['total_sales'].sum()/1000000

# %% [markdown]
# Otro operador de interés es `.unique`, pues permite entender cuales son los valores únicos presentes en una columna. Con éste, podemos saber cuales son todos los estatus de las órdenes que el equipo de ingeniería de datos del e-commerce nos dió.

# %%
oilst['order_status'].unique()

# %% [markdown]
# A su vez, el operador `.value_counts()` nos permite contar cuantas veces aparecen estos valores en cada categoría presente en cada columna:

# %%
oilst['order_status'].value_counts()

# %% [markdown]
# **Preguntas***
# 
# * ¿Porqué deberíamos centrar el análisis de las órdenes con retraso en la categoría `delivered`?
# 
# Porque la idea es identificar patrones de comportamiento en las órdenes que están represadas y no han llegado a tiempo, además que son la mayor parte de la muestra.
# 
# * ¿Qué sucedería si incluyeramos órdenes con estatus distintos, por ejemplo, `processing` o `shipped`?
# 
# Estaríamos atribuyendo retrasos a las órdenes que de alguna manera ya fueron gestionadas o no han entrado en la línea de despachos.
# 
# * ¿Qué hace el operador `.value_counts(normalize=True)` sobre la columna `oilst['order_status']`?
# 
# Este operador se utiliza para contar y normalizar los valores únicos en una columna de un DataFrame en Pandas. En este contexto, estamos aplicando esta función a la columna olist['order_status'] para contar y normalizar los valores de estado de los pedidos en un conjunto de datos.

# %%
oilst['order_status'].value_counts(normalize=True)

# %% [markdown]
# #### 4.2.2 Varias columnas
# 
# En complemento, Pandas también permite seleccionar varias columnas a la vez para llevar a cabo el análisis multivariado.
# 
# Esencialmente, se pueden acceder de dos formas distintas: 1) usando una lista con los nombres de las columnas de nuestro interñes después del nombre de dataframe, es decir `oilst[['columna_1', 'columna_2', ..., 'columna_10']` , 2) o bien, usando el método `filter`, como sigue:

# %%
oilst[['total_sales','total_products']]

# %%
oilst.filter(['total_sales','total_products'])

# %% [markdown]
# En ambos casos, se pueden usar los operadores que hemos visto, por ejemplo para calcular el promedio de ventas y productos en las órdenes:

# %%
oilst[['total_sales','total_products']].mean()

# %% [markdown]
# **Pregunta:**
# 
# * ¿Cómo podemos interpretar el promedio de la variable `total_products`?,
# 
# Nos indica que la media promedio que lleva un cliente es 1 producto, equivalente a una suscripción.
# 
# * Lo anterior, ¿dice algo respecto a la cantidad de productos que suelen llevar los clientes en una compra?
# 
# Sí, esto es lo que se conoce como *Ticket promedio* por transacción realizada.
# 
# * ¿Qué se puede apreciar sobre la cantidad de productos  que la gente compra si aplicamos el método `.describe` a `oilst[['total_sales','total_products']]`?
# 
# Podemos observar que hasta el Q3(75% de la población de la muestra) las ventas son de 1 unidad por cliente.

# %%
#oilst[['total_sales','total_products']].describe()
oilst[['total_sales','total_products']].describe()

# %% [markdown]
# Cabe destacar que los operadores `.min` y `.max` también pueden trabajar con fechas, por ejemplo nos sirven para conocer los valores mínimo y máximo de las fechas de las órdenes:

# %%
print("Primera fecha: ", oilst['order_purchase_timestamp'].min())

# %%
print("Última fecha: ", oilst['order_purchase_timestamp'].max())

# %% [markdown]
# Estos también los podemos conocer con `.describe`

# %%
# Condicion  lógica para filtrar (solo ordenes entregadas)
delivered_filter = "order_status  == 'delivered' "

delivered = oilst.query(delivered_filter)

delivered['order_purchase_timestamp'].describe()

# %% [markdown]
# ## 4.3 Filtrando subconjuntos de datos
# 
# En ocasiones, es necesario estudiar sólo una parte de todos los datos proporcionados. Pandas permite realizar estos filtros en los datos en varias formas (https://www.geeksforgeeks.org/ways-to-filter-pandas-dataframe-by-column-values/), por ejemplo con valores de una columna, estructura lógicas para comparar fechas, entre otros.

# %% [markdown]
# En este análisis únicamente nos interesarán las órdenes completadas, así que tenemos que obtener el subconjunto de datos correspondiente. La utilidad de pandas que no servirá para dicho propósito es `.query()` (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html). En su interior debemos espeficar como texto una cadena lógica que indique que valor de una columna queremos obtener (`"order_status  == 'delivered' "`)

# %%
# Condicion  lógica para filtrar (solo ordenes entregadas)
delivered_filter = "order_status  == 'delivered' "

delivered = oilst.query(delivered_filter)

# %% [markdown]
# Ahora podemos ver una muestra de este nuevo subconjunto de datos:

# %%
delivered.sample(5)

# %% [markdown]
# La cantidad de renglones y columnas totales en este dataframe se puede obtener con el método `.shape`

# %%
delivered.shape

# %% [markdown]
# Este método es bastante amigable pues nos permite añadir muchas condiconales lógicas en el análisis en una misma expresión. Por ejemplo, si queremos el conjunto cantidad de ordenes que llegaron con retrazo prolongado y cuya venta represento más de 50 unidades monetarias esto se calcula como:

# %%
delivered.query("delay_status == 'long_delay'  & total_sales > 50").head()

# %% [markdown]
# **Preguntas:**
# 
# * ¿Cuantas órdenes completadas llegaron en tiempo (`delay_status` igual a `on_time`), con al menos 3 productos y con valor de ventas de más de 100 unidades monetarias?
# 
# 720 órdenes

# %%
# delivered.query("delay_status == 'on_time'  & total_sales > 100 & total_products > 3")
delivered.query("delay_status == 'on_time'  & total_sales > 100 & total_products > 3")

# %% [markdown]
# ## 4.4 Trabajando con variables categóricas
# 
# En estadística, una variable categórica es una variable que denota representa una categoría que califica a algo del mundo real, por ejemplo palabras o frases que describen una característica o cualidad específica, como el color de ojos (azul, verde, marrón) o la marca de automóvil (Toyota, Ford, Honda).
# 
# Pandas tiene métodos especiales para realizar cálculos de conteos y proporciones que cada categoría representa con respecto al total.

# %% [markdown]
# Por ejemplo, `.value_counts()` nos permite contar cuantos elementos de cada categoría existen en los tipos de entrega que se observaron respecto a la existencia de retrasos en las órdenes:

# %%
delivered['delay_status'].value_counts()

# %% [markdown]
# Además el parámetro `normalize=True` permite calcular lo anterior, como proporciones del total:

# %%
delivered['delay_status'].value_counts(normalize=True)

# %% [markdown]
# Aquí, se desprende que casi el 92% de las órdenes llegaron en tiempo, lo cual es un gran parámetro de la calidad de servicio del e-commerce Olist. Además, en el umbral de retrasos aceptables (hasta 3 días después de lo estimado) se encuentran el 2.76% de las órdenes.
# 
# Sin embargo, casi 5% de las órdenes tiene retrasos prolongados, es decir, los reportes de las redes sociales derivan de personas en este segmento específico.
# 
# **Preguntas**
# 
# * ¿Cómo podriamos comunicar lo anterior como un el área de oportunidad para Oilst?
# 
# Comunicar los resultados mencionados como un área de oportunidad para Olist podría implicar destacar la calidad del servicio en términos de entregas *on_time* y poner énfasis en la necesidad de abordar y mejorar el manejo de las órdenes con *long_delay*, más o menos así:
# 
# * Se comienza resaltando el éxito y la calidad del servicio que Olist ha logrado. Mencionando que aproximadamente el 92% de las órdenes se entregan puntualmente, lo que es un logro significativo en términos de satisfacción del cliente y eficiencia operativa.
# 
# * Luego, se identifica un desafío u oportunidad de mejora para alrededor del 5% de las órdenes experimentan que retrasos prolongados. Este segmento específico de órdenes representa una preocupación y puede ser la fuente de los informes negativos en las redes sociales.
# 
# * Adquirir un compromiso de mejoramiento para abordar este desafío y mejorar aún más la calidad del servicio. Esto puede incluir inversiones en logística especificamente en Sao Paulo, procesos de gestión de pedidos y atención al cliente. Esto podría incluir mejoras en la gestión de inventario, optimización de rutas de entrega y una comunicación más efectiva con los clientes en caso de retrasos.
# 
# * Incorporar a los clientes dentro del proceso, para que hagan participación activa con su retroalimentación con asuntos como calificar su experiencia y comunicar cualquier problema que puedan haber enfrentado. Este proceso debe complementarse con un acompañamiento por parte de Olist, que debe estar dispuesto para escuchar y responder antes las preocupaciones de los clientes.
# 
# * Hacer un seguimiento trasparente y comunicar los avances realizados en la mejora de los tiempos de entrega y la satisfacción del cliente. La comunicación efectiva sobre los desafíos y las áreas de oportunidad demuestra la transparencia y la voluntad de una empresa para abordar problemas y mejorar la experiencia del cliente. También puede ayudar a ganar la confianza de los clientes y a mantener una relación positiva con ellos.

# %% [markdown]
# ## 4.5 Trabajando con variables numéricas y categóricas
# 
# Cómo hemos visto antes, Pandas posee una serie de métodos (`.min, .max, .mean, .std, .median, .sum, .count`) para operar sobre variables numéricas. Estas se pueden combinar con agrupaciones sobre variables categóricas para observar como cambian las variables dentro de grupos específicos.
# 
# Para ello, Pandas ofrece al operador `.groupby()` que permite realizar operaciones agregadas en sobres los valores de una variable categóricas. A continuación, calcularemos el promedio de la diferencia de dias entre la entrega estimada y la fecha real de entrega, por cada los elementos de `delay_status`:

# %%
delivered.groupby(['delay_status'])['delta_days'].mean()


# %% [markdown]
# Aquí podemos apreciar que en el caso de órdenes a tiempo, estas llegan en promedio 13 días antes de lo proyectado. En el caso de las órdenes con retraso moderado, tales llegan posteriormente en 1 día después de la fecha estimada
# 
# **Pregunta**
# 
# * ¿Cómo se puede interpretar el promedio de `delta_days` para las órdenes con retrasos prolongados?
# 
# Un valor positivo de una unidad significa que, en promedio, las órdenes con retrasos prolongados llegan 13 días después de la fecha estimada de entrega. Existe retraso muy alto. 
# 
# * ¿Cuál es el área de oportunidad que tiene el e-commerce con respecto a dicho promedio?
# 
# Para lograrlo, el e-commerce podría considerar las siguientes acciones:
# 
# * Mejorar la Logística: Evaluar y optimizar los procesos logísticos, incluyendo la gestión de inventario, las rutas de entrega y la eficiencia operativa para reducir los retrasos.
# 
# * Comunicación Proactiva: Implementar una comunicación proactiva con los clientes en caso de retrasos, brindando información actualizada sobre el estado de sus órdenes y proporcionando expectativas realistas de entrega.
# 
# * Gestión de Inventarios: Asegurarse de mantener un inventario adecuado y prever los posibles problemas de abastecimiento que puedan llevar a retrasos en las entregas.
# 
# * Seguimiento y Análisis: Realizar un seguimiento constante de las órdenes con retrasos prolongados y analizar las causas subyacentes de los retrasos para abordarlos de manera efectiva.
# 
# * Capacitación del Personal: Brindar capacitación a los empleados involucrados en la gestión y entrega de órdenes para mejorar la eficiencia y la calidad del servicio.
# 
# El objetivo es reducir el promedio de delta_days para las órdenes con retrasos prolongados, lo que mejorará la experiencia del cliente y la percepción de la calidad del servicio.

# %% [markdown]
# De la misma forma, se pueden estimar los `.min, .max, .std`. Hagámoslo a continuación:

# %%
delivered.groupby(['delay_status'])['delta_days'].min()

# %%
delivered.groupby(['delay_status'])['delta_days'].max()


# %%
delivered.groupby(['delay_status'])['delta_days'].std()


# %% [markdown]
# Los estadísticos anteriores, también se pueden calcular usando la función `.describe` de Pandas, que calcula la cantidad de elementos de las columnas, su media y desviación estándar, juntos con los valores mínimo y máximo de la misma, así como valores inter-cuartiles Q1, Q2 y Q3.

# %%
delivered.groupby(['delay_status'])['delta_days'].describe()

# %% [markdown]
# **Impacto en ventas**

# %% [markdown]
# Usando lo anterior, también podemos estimar cual es el valor de las ventas en cada uno de los estatus de entrega de las órdenes.

# %% [markdown]
# Ellos se puede lograr realizando primero la agrupación por `delay_status` y posteriormente sumando los valores de `total_sales`:

# %%
delivered.groupby(['delay_status'])['total_sales'].sum()

# %% [markdown]
# Con las cantidades anterios podemos calcular que porcentaje de las ventas de Oilst representan lás ventas de las órdenes a través de sus estatus de entrega: 

# %%
delivered.groupby(['delay_status'])['total_sales'].sum()/ delivered['total_sales'].sum()*100

# %% [markdown]
# **Preguntas**
# 
# Si todas las personas con retrazos prolongados en sus entregas decidieran cancelar las entregas:
#   
#     * ¿cuál serían el impacto económico de la compañía en millones?
# 
# Se perderían 6 millones
# 
#     * ¿a qué porcentaje de sus ventas equivaldría dicho impacto?
# 
# Al 6% del valor de las ventas

# %% [markdown]
# **Pivot Tables en Pandas**
# 
# Para enriquecer en análisis, también se puede incorporar el impacto en ventas en el tiempo. Esto nos da oportunidad de introdución de la función `pivot_table` (https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html), que esencilmente permite calcular valores agregados en a lo larga de valores y columnas de una tabla.

# %% [markdown]
# En el siguiente ejemplo, calcularemos las ventas a lo largo de los estatus de entrega `delay_status` y los diferentes años de las órdenes:

# %%
delivered.pivot_table(
    # renglones
    index='delay_status',
    # columnas
    columns = 'year',
    # variable a calcula
    values= 'total_sales',
    # funcion para agrega la variable calculada
    aggfunc= 'sum',
    # agrega filas de totasl
    margins=True
    )


# %% [markdown]
# Esta tabla, también puede manipular con operaciones como hacemos con columnas de Pandas, por ejemplo, se puede expresar las sumas como millones al dividirlas ente 1000,000

# %%
delivered.pivot_table(
    # renglones
    index='delay_status',
    # columnas
    columns = 'year',
    # variable a calcula
    values= 'total_sales',
    # funcion para agrega la variable calculada
    aggfunc= 'sum',
    # agrega filas de totasl
    margins=True
    ).divide(1_000_000).round(4)

# %% [markdown]
# **Preguntas:**
# 
#     * ¿En que año hubo más ventas?
# 
# En el año 2018
# 
#     * ¿En que periodo las ventas con retrazos fueron más altas?
# 
#  En el Q1 de 2018

# %% [markdown]
# Este mismo tipo de análsis se puede llevar a cabo a lo largo de los diferentes trimestres:

# %% [markdown]
# Podemos analizar también la proporción de las ventas que provienen de retrasos prolongados lo largo de los diferentes trimestres. Primero construyamos la pivot tables de ventas segmentada por `delay_status` a lo largo de `quarter`

# %%
delivered.pivot_table(
    index='delay_status',
    columns = 'quarter',
    values= 'total_sales',
    aggfunc= 'sum',
    fill_value=0
    )

# %%
# Ahora generamos el archivo en formato .csv
prop_sales = delivered.pivot_table(
    index='delay_status',
    columns = 'quarter',
    values= 'total_sales',
    aggfunc= 'sum',
    fill_value=0
    )

# Guardar la tabla dinámica en un archivo CSV
prop_sales.to_csv('prop_sales_delay_status_by_quarte.csv')

# %% [markdown]
# A la tabla anterior, se le puede aplicar un función que calcule las proporciones dentro de ventas dentro de cada categoría:

# %%
# Aplica la función lambda x:   x / float(x.sum() sobre
# renglones (axis=0)

delivered.pivot_table(
    index='delay_status',
    columns = 'quarter',
    values= 'total_sales',
    aggfunc= 'sum',
    #margins=True,
    fill_value=0
    ).apply(lambda x:   x / float(x.sum()), axis=0).round(2)

# %% [markdown]
# **Problemas:**
# 
# + ¿Qué sucedió entre el último trimestre de 2017 y el primer trimestre de 2018?
# 
# En estos periodos fue donde más órdenes se entregaron con un retraso prolongado.
# 
# + ¿Existe alguna relación con el valor que representar las ventas con retrasos y los picos de ventas de la tienda?
# 
# Si existe relación porque vemos que son 2 del top 3 de meses en que más ventas se concretaron, aunque no es tan directo porque ninguno de esos periodos es el lìder en ventas de esta lista.
# 
# + De ser el caso, ¿qué es lo que esto implica para la escala de ventas y la operación de logística de la empresa?
# 
# A mayor número de ventas, mayor probabilidad de retraso, esto habla mucho de la logística de la empresa.

# %% [markdown]
# **Tablas de contingencia en Pandas**
# 
# De manera similar a las Pivot Tables, Pandas posee herramientas para realizar cruces entre variables de tipo categóricas, que se pueden comparar mediante conteos. Estas herramientas se pueden construir con la función `.crosstab` (https://pandas.pydata.org/docs/reference/api/pandas.crosstab.html)
# 
# En este caso, solo tenemos que pasar las columnas que se quieren comparar y Pandas realizará los conteos correspondientes:

# %%
pd.crosstab(
    oilst['delay_status'],
    oilst['year']
)

# %% [markdown]
# Ahora añadiremos la variable `normalize=True`:

# %%
pd.crosstab(
    oilst['delay_status'],
    oilst['year'],
    normalize=True
)

# %% [markdown]
# **Preguntas**
# 
# * ¿Qué no dice la tabla anterior acerca de la tendencia de casos con demoras prolongadas en entregas de órdenes? ¿Se ha incrementado a lo largo de los años o ha disminuido?
# 
# La tendecia nos muestra que a más años, más aumentan los retrasos.
# 
# * ¿Qué representa lo anterior para la empresa Oilst?
# 
# Un posible aumento en la demanda pero sin aumento o mejoras en la logística (gestiones de compras, ventas, inventarios, etc).

# %%
pd.crosstab(
     oilst['total_products'],
     oilst['delay_status'],
     margins = True
 ).sort_values(['long_delay']).tail(10)

# %%
# Ahora generamos el archivo en formato .csv
count_orders = pd.crosstab(
     oilst['total_products'],
     oilst['delay_status'],
     margins = True
 ).sort_values(['long_delay']).tail(10)

# Guardar la tabla dinámica en un archivo CSV
count_orders.to_csv('count_orders_basket_size_by_delay_status.csv')

# %% [markdown]
# ### 4.6 Elementos de análisis estadístico

# %% [markdown]
# En estadística, existe uno de los conceptos más útiltes para apreciar un fenómenos a través de muchas de sus observaciones es el de **histograma de frecuencias**, 
# 
# Esta herramienta gráfica que muestra cuantas veces ocurren las diferentes valores en un conjunto de datos. En otras palabras, representa cuántas veces aparece cada valor en el conjunto de datos, usando un diagrama de 
#  gráfica con barras que muestran la frecuencia con la que aparece cada uno de los valores que típicamente se agrupan en intervalos para facilitar el conteo (`bins`, en inglés).
# 
#  Un histograma puede ayudarnos a identificar patrones en la distribución de los datos, como si las notas están concentradas en un rango estrecho o si están más dispersas.
# 
# La curva que dibuja un histograma se puede dividir entre el número de casos totales y con ello aproximar la probabilidad de que un fenómeno determinado ocurra para un valor o un rango de valores de interés (por ejemplo, la probabilidad de que una orden llegue 3 o menos días respecto a la fecha de entrega). Estas curvas son conceptos matemáticos muy relevantes, pues sirven para crear modelos probabilísticos de los fenómenos.
# 

# %% [markdown]
# En Python, la librería Matplotlib permite construir el histograma de frecuencias de una manera sencilla con la función `.hist`:

# %%
# figura y eje de la figura
fig, ax = plt.subplots(figsize=(10, 5))

# numero de intervalos para conteos
n_bins = 100

# creacion del objeto historgama
n, bins, patches = ax.hist(
    delivered['delta_days'],
    n_bins
    )

ax.set_title('Fig.1 Histograma de frequencias de delta_days')
ax.set_xlabel('Diferencia entre el tiempo estimado y tiempo real de entrega')
ax.set_ylabel('# Ocurrencias')

# %% [markdown]
# La gráfica anterior muestra la cantidad de veces que se observaron diferencias de tiempo entre la estimación y la entrega real. Como se aprencia hay pico alrededor del valor -11, porque como sabemos las órdenes tienden a llega antes de tiempo
# 
# Además, dicha gráfica está **sesgada a la izquierda**, antes del valor cero, lo que significa que la mayoria de las órdenes llegan antes del tiempo estimado. Los valores extremos  a la derecha indican retrasos, que como se ve pueden superar hasta los 50 días.

# %% [markdown]
# En estadística, existe un concepto denominado `regla empírica débil` que nos permite relacionar a la distribución de los datos junto con la media y la desviación estándar. En esencia, nos permite asegurar que aproximadamente 88.88% de los datos, se encontrarán entre el intervalo definido por la media y tres veces la desviación estándar.
# 
# Esto se puede constatar empíricamente en nuestro histograma, añadiendo las regiones descritan previamente:

# %%
# figura y eje de la figura
fig, ax = plt.subplots(figsize=(10, 5))

# numero de intervalos para conteos
n_bins = 100

# creacion del objeto historgama
n, bins, patches = ax.hist(
    delivered['delta_days'],
    n_bins
    )

ax.set_title('Fig.2 Histograma de frequencias de delta_days y regla empírica débil' )
ax.set_xlabel('Diferencia entre el tiempo estimado y tiempo real de entrega')
ax.set_ylabel('# Ocurrencias')

## Agrega la media y las regiones de la regla empírica débil
## Linea para la media
plt.axvline(
    oilst['delta_days'].mean(),
    color='r',
    linestyle='dashed',
    linewidth=3)

## Linea para la media + 3 veces la desv. estandar
plt.axvline(
    oilst['delta_days'].mean() + 3*oilst['delta_days'].std(),
    color='y',
    linestyle='dashed',
    linewidth=2)

## Linea para la media - 3 veces la desv. estandar
plt.axvline(
    oilst['delta_days'].mean() - 3*oilst['delta_days'].std(),
    color='y',
    linestyle='dashed',
    linewidth=2)

## limites de la figura
min_ylim, max_ylim = plt.ylim()

## Etiquetas
plt.text(
    delivered['delta_days'].mean()*1.1,
    max_ylim*0.9,
    'Promedio: {:.2f}'.format(oilst['delta_days'].mean())
    )

plt.show()

# %%
# figura y eje de la figura
fig, ax = plt.subplots(figsize=(10, 5))

# numero de intervalos para conteos
n_bins = 100

# creacion del objeto historgama
n, bins, patches = ax.hist(
    delivered['delta_days'],
    n_bins
    )

ax.set_title('Fig.2 Histograma de frequencias de delta_days y regla empírica débil' )
ax.set_xlabel('Diferencia entre el tiempo estimado y tiempo real de entrega')
ax.set_ylabel('# Ocurrencias')

## Agrega la media y las regiones de la regla empírica débil
## Linea para la media
plt.axvline(
    oilst['delta_days'].mean(),
    color='r',
    linestyle='dashed',
    linewidth=3)

## Linea para la media + 3 veces la desv. estandar
plt.axvline(
    oilst['delta_days'].mean() + 3*oilst['delta_days'].std(),
    color='y',
    linestyle='dashed',
    linewidth=2)

## Linea para la media - 3 veces la desv. estandar
plt.axvline(
    oilst['delta_days'].mean() - 3*oilst['delta_days'].std(),
    color='y',
    linestyle='dashed',
    linewidth=2)

## limites de la figura
min_ylim, max_ylim = plt.ylim()

## Etiquetas
plt.text(
    delivered['delta_days'].mean()*1.1,
    max_ylim*0.9,
    'Promedio: {:.2f}'.format(oilst['delta_days'].mean())
    )

#Generar la imagen .png
plt.savefig('histogram_sales_long_delay.png')

# %%
print("La mayoria de los datos se ubican en el intervalo:")

print(
    "(media + 3 desv. std , media - 3 desv. std)= ",'(',
    round(oilst['delta_days'].mean() - 3*oilst['delta_days'].std(),1), ",",
    round(oilst['delta_days'].mean() + 3*oilst['delta_days'].std(),1),")",
    )

# %% [markdown]
# Una forma alternativa de visualizar lo anterior, es echar mano la **función de distribución acumulativa empírica**. 
# 
# Dicha herramienta es una manera de resumir datos y entender cómo se distribuyen los valores en un conjunto de datos, pues esencialmente, para una lista ordenada de números, nos permite entender cuántos de los valores son menores o iguales a un número específico y con ello entender de manera aproximada cuantos de los casos ocurren en la realidad y en que proporción, aproximando la probabilidad de un fenómeno.
# 
# Por ejemplo, si tenemos una lista de edades y queremos saber cuántas personas tienen 30 años o menos, 
# podemos usar la función empírica de distribución cumulativa. Si hay 50 personas en total y 20 tienen 30 años o menos, entonces la función nos dirá que el 40% de las personas tienen 30 años o menos. Podemos repetir esto para cada edad y obtener una imagen completa de cómo se distribuyen las edades en nuestro conjunto de datos.
# 
# En el caso de la variable `delta_days`, la **función de distribución acumulativa empírica** se puede visualizar mediante la función `ecdfplot`. En el **eje X** se tiene el valor de la variable en estudio y en el **eje Y** se encuentra la proporción de casos que corresponden a valores menores o iguales a los del **eje X** .

# %% [markdown]
# En Python, se puede construir la función **función de distribución acumulativa empírica** usando las utilidades de Matplotlib `.hist` (https://www.google.com/search?client=safari&rls=en&q=hist+matplotlib&ie=UTF-8&oe=UTF-8) junto con sus parámetros `cumulative=True`, `histtype='step'` y ` density=True`

# %%
fig, ax = plt.subplots(figsize=(15, 6))

n_bins = 300

# plot the cumulative histogram
n, bins, patches = ax.hist(
    oilst.query("year > 2017")['delta_days'],
    n_bins,
    density=True,
    histtype='step',
    cumulative=True,
    label='Empirical'
    )

# tidy up the figure
ax.grid(True)
ax.legend(loc='right')
ax.set_title('Fig. 3 Función de distribución acumulativa empírica')
ax.set_xlabel('Diferencia entre el tiempo estimado y tiempo real de entrega')
ax.set_ylabel('Proporción de ocurrencia')

plt.show()

# %% [markdown]
# En esta gráfica se puede apreciar que casi con más del 90% de probabilidad, las órdenes llegan en tiempo (comparando el valor cero en el eje X vs la proporción de ocurrencias en el eje Y).

# %% [markdown]
# Existe un concepto matemático llamada kernel gaussiano que permite aproximar dicha probabilidad y que en Python se calcula con la herramien `gaussian_kde` de la librería Scipy.
# 
# A continuación se aproximarán los valores que vemos en el diagrama de la función de distribución acumulativa empírica

# %%
# Aproxima los valores de la función de
#  distribución acumulativa empírica
import scipy.stats

# Nota: el metodo .dropna() elimina valores nulos
kde = scipy.stats.gaussian_kde(
    oilst['delta_days'].dropna() 
    )

# %% [markdown]
# Ahora estamos en condiciones de aproximar la probabilidad de recibir un pedido antes del tiempo estimado:

# %%
# Probabilidad de recibir entre un mes y hasta 
# en cero dias antes de lo estimado
print("Probabilidad: ",kde.integrate_box_1d(-30, 0)*100)

# %% [markdown]
# Del mismo modo, se puede calcular la probabilidad de recibir el pedio con retrazo moderado (entre cero dias de lo estimado y hasta en menos de 3):

# %%
# Probabilidad de recibir con un retraso moderado
print("Probabilidad: ",kde.integrate_box_1d(0, 3)*100)

# %%
# Probabilidad de recibir con un retraso de 3 a 7 días
print("Probabilidad: ",kde.integrate_box_1d(3, 7)*100)

# %%
# Probabilidad de recibir con un retraso de 3 a 15 días
print("Probabilidad: ",kde.integrate_box_1d(3, 15)*100)

# %%
# Probabilidad de recibir con un retraso grande
print("Probabilidad: ",kde.integrate_box_1d(4, 200)*100)

# %% [markdown]
# **Pregunta:**
# 
# * ¿Cuál es la probabilidad de recibir un pedido entre 3 y 7 dias después de lo estimado?
# 
# Aproximadamente del 2%
# 
# * ¿Cuál es la probabilidad de recibir un pedido entre 3 y 15 dias después de lo estimado?
# 
# Aproximadamente del 4%
# 
# * ¿Cuál es la probabilidad de recibir un pedido después de 3 dias después de lo estimado? Hint: se puede usar una fecha muy larga como limite superior derecho, por ejemplo 200 días
# 
# Aproximadamente del 5%

# %% [markdown]
# ### 4.7 Análsis de correlación lineal
# 
# La correlación lineal es una herramienta que se utiliza para analizar la relación lineal entre varias variables. En esencia, lo que hace es medir cuánto se parecen dos variables y cuánto se influyen mutuamente.
# 
# Formalmente, se denomina **Coeficiente de correlación de Pearson** y se calcula como un coeficiente entre dos variables numéricas, que oscila entre entre -1 y 1, donde -1 significa que las dos variables están completamente inversamente relacionadas (si una aumenta, la otra disminuye) y 1 significa que las dos variables están completamente relacionadas (si una aumenta, la otra también lo hace). En el caso cercano a cero, esto significa que no hay correlacion de tipo lineal entre estas
# 
# Si queremos detectar que una variable tiene correlación lineal con otra, su coeficiente de correlación debe aproximarse lo más posible a -1 o 1. 
# 
# Debemos mencionar que la existencia de correlación lineal entre dos variables no implica que una cause a la otra; por ejemplo, la cantidad de helados que se venden en verano aumenta a la vez que la cantidad de quemaduras en la piel en la misma época, sin que alguna de ellas sea la causa de la otra. Sin embargo la correlación alta es un elemento deseable en cualquier análisis exploratorio para comenzar a indagar como es que un fenómeno cambia ante diversos factores. 
# 
# 

# %% [markdown]
# Ahora veremos como cambia la distancia de los domicilios de los clientes a su centro de distribución más cercano (`distance_distribution_center`) con respecto al estatus del tiempo de entrega. Primero, podemos revisar los estadísticos básicos:

# %%
delivered.groupby(['delay_status'])['distance_distribution_center'].describe()

# %% [markdown]
# Ahora usaremos el métod `.corr` de pandas sobre las variables numéricas `total_sales`, `total_products`, `distance_distribution_center`y `delta_days`.

# %%
delivered[
    ['total_sales', 'total_products', 'distance_distribution_center', 'delta_days']
    ].corr().round(4)

# %% [markdown]
# En esta tabla no se aprecia correlación entre las variables. Repitamos los cálculos pero en el caso de que ordenes entregas, que presentaron retrasos prolongados. 

# %%
# Completa el codigo provisto
filter = delivered['delay_status'] == 'long_delay' # filtro para definir ordenes con retraso prolongado

# lista de variables numericas de ventas, productos, retrasos y distancia al centro de distribucion
numerical_variables = ['total_sales', 'total_products', 'delta_days', 'distance_distribution_center']

# calculo de matriz de correlacion
delivered[filter][numerical_variables].corr().round(4)


# %% [markdown]
# **Preguntas**
# 
# * ¿Existe correlación fuerte entre alguna de las variables? De ser el caso, ¿entre cuales?
# 
#   Después de aplicar el coeficiente de relación de Pearson, observamos lo siguiente:
#   - No hay una fuerte correlación lineal entre el total de ventas y el total de productos.
#   - Existe una correlación débil y negativa entre el total de productos y la cantidad de días de  retraso.
#   - Hay una correlación moderadamente fuerte y positiva entre la cantidad de días de retraso y la   distancia al centro de distribución.
#   - No hay una fuerte correlación lineal entre el total de ventas y la distancia al centro de  distribución.
# 
# 
# * ¿Qué es lo que implica lo anterior para el problema de los retrasos prolongados en las entregas a los clientes de Oilst?
# 
# 
#   Las observaciones derivadas de la matriz de correlación entre las variables pueden proporcionar algunas pistas importantes sobre el problema de los retrasos prolongados en las entregas a los clientes, con la intención de no minimizar ningún hallazgo, vamos a analizar nuevamente cada una de las relaciones que involucran retrasos:
# 
#   - Correlación débil entre total de ventas y retrasos prolongados, esto indica que la magnitud de las ventas no es un factor crítico para predecir los retrasos prolongados.
#   - Correlación moderada entre días de retraso y distancia al centro de distribución, que sugiere que la distancia geográfica podría estar relacionada con los retrasos prolongados. Esto podría implicar que las entregas a ubicaciones más lejanas desde el centro de distribución tienen una mayor probabilidad de experimentar retrasos prolongados.
#   - Correlación débil entre total de ventas y distancia al centro de distribución, indica que el volumen de ventas no está directamente relacionado con la distancia geográfica al centro de distribución. Esto podría sugerir que la empresa atiende a una amplia gama de ubicaciones, independientemente del volumen de ventas.
# 
#   En resumen y en función de los anteriores hallzgos, se pueden considerar algunas implicaciones  para abordar el problema de los retrasos prolongados en las entregas a los clientes:
# 
# 
#   1. Enfoque en la gestión de distancias: Viendo que la distancia al centro de distribución parece estar relacionada con los retrasos prolongados, se deben considerar estrategias para optimizar la logística y reducir los tiempos de entrega en ubicaciones más alejadas.
# 
#   2. Análisis de la logística de Olist: Estos resultados sugieren que hay otros factores en juego que podrían estar contribuyendo a los retrasos prolongados. Es importante hacer análisis adicionales para identificar y abordar estos factores, como la eficiencia en la gestión de pedidos, la calidad del servicio de transporte o la capacidad de gestión de inventario.
# 
#   3. Segmentación de clientes: dependiendo de los resultados de análisis adicionales, se podría considerar segmentar a los clientes según la ubicación geográfica y aplicar estrategias de entrega específicas para las ubicaciones que experimentan retrasos prolongados.
# 
#   En general, aunque los resultados no son concretos, si sirven para dirigir esfuerzos de mejora de manera más precisa y a tomar decisiones informadas para abordar el problema de los retrasos prolongados en las entregas a los clientes.
# 

# %% [markdown]
# ## 5. Entregables
# 
# En esta sección los entregables consisten en un script en Python junto con un tabla/imagen en un archivo en formato específico:
# 
# A. Script que calcule la proporción que han representado las ventas de órdenes completas de Oilst dentro de los categorías de `delay_status` y a los largo de los trimestres de 2016 a 2018. El resultado de este script deberá ser un tabla denominada `prop_sales_delay_status_by_quarte.csv`.
# 
# B. Programa que construya una tabla con la cantidad conteos cuantas órdenes que existieron por cantidad de productos dentro de la orden y el tipo de retraso de las categorías `delay_status`. El resultado de este script deberá ser un tabla denominada `count_orders_basket_size_by_delay_status.csv`.
# 
# C. Programa que construya el histograma de frecuencias de la variable `total_sales`, junto con la el promedio intervalos que define la regla empírica débil para encontrar el 88.88% de los datos alrededor del promedio, restringiendo el análisis las órdenes que tienen status completo. El resultado de este script deberá ser una figura denominada `histogram_sales_long_delay.png`.
# 
# D. Script que calcula la matriz de correlación entre las variables `total_sales`, `total_products`, `delta_days` y `distance_distribution_center` para órdenes completadas que cuya fecha de entrega sobrepasa los 10 días de la fecha estimada para la entrega.

# %% [markdown]
# Para calcular la matriz de correlación cuando 'long_delay' sea mayor a 10, aplicamos un filtro adicional a las filas que cumplan con esa condición antes de calcular la matriz de correlación:

# %%
# Aplica el filtro para las órdenes con 'long_delay' mayor a 10
filter = (delivered['delay_status'] == 'long_delay') & (delivered['delta_days'] > 10)

# Lista de variables numéricas de interés
numerical_variables = ['total_sales', 'total_products', 'delta_days', 'distance_distribution_center']

# Calcula la matriz de correlación
delivered[filter][numerical_variables].corr().round(4)


