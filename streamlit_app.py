import streamlit as st
import numpy as np
from results_handler import create_temperature_plot, save_simulation_results
from disturbance_handler import generate_random_disturbance_with_params
import matplotlib.pyplot as plt

st.set_page_config(page_title='Simulación de Control de Temperatura', page_icon='🌡️', layout='centered')
st.markdown('<h1 style="font-size:2.1rem; white-space:nowrap; color:#fff; margin-bottom:0.2em;">🌡️ Simulación de Control de Temperatura</h1>', unsafe_allow_html=True)
st.markdown('''<style>body {background-color: #f8f9fa;} .stButton>button {background-color: #006400; color: white; font-size: 1.2em; border-radius: 8px;} .block-container {padding-top: 1.5rem;} </style>''', unsafe_allow_html=True)

if 'sim_done' not in st.session_state:
    st.session_state.sim_done = False
if 'last_fig' not in st.session_state:
    st.session_state.last_fig = None

if not st.session_state.sim_done:
    with st.form('sim_form'):
        st.subheader('Parámetros de simulación')
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input('Duración (min)', min_value=1, max_value=10000, value=1000, step=1)
            prob = st.number_input('Probabilidad de perturbación (0-1)', min_value=0.0, max_value=1.0, value=0.005, step=0.001, format='%.3f')
            min_temp = st.number_input('Perturbación mínima (°C)', min_value=0.0, max_value=10.0, value=0.6, step=0.1)
        with col2:
            target = st.slider('Temperatura objetivo (°C)', 17.0, 30.0, 22.0, 0.1)
            initial = st.slider('Temperatura inicial (°C)', 17.0, 30.0, 26.0, 0.1)
            max_temp = st.number_input('Perturbación máxima (°C)', min_value=0.0, max_value=10.0, value=1.2, step=0.1)
        submitted = st.form_submit_button('Iniciar Simulación')

    if submitted:
        if min_temp > max_temp:
            st.error('La perturbación mínima no puede ser mayor que la máxima.')
        elif not (17 <= target <= 30 and 17 <= initial <= 30):
            st.error('Las temperaturas deben estar entre 17 y 30 °C.')
        else:
            st.success('Simulación en curso...')
            # Simulación
            hysteresis = 0.5
            cooling_power = 0.2
            current_temperature = initial
            temperature_history = [current_temperature]
            time_points = [0]
            disturbance_params = {
                'probability': prob,
                'min_temp': min_temp,
                'max_temp': max_temp
            }
            for current_time in range(1, int(duration) + 1):
                disturbance = generate_random_disturbance_with_params(disturbance_params)
                if disturbance is not None:
                    current_temperature += disturbance
                if current_time == 1:
                    compressor_on = False
                if not compressor_on and current_temperature >= target + hysteresis:
                    compressor_on = True
                elif compressor_on and current_temperature <= target - hysteresis:
                    compressor_on = False
                if compressor_on:
                    current_temperature -= cooling_power
                temperature_history.append(current_temperature)
                time_points.append(current_time)
            # Guardar resultados y mostrar gráfico
            save_simulation_results(temperature_history, time_points, target, int(duration))
            import pandas as pd
            simulation_data = pd.DataFrame({'Time (min)': time_points, 'Temperature (°C)': temperature_history})
            fig = create_temperature_plot(simulation_data, target)
            st.session_state.last_fig = fig
            st.session_state.sim_done = True
            st.rerun()
else:
    st.pyplot(st.session_state.last_fig)
    st.success('¡Simulación finalizada! Los resultados se guardaron en la carpeta simulation_results.')
    if st.button('Nueva simulación'):
        st.session_state.sim_done = False
        st.session_state.last_fig = None
        st.rerun() 