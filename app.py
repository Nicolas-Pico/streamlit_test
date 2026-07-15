import time

import pandas as pd
import scipy.stats
import streamlit as st

# ==========================
# Estado de la aplicación
# ==========================

# estas son variables de estado que se conservan cuando Streamlin vuelve a ejecutar este script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

# ==========================
# Interfaz
# ==========================
st.header('Lanzar una moneda')

number_of_trials = st.slider(
    '¿Número de intentos?', 
    1, 
    1000, 
    10

)
start_button = st.button('Ejecutar')

# ==========================
# Función principal
# ==========================

def toss_coin(n: int) -> float:
    """
    Simula n lanzamientos de una moneda y
    muestra la evolución de la media.
    """

    # Placeholder donde irá el gráfico
    chart_placeholder = st.empty()

    # Generar los lanzamientos
    trial_outcomes = scipy.stats.bernoulli.rvs(
        p=0.5,
        size=n
    )

    medias = []

    caras = 0

    for intento, resultado in enumerate(trial_outcomes, start=1):

        if resultado == 1:
            caras += 1

        media = caras / intento

        medias.append(media)

        # Actualizar el gráfico
        chart_placeholder.line_chart(
            pd.DataFrame(
                {"Media": medias}
            )
        )

        time.sleep(0.05)

    return media

# ==========================
# Ejecutar experimento
# ==========================

if start_button:

    st.write(f"Experimento con **{number_of_trials}** intentos en curso...")

    st.session_state["experiment_no"] += 1

    mean = toss_coin(number_of_trials)

    nuevo_resultado = pd.DataFrame(
        {
            "no": [st.session_state["experiment_no"]],
            "iteraciones": [number_of_trials],
            "media": [mean],
        }
    )

    # Evita FutureWarning de pandas
    if st.session_state["df_experiment_results"].empty:
        st.session_state["df_experiment_results"] = nuevo_resultado
    else:
        st.session_state["df_experiment_results"] = pd.concat(
            [
                st.session_state["df_experiment_results"],
                nuevo_resultado,
            ],
            ignore_index=True,
        )

# ==========================
# Mostrar historial
# ==========================

st.subheader("Resultados")

st.dataframe(
    st.session_state["df_experiment_results"],
    use_container_width=True,
)