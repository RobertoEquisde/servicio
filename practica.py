import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import streamlit as st

# Función para leer el archivo CSV
def leer_csv(archivo):
    df = pd.read_csv(archivo, parse_dates=['Fecha'])
    df.columns = df.columns.str.strip()  # Eliminar espacios en los nombres de las columnas
    return df

# Función para resamplear los datos según el intervalo seleccionado
def resamplear_datos(df, intervalo):
    df_resampleado = df.resample(f'{intervalo}T', on='Fecha').mean().dropna()
    df_resampleado = df_resampleado.reset_index()  # Asegurar que 'Fecha' sea una columna
    return df_resampleado

# Función lineal para ajustar el patrón
def lineal(x, m, b):
    return m * x + b

# Función para verificar y ajustar un patrón lineal a los datos
def ajustar_y_comparar(df, tolerancia):
    x_datos = np.arange(len(df))
    y_datos = df['Valor'].values

    # Ajustar a un patrón lineal y obtener parámetros
    params, _ = curve_fit(lineal, x_datos, y_datos)
    m, b = params
    st.write(f"Función ajustada: y = {m:.2f}x + {b:.2f}")

    # Comparar con patrones predefinidos
    patrones = {
        'Patron 1': (0.16, 87.05),
        'Patron 2': (-0.26, 104.06),
        'Patron 3': (-0.10, 95.74)
    }
    distancias = {}
    for nombre, (pm, pb) in patrones.items():
        distancia = np.sqrt((pm - m) ** 2 + (pb - b) ** 2)
        distancias[nombre] = distancia

    patrón_cercano = min(distancias, key=distancias.get)
    
    # Comprobar si la distancia está dentro del margen de tolerancia
    if distancias[patrón_cercano] <= tolerancia:
        return patrón_cercano, distancias[patrón_cercano], m, b, True
    else:
        return patrón_cercano, distancias[patrón_cercano], m, b, False

# Función para graficar los datos y el ajuste
def graficar_datos(df_original, df_resampleado, m, b):
    fig, ax = plt.subplots(2, 1, figsize=(10, 10))

    # Graficar los datos originales
    ax[0].plot(df_original['Fecha'], df_original['Valor'], color='blue', marker='o')
    ax[0].set_title('Datos Originales')
    ax[0].set_xlabel('Fecha')
    ax[0].set_ylabel('Valor')
    ax[0].grid(True)

    # Graficar los datos resampleados y el ajuste lineal
    x_resampleado = np.arange(len(df_resampleado))
    y_ajustado = lineal(x_resampleado, m, b)
    ax[1].plot(df_resampleado['Fecha'], df_resampleado['Valor'], color='blue', marker='o', label='Resampleado')
    ax[1].plot(df_resampleado['Fecha'], y_ajustado, color='red', label='Ajuste Lineal')
    ax[1].set_title('Datos Resampleados y Ajuste Lineal')
    ax[1].set_xlabel('Fecha')
    ax[1].set_ylabel('Valor')
    ax[1].legend()
    ax[1].grid(True)

    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)

# Interfaz de Streamlit
st.title("Análisis de Patrones en Datos CSV")
archivo_subido = st.file_uploader("Selecciona un archivo CSV", type="csv")

if archivo_subido is not None:
    df = leer_csv(archivo_subido)
    intervalo = st.selectbox("Selecciona el intervalo (minutos)", [5, 10, 15, 30])
    df_resampleado = resamplear_datos(df, intervalo)
    
    st.write("Datos Resampleados", df_resampleado)
    
    # Margen de tolerancia seleccionado por el usuario
    tolerancia = st.slider("Selecciona el margen de tolerancia", 0.0, 10.0, 1.0)
    
    # Ajustar el patrón y comparar con el margen de tolerancia
    patrón_cercano, distancia, m, b, dentro_tolerancia = ajustar_y_comparar(df_resampleado, tolerancia)
    
    if dentro_tolerancia:
        st.write(f"El patrón más cercano es {patrón_cercano} con una distancia de {distancia:.2f}, dentro del margen de tolerancia.")
    else:
        st.write(f"El patrón más cercano es {patrón_cercano}, pero con una distancia de {distancia:.2f}, fuera del margen de tolerancia.")
    
    # Graficar los datos y el ajuste
    graficar_datos(df, df_resampleado, m, b)
