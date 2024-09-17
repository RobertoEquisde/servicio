import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generar_datos_patron(tipo, n=100):
    fecha_inicial = datetime.now()
    fechas = [fecha_inicial + timedelta(days=i) for i in range(n)]
    x = np.linspace(0, 99, n)
    
    if tipo == 1:
        y = 0.16 * x + 87.05
    elif tipo == 2:
        y = -0.26 * x + 104.06
    elif tipo == 3:
        y = -0.10 * x + 95.74
    else:
        raise ValueError("Tipo de patrón no reconocido")
    
    df = pd.DataFrame({
        'Fecha': fechas,
        'Valor': y
    })
    
    return df

# Generar datos para cada patrón
df1 = generar_datos_patron(1)
df2 = generar_datos_patron(2)
df3 = generar_datos_patron(3)

# Guardar los DataFrames como CSV (ejecutar en tu entorno local)
df1.to_csv('datos_patron_1.csv', index=False)
df2.to_csv('datos_patron_2.csv', index=False)
df3.to_csv('datos_patron_3.csv', index=False)
