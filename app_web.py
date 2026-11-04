import numpy as np
from scipy.special import erfc
import matplotlib.pyplot as plt
import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Simulador de Dispersión - Cipermetrina",
    page_icon="🧪",
    layout="wide"
)

# Título y descripción principal
st.title("🧪 Modelo 1D de Transporte y Retardación de Cipermetrina en Suelo")
st.markdown("""
Este simulador evalúa la dispersión hidrodinámica del plaguicida **Cipermetrina** mediante la **solución de Ogata-Banks (1961)** modificada para transporte con adsorción (Factor de Retardación $R$).
""")

# Barra lateral de parámetros (Inputs)
st.sidebar.header("⚙️ Parámetros de la Cipermetrina y Suelo")

C0 = st.sidebar.slider(
    "Concentración Inicial C0 (mg/L)", 
    min_value=0.001, max_value=1.0, value=0.05, step=0.005,
    help="Solubilidad máxima / concentración inicial en la fuente."
)

v = st.sidebar.slider(
    "Velocidad del agua v (m/día)", 
    min_value=0.01, max_value=2.0, value=0.5, step=0.05,
    help="Velocidad lineal del flujo de agua subterránea."
)

D = st.sidebar.slider(
    "Coeficiente de Dispersión D (m²/día)", 
    min_value=0.01, max_value=1.0, value=0.1, step=0.01,
    help="Dispersión hidrodinámica intrínseca del medio."
)

st.sidebar.markdown("---")
st.sidebar.header("🌱 Propiedades de Adsorción (Retardación)")

R = st.sidebar.slider(
    "Factor de Retardación (R)", 
    min_value=1.0, max_value=200.0, value=50.0, step=1.0,
    help="Retardación por adsorción en el suelo (R = 1 implica sin adsorción, R > 10 típico de la cipermetrina)."
)

t_eval = st.sidebar.slider(
    "Tiempo de evaluación (días)", 
    min_value=1, max_value=365, value=90, step=1,
    help="Tiempo transcurrido en días desde el derrame/aplicación."
)

# Velocidad y dispersión retardadas para el contaminante
v_c = v / R
D_c = D / R

# Dominio espacial ajustado (0 a 10 metros)
x = np.linspace(0.001, 10, 500)

def ogata_banks_retarded(x, t, C0, v_eff, D_eff):
    term1 = erfc((x - v_eff * t) / (2 * np.sqrt(D_eff * t)))
    term2 = np.exp((v_eff * x) / D_eff) * erfc((x + v_eff * t) / (2 * np.sqrt(D_eff * t)))
    return (C0 / 2.0) * (term1 + term2)

# Cálculo del perfil
C_actual = ogata_banks_retarded(x, t_eval, C0, v_c, D_c)

# Generación de la gráfica con Matplotlib
fig, ax = plt.subplots(figsize=(10, 5))

# Curvas de referencia en el tiempo
tiempos_ref = [30, 90, 180, 365]
estilos = ['--', ':', '-.', '--']

for t_ref, estilo in zip(tiempos_ref, estilos):
    if t_ref != t_eval:
        C_ref = ogata_banks_retarded(x, t_ref, C0, v_c, D_c)
        ax.plot(x, C_ref, linestyle=estilo, label=f"{t_ref} días (ref)", alpha=0.6)

# Curva principal
ax.plot(x, C_actual, color="#2E7D32", linewidth=3, label=f"Día actual ({t_eval} d)")
ax.fill_between(x, C_actual, color="#2E7D32", alpha=0.15)

# Personalización estética
ax.set_title(f"Perfil de Concentración de Cipermetrina a los {t_eval} días (R = {R})", fontsize=13, fontweight='bold')
ax.set_xlabel("Distancia desde la fuente x (metros)", fontsize=11)
ax.set_ylabel("Concentración C(x,t) (mg/L)", fontsize=11)
ax.set_xlim(0, 10)
ax.set_ylim(0, C0 * 1.05)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(loc="upper right")

st.pyplot(fig)

# Métricas y defensa técnica
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avance del Agua (v · t)", f"{v * t_eval:.2f} m")
col2.metric("Frente del Contaminante (v_c · t)", f"{v_c * t_eval:.2f} m")
col3.metric("Velocidad Efectiva (v/R)", f"{v_c:.4f} m/día")
col4.metric("Factor de Retardación R", f"{R}")

st.info(
    "🌿 **Justificación Químico-Ambiental:** La Cipermetrina es un plaguicida fuertemente hidrófobo ($K_{oc} \\approx 100,000 \\text{ mL/g}$). "
    "Su elevadísima adsorción en la materia orgánica del suelo genera un alto factor de retardación ($R$), haciendo que la pluma "
    "avance a una fracción ($1/R$) de la velocidad del agua subterránea."
)
