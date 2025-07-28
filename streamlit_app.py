import streamlit as st
from ui_parameters import get_simulation_parameters_ui
from simulation_logic import run_simulation # Importamos la función principal
from results_handler import create_simulation_directory, save_simulation_data, save_summary
from plotting_handler import create_and_save_plots

# --- Configuración de la página ---
st.set_page_config(page_title='Simulación de Control de Temperatura', page_icon='🌡️', layout='wide')
st.title('🌡️ Simulación y Análisis de Sistema de Control de Temperatura')

# --- Estado de la Sesión ---
if 'sim_done' not in st.session_state:
    st.session_state.sim_done = False
if 'last_fig' not in st.session_state:
    st.session_state.last_fig = None
if 'results_dir' not in st.session_state:
    st.session_state.results_dir = ""

def reset_simulation():
    """Reinicia el estado para una nueva simulación."""
    st.session_state.sim_done = False
    st.session_state.last_fig = None
    st.session_state.results_dir = ""
    if 'custom_events' in st.session_state:
        del st.session_state['custom_events']
    st.rerun()

# --- Flujo Principal de la App ---
if not st.session_state.sim_done:
    params = get_simulation_parameters_ui()
    
    if st.button('Iniciar Simulación', key='start_button'):
        with st.spinner('Ejecutando simulación y generando análisis...'):
            # 1. Ejecutar la lógica de la simulación para cualquier modo
            results_df, sim_status = run_simulation(params)

            # 2. Guardar resultados
            simulation_dir = create_simulation_directory()
            save_simulation_data(simulation_dir, results_df)
            save_summary(simulation_dir, results_df, params)

            # 3. Generar y guardar los gráficos de análisis
            fig, plot_path = create_and_save_plots(results_df, params, simulation_dir)

            # 4. Actualizar el estado de la sesión para mostrar los resultados
            st.session_state.sim_done = True
            st.session_state.last_fig = fig
            st.session_state.results_dir = simulation_dir
            st.rerun()
else:
    st.success(f"¡Simulación finalizada! Los resultados se guardaron en: `{st.session_state.results_dir}`")
    st.pyplot(st.session_state.last_fig)
    
    if st.button('Realizar una Nueva Simulación'):
        reset_simulation()