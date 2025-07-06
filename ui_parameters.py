import streamlit as st

def get_simulation_parameters_ui():
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
    return {
        'mode': mode,
        'permitir_fallas': permitir_fallas,
        'duration': duration,
        'prob': prob if mode == 'Aleatorio' else None,
        'min_temp': min_temp if mode == 'Aleatorio' else None,
        'max_temp': max_temp if mode == 'Aleatorio' else None,
        'target': target,
        'initial': initial,
        'custom_events': custom_events
    } 