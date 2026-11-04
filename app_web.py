import numpy as np
from scipy.special import erfc
import matplotlib.pyplot as plt
import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Simulador de Dispersión de Contaminantes",
    page_icon="🧪",
    layout="wide"
)

# Título y descripción principal
st.title("🧪 Modelo 1D de Dispersión de Contaminantes en Suelo")
st.markdown("""
Este simulador permite evaluar la concentración de un contaminante en un medio poroso unidimensional a lo largo de la distancia $x$ y en un tiempo determinado $t$, utilizando la **solución analítica de Ogata-Banks (1961)** para la ecuación de advección-dispersión.
""")

# Barra lateral de parámetros (Inputs)
st.sidebar.header("⚙️ Parámetros del Suelo y Contaminante")

C0 = st.sidebar.slider(
    "Concentración Inicial C0 (mg/L)", 
    min_value=10.0, max_value=500.0, value=100.0, step=10.0,
    help="Concentración constante del contaminante en la fuente (x = 0)."
)

v = st.sidebar.slider(
    "Velocidad del agua v (m/día)", 
    min_value=0.01, max_value=2.0, value=0.5, step=0.05,
    help="Velocidad lineal media del flujo subterráneo (advección)."
)

D = st.sidebar.slider(
    "Coeficiente de Dispersión D (m²/día)", 
    min_value=0.01, max_value=1.0, value=0.1, step=0.01,
    help="Coeficiente de dispersión hidrodinámica (difusión molecular + dispersión mecánica)."
)

t_eval = st.sidebar.slider(
    "Tiempo principal de evaluación (días)", 
    min_value=1, max_value=100, value=30, step=1,
    help="Tiempo en el cual se evalúa la curva principal resaltada."
)

# Cálculo de la solución analítica de Ogata-Banks
x = np.linspace(0.01, 50, 500) # Dominio espacial de 0 a 50 metros

def ogata_banks(x, t, C0, v, D):
    term1 = erfc((x - v * t) / (2 * np.sqrt(D * t)))
    term2 = np.exp((v * x) / D) * erfc((x + v * t) / (2 * np.sqrt(D * t)))
    return (C0 / 2.0) * (term1 + term2)

# Concentración para el tiempo seleccionado
C_actual = ogata_banks(x, t_eval, C0, v, D)

# Generación de la gráfica con Matplotlib
fig, ax = plt.subplots(figsize=(10, 5))

# Curvas de referencia en el tiempo (para comparación)
tiempos_ref = [10, 30, 60, 90]
estilos = ['--', ':', '-.', '--']
colores_ref = ['#888888', '#aaaaaa', '#cccccc', '#999999']

for t_ref, estilo in zip(tiempos_ref, estilos):
    if t_ref != t_eval:
        C_ref = ogata_banks(x, t_ref, C0, v, D)
        ax.plot(x, C_ref, linestyle=estilo, label=f"{t_ref} días (ref)", alpha=0.7)

# Curva principal resaltada
ax.plot(x, C_actual, color="#D32F2F", linewidth=3, label=f"Día actual ({t_eval} d)")
ax.fill_between(x, C_actual, color="#D32F2F", alpha=0.15)

# Personalización estética de la gráfica
ax.set_title(f"Perfil de Concentración Espacial a los {t_eval} días", fontsize=14, fontweight='bold')
ax.set_xlabel("Distancia desde la fuente x (metros)", fontsize=11)
ax.set_ylabel("Concentración C(x,t) (mg/L)", fontsize=11)
ax.set_xlim(0, 50)
ax.set_ylim(0, C0 * 1.05)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(loc="upper right")

# Mostrar gráfica en la app de Streamlit
st.pyplot(fig)

# Métrica e información de contexto
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Concentración en Fuente (x=0)", f"{C0} mg/L")
col2.metric("Frente AdvectivoTeórico (v · t)", f"{v * t_eval:.2f} m")
col3.metric("Dispersión Hidrodinámica (D)", f"{D} m²/día")

st.info(
    "💡 **Nota conceptual:** La curva sigmoidea representa el frente de mezcla donde actúan "
    "conjuntamente la advección (traslación) y la dispersión (ensanchamiento del perfil)."
)
