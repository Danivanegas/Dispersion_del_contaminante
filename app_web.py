import streamlit as st
import numpy as np
from scipy.special import erfc
import matplotlib.pyplot as plt

# Configuración de página ancha
st.set_page_config(page_title="Simulador de Suelos", layout="wide")

st.title('🔬 Simulador de Dispersión de Contaminantes en Suelo (1D)')
st.write("Modelo analítico de advección-dispersión hidrodinámica de Ogata-Banks.")

# Barra lateral
st.sidebar.header('⚙️ Parámetros del Suelo y Contaminante')
C0 = st.sidebar.slider('Concentración Inicial C0 (mg/L)', 10.0, 500.0, 100.0)
v = st.sidebar.slider('Velocidad del agua v (m/día)', 0.05, 2.0, 0.5)
D = st.sidebar.slider('Coeficiente de Dispersión D (m²/día)', 0.01, 1.0, 0.1)
tiempo_eval = st.sidebar.slider('Tiempo principal de evaluación (días)', 1, 120, 30)

# Cálculos para la curva seleccionada
x = np.linspace(0.1, 50, 500)
def calcular_C(t):
    term1 = erfc((x - v * t) / (2 * np.sqrt(D * t)))
    term2 = np.exp((v * x) / D) * erfc((x + v * t) / (2 * np.sqrt(D * t)))
    return (C0 / 2.0) * (term1 + term2)

C_actual = calcular_C(tiempo_eval)

# Tarjetas de Métricas (Dashboard)
col1, col2, col3 = st.columns(3)
col1.metric("Frente de Avance Promedio", f"{v * tiempo_eval:.2f} m")
col2.metric("Concentración en Origen (x=0)", f"{C0} mg/L")
col3.metric("Tiempo Simulado", f"{tiempo_eval} Días")

# Gráfica interactiva avanzadas
fig, ax = plt.subplots(figsize=(10, 5))

# Dibujar curvas de tiempo previas como referencia
for t_ref in [10, 30, 60, 90]:
    if t_ref != tiempo_eval:
        ax.plot(x, calcular_C(t_ref), linestyle='--', alpha=0.4, label=f'{t_ref} días (ref)')

# Dibujar curva actual activa
ax.plot(x, C_actual, color='crimson', linewidth=3, label=f'Día actual ({tiempo_eval} d)')
ax.fill_between(x, C_actual, color='crimson', alpha=0.25)

ax.set_title(f'Perfil de Concentración a los {tiempo_eval} días', fontsize=12, fontweight='bold')
ax.set_xlabel('Distancia desde la fuente x (metros)', fontsize=10)
ax.set_ylabel('Concentración C(x,t) (mg/L)', fontsize=10)
ax.set_ylim(0, C0 * 1.05)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper right')

# Mostrar en la app web
st.pyplot(fig)