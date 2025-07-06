import streamlit as st
import numpy as np
from results_handler import create_temperature_plot, save_simulation_results
from disturbance_handler import generate_random_disturbance_with_params
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title='Simulación de Control de Temperatura', page_icon='🌡️', layout='centered')
st.markdown('<h1 style="font-size:2.1rem; white-space:nowrap; color:#fff; margin-bottom:0.2em;">🌡️ Simulación de Control de Temperatura</h1>', unsafe_allow_html=True)
st.markdown('''<style>body {background-color: #f8f9fa;} .stButton>button {background-color: #006400; color: white; font-size: 1.2em; border-radius: 8px;} .block-container {padding-top: 1.5rem;} </style>''', unsafe_allow_html=True)

if 'sim_done' not in st.session_state:
    st.session_state.sim_done = False
if 'last_fig' not in st.session_state:
    st.session_state.last_fig = None

if not st.session_state.sim_done:
    st.subheader('Parámetros de simulación')
    mode = st.radio('Modo de perturbación', ['Aleatorio', 'Personalizado'], key='mode')
    permitir_fallas = False
    if mode == 'Aleatorio':
        permitir_fallas = st.checkbox('Permitir fallas (perturbaciones largas)', value=True)
    col1, col2 = st.columns(2)
    with col1:
        duration = st.number_input('Duración (min)', min_value=1, max_value=10000, value=1000, step=1, key='duration')
        if mode == 'Aleatorio':
            prob = st.number_input('Probabilidad de perturbación (0-1)', min_value=0.0, max_value=1.0, value=0.005, step=0.001, format='%.3f', key='prob')
            min_temp = st.number_input('Perturbación mínima (°C)', min_value=0.0, max_value=10.0, value=0.6, step=0.1, key='min_temp')
    with col2:
        target = st.slider('Temperatura objetivo (°C)', 17.0, 30.0, 22.0, 0.1, key='target')
        initial = st.slider('Temperatura inicial (°C)', 17.0, 30.0, 26.0, 0.1, key='initial')
        if mode == 'Aleatorio':
            max_temp = st.number_input('Perturbación máxima (°C)', min_value=0.0, max_value=10.0, value=1.2, step=0.1, key='max_temp')
    custom_events = []
    if mode == 'Personalizado':
        if 'custom_events' not in st.session_state:
            st.session_state['custom_events'] = [{'start': 0, 'duration': 1, 'intensity': 1.0}]
        st.markdown('---')
        st.markdown('#### Configuración de perturbaciones personalizadas')
        with st.form('event_control_form', clear_on_submit=True):
            cols_btn = st.columns([1, 1])
            add = cols_btn[0].form_submit_button('Agregar perturbación')
            remove = cols_btn[1].form_submit_button('Quitar última')
            if add:
                st.session_state['custom_events'].append({'start': 0, 'duration': 1, 'intensity': 1.0})
                st.rerun()
            if remove and len(st.session_state['custom_events']) > 1:
                st.session_state['custom_events'].pop()
                st.rerun()
        for i, event in enumerate(st.session_state['custom_events']):
            st.markdown(f'**Perturbación #{i+1}**')
            cols = st.columns(3)
            with cols[0]:
                event['start'] = st.number_input(f'Inicio (min) #{i+1}', min_value=0, max_value=10000, value=event['start'], step=1, key=f'start_{i}')
            with cols[1]:
                event['duration'] = st.number_input(f'Duración (min) #{i+1}', min_value=1, max_value=10000, value=event['duration'], step=1, key=f'duration_{i}')
            with cols[2]:
                event['intensity'] = st.number_input(f'Intensidad (°C) #{i+1}', min_value=0.0, max_value=10.0, value=event['intensity'], step=0.1, key=f'intensity_{i}')
        custom_events = st.session_state['custom_events']
    with st.form('sim_form'):
        submitted = st.form_submit_button('Iniciar Simulación')

    if submitted:
        if mode == 'Aleatorio':
            # En el modo aleatorio, las perturbaciones ahora tienen duración aleatoria
            min_temp = st.session_state['min_temp']
            max_temp = st.session_state['max_temp']
            prob = st.session_state['prob']
            # Definir rango de duración según permitir_fallas
            if permitir_fallas:
                duracion_min = 1
                duracion_max = 6
            else:
                duracion_min = 1
                duracion_max = 3
            if min_temp > max_temp:
                st.error('La perturbación mínima no puede ser mayor que la máxima.')
            elif not (17 <= target <= 30 and 17 <= initial <= 30):
                st.error('Las temperaturas deben estar entre 17 y 30 °C.')
            else:
                st.success('Simulación en curso...')
                hysteresis = 0.5
                cooling_power = 0.2
                current_temperature = initial
                temperature_history = [current_temperature]
                time_points = [0]
                duration_int = int(duration)
                perturbacion_activa = False
                duracion_restante = 0
                intensidad_perturbacion = 0.0
                minutos_en_perturbacion_larga = 0
                corte_por_falla = False
                minuto_falla = None
                duracion_perturbacion_actual = 0
                temperatura_meseta = None
                for current_time in range(1, duration_int + 1):
                    if perturbacion_activa:
                        current_temperature = temperatura_meseta
                        duracion_restante -= 1
                        if duracion_perturbacion_actual > 3:
                            minutos_en_perturbacion_larga += 1
                            if minutos_en_perturbacion_larga >= 3:
                                corte_por_falla = True
                                minuto_falla = current_time
                                break
                        else:
                            minutos_en_perturbacion_larga = 0
                        compressor_on = False
                        temperature_history.append(current_temperature)
                        time_points.append(current_time)
                        if duracion_restante == 0:
                            perturbacion_activa = False
                            minutos_en_perturbacion_larga = 0
                            temperatura_meseta = None
                        continue
                    # Si no hay perturbación activa, puede generarse una nueva
                    disturbance = generate_random_disturbance_with_params({'probability': prob, 'min_temp': min_temp, 'max_temp': max_temp})
                    if disturbance is not None:
                        # Definir duración aleatoria según el rango
                        duracion = random.randint(duracion_min, duracion_max)
                        perturbacion_activa = True
                        duracion_restante = duracion
                        duracion_perturbacion_actual = duracion
                        intensidad_perturbacion = disturbance
                        temperatura_meseta = current_temperature + intensidad_perturbacion
                        minutos_en_perturbacion_larga = 1 if duracion > 3 else 0
                        current_temperature = temperatura_meseta
                        compressor_on = False
                        temperature_history.append(current_temperature)
                        time_points.append(current_time)
                        if duracion > 3 and minutos_en_perturbacion_larga >= 3:
                            corte_por_falla = True
                            minuto_falla = current_time
                            break
                        duracion_restante -= 1
                        if duracion_restante == 0:
                            perturbacion_activa = False
                            minutos_en_perturbacion_larga = 0
                            temperatura_meseta = None
                        continue
                    # Si no hay perturbación, control normal
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
                # Mostrar gráfico y mensaje de error si hubo corte
                save_simulation_results(temperature_history, time_points, target, len(time_points)-1)
                import pandas as pd
                simulation_data = pd.DataFrame({'Time (min)': time_points, 'Temperature (°C)': temperature_history})
                fig = create_temperature_plot(simulation_data, target)
                st.session_state.last_fig = fig
                st.session_state.sim_done = True
                st.pyplot(fig)
                if corte_por_falla:
                    st.error(f'Falla: Se detectó una perturbación aleatoria con duración mayor a 3 minutos en el minuto {minuto_falla}. Ejecución abortada.')
                else:
                    st.success('¡Simulación finalizada! Los resultados se guardaron en la carpeta simulation_results.')
                if st.button('Nueva simulación'):
                    st.session_state.sim_done = False
                    st.session_state.last_fig = None
                    st.rerun()
        else:
            if not (17 <= target <= 30 and 17 <= initial <= 30):
                st.error('Las temperaturas deben estar entre 17 y 30 °C.')
            else:
                st.success('Simulación en curso...')
                from disturbance_handler import generate_custom_disturbances
                hysteresis = 0.5
                cooling_power = 0.2
                current_temperature = initial
                temperature_history = [current_temperature]
                time_points = [0]
                # --- Nueva lógica para perturbaciones tipo "meseta" ---
                # Creamos una lista de "mesetas" activas para cada minuto
                duration_int = int(duration)
                plateau = [None] * (duration_int + 1)  # None si no hay, si hay: (valor objetivo, fin)
                for event in custom_events:
                    start = int(event['start'])
                    end = min(int(event['start']) + int(event['duration']), duration_int)
                    for t in range(start, end):
                        plateau[t] = target + event['intensity']
                corte_por_falla = False
                minuto_falla = None
                perturbacion_larga_activa = None
                minutos_en_perturbacion_larga = 0
                temperatura_meseta = None
                duracion_meseta = 0
                minutos_en_esta_perturbacion = 0
                for current_time in range(1, duration_int + 1):
                    # Verificar si hay una perturbación activa (de cualquier duración)
                    perturbacion_activa = None
                    for event in custom_events:
                        start = int(event['start'])
                        end = min(int(event['start']) + int(event['duration']), duration_int)
                        if start <= current_time < end:
                            perturbacion_activa = event
                            break
                    if perturbacion_activa:
                        if duracion_meseta == 0:
                            temperatura_meseta = current_temperature + perturbacion_activa['intensity']
                            duracion_meseta = int(perturbacion_activa['duration'])
                            minutos_en_esta_perturbacion = 1
                        else:
                            minutos_en_esta_perturbacion += 1
                        current_temperature = temperatura_meseta
                        compressor_on = False
                        temperature_history.append(current_temperature)
                        time_points.append(current_time)
                        # Lógica de corte por falla si la perturbación es larga
                        if duracion_meseta + minutos_en_esta_perturbacion - 1 > 3 and minutos_en_esta_perturbacion > 3:
                            corte_por_falla = True
                            minuto_falla = current_time
                            break
                        duracion_meseta -= 1
                        if duracion_meseta == 0:
                            temperatura_meseta = None
                            minutos_en_esta_perturbacion = 0
                        continue
                    else:
                        temperatura_meseta = None
                        duracion_meseta = 0
                        minutos_en_esta_perturbacion = 0
                    if plateau[current_time] is not None:
                        # (Ya cubierto por la lógica anterior)
                        pass
                    else:
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
                # Mostrar gráfico y mensaje de error si hubo corte
                save_simulation_results(temperature_history, time_points, target, len(time_points)-1)
                import pandas as pd
                simulation_data = pd.DataFrame({'Time (min)': time_points, 'Temperature (°C)': temperature_history})
                fig = create_temperature_plot(simulation_data, target)
                st.session_state.last_fig = fig
                st.session_state.sim_done = True
                st.pyplot(fig)
                if corte_por_falla:
                    st.error(f'Falla: Se detectó una perturbación con duración mayor a 3 minutos en el minuto {minuto_falla}. Ejecución abortada.')
                else:
                    st.success('¡Simulación finalizada! Los resultados se guardaron en la carpeta simulation_results.')
                if st.button('Nueva simulación'):
                    st.session_state.sim_done = False
                    st.session_state.last_fig = None
                    st.rerun()
else:
    st.pyplot(st.session_state.last_fig)
    st.success('¡Simulación finalizada! Los resultados se guardaron en la carpeta simulation_results.')
    if st.button('Nueva simulación'):
        st.session_state.sim_done = False
        st.session_state.last_fig = None
        st.rerun() 