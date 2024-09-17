import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Título de la aplicación
st.title("Subir Imagen y Extraer Puntos de la Gráfica")

# Permitir al usuario subir una imagen
uploaded_file = st.file_uploader("Sube una imagen de la gráfica", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Abrir la imagen y convertirla a escala de grises
    image = Image.open(uploaded_file).convert("L")
    st.image(image, caption="Imagen subida", use_column_width=True)
    
    # Convertir la imagen a un array de numpy
    image_np = np.array(image)

    # Mostrar dimensiones de la imagen
    st.write(f"Dimensiones de la imagen: {image_np.shape}")
    
    # Suponiendo que la gráfica es negra sobre un fondo blanco,
    # encontraremos los puntos donde los píxeles son oscuros (cercanos a 0)
    threshold = st.slider("Selecciona el umbral de intensidad", 0, 255, 100)
    
    # Extraer los puntos que tienen un valor menor al umbral (son oscuros)
    points = np.column_stack(np.where(image_np < threshold))
    
    # Invertir las coordenadas y mostrar los puntos (x, y)
    x_points = points[:, 1]  # Columnas de la imagen
    y_points = points[:, 0]  # Filas de la imagen
    
    st.write(f"Se encontraron {len(points)} puntos.")

    # Graficar los puntos extraídos
    fig, ax = plt.subplots()
    ax.scatter(x_points, y_points, label='Puntos extraídos', color='red', s=1)
    ax.invert_yaxis()  # Invertir el eje Y porque en las imágenes el origen está en la esquina superior
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    st.pyplot(fig)

    # Ajuste de curva (por ejemplo, una línea recta)
    def linear_function(x, m, b):
        return m * x + b

    # Para hacer el ajuste, simplificamos los puntos seleccionando una parte de ellos
    # (usualmente seleccionar todos podría hacer el ajuste pesado)
    sample_points = np.random.choice(len(x_points), size=min(500, len(x_points)), replace=False)
    x_sample = x_points[sample_points]
    y_sample = y_points[sample_points]

    # Ajuste de curva
    from scipy.optimize import curve_fit
    params, _ = curve_fit(linear_function, x_sample, y_sample)
    m, b = params

    # Mostrar la función ajustada
    st.write(f"Función ajustada: y = {m:.2f}x + {b:.2f}")

    # Graficar la curva ajustada junto con los puntos
    y_fit = linear_function(x_points, m, b)
    
    fig, ax = plt.subplots()
    ax.scatter(x_points, y_points, label='Puntos extraídos', color='red', s=1)
    ax.plot(x_points, y_fit, label=f'Ajuste: y = {m:.2f}x + {b:.2f}', color='blue')
    ax.invert_yaxis()  # Invertir el eje Y
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    st.pyplot(fig)
