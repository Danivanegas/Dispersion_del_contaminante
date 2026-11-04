import numpy as np
from scipy.special import erfc
import matplotlib.pyplot as plt
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Simulador de Suelos", layout="centered")

st.title("🧪 Modelo 1D de Dispersión de Contaminantes en Suelo")
st.subheader("Ecuación Analítica de Ogata-Banks (Curva de Avance Temporal)")

# Barra lateral: Parámetros del modelo
st.sidebar.header("Parámetros del Suelo y Contaminante")

C0 = st.sidebar.slider("Concentración Inicial C0 (mg/L)", 10.0, 500.0, 100.0)
v = st.sidebar.slider("Velocidad del agua v (m/día)", 0.01, 2.0, 0.5)
D = st.sidebar.slider("Coeficiente de Dispersión D (m²/día)", 0.01, 1.0, 0.1)

st.sidebar.markdown("---")
st.sidebar.header("Ubicación de Monitoreo")
x_pozo = st.sidebar.slider("Distancia del pozo/punto x (metros)", 1.0, 50.0, 10.0)

# Dominio temporal (de 0 a 100 días)
t = np.linspace(0.1, 100, 500)

# Solución analítica de Ogata-Banks en función del tiempo para una distancia fija x
term1 = erfc((x_pozo - v * t) / (2 * np.sqrt(D * t)))
term2 = np.exp((v * x_pozo) / D) * erfc((x_pozo + v * t) / (2 * np.sqrt(D * t)))
C_t = (C0 / 2.0) * (term1 + term2)

# Graficación (Curva S Ascendente - Breagrama)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(t, C_t, color="#00C853", linewidth=3, label=f"Pozo a x = {x_pozo} m")
ax.fill_between(t, C_t, color="#00C853", alpha=0.15)

# Títulos y ejes
ax.set_title(f"Curva de Avance de Concentración (Pozo a {x_pozo} m de la fuente)", fontsize=12, fontweight='bold')
ax.set_xlabel("Tiempo t (días)", fontsize=10)
ax.set_ylabel("Concentración C(x,t) (mg/L)", fontsize=10)
ax.grid(True, linestyle="--", alpha=0.6)
ax.legend(loc="upper left")

# Mostrar gráfica en Streamlit
st.pyplot(fig)

st.info(
    "💡 **Justificación Teórica:** Esta gráfica representa el **Breagrama (Curva de Avance)** en un punto de monitoreo fijo. "
    "Muestra la transición en forma de 'S' ascendente a medida que la pluma advectiva-dispersiva alcanza y satura el punto evaluado."
)
