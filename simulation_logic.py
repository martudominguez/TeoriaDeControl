import pandas as pd
import random
from disturbance_handler import generate_custom_disturbances, generate_random_disturbance_with_params

def run_simulation(params: dict):
    """
    Función principal que ejecuta la simulación según el modo seleccionado.
    """
    if params['mode'] == 'Personalizado':
        return run_custom_simulation(params)
    elif params['mode'] == 'Aleatorio':
        return run_random_simulation(params)

def run_custom_simulation(params: dict):
    """
    Ejecuta la simulación con perturbaciones personalizadas y retorna un DataFrame con todos los resultados.
    """
    duration = params['duration']
    target_temp = params['target']
    initial_temp = params['initial']
    events = params['custom_events']
    
    hysteresis = 0.5
    cooling_power = 0.2

    disturbances = generate_custom_disturbances(events, duration)

    current_temp = initial_temp
    compressor_on = False
    
    time_history, temp_history, compressor_history, error_history, disturbance_history = [0], [current_temp], [0], [current_temp - target_temp], [0]
    
    for t in range(1, duration + 1):
        current_temp += disturbances[t-1]
        
        if not compressor_on and current_temp > target_temp + hysteresis:
            compressor_on = True
        elif compressor_on and current_temp < target_temp - hysteresis:
            compressor_on = False
            
        if compressor_on:
            current_temp -= cooling_power
            
        time_history.append(t)
        temp_history.append(current_temp)
        compressor_history.append(1 if compressor_on else 0)
        error_history.append(current_temp - target_temp)
        disturbance_history.append(disturbances[t-1])

    results_df = pd.DataFrame({
        'Time (min)': time_history,
        'Temperature (°C)': temp_history,
        'Compressor State': compressor_history,
        'Error (°C)': error_history,
        'Perturbation (°C)': disturbance_history
    })

    return results_df, {'corte_por_falla': False, 'minuto_falla': None}


def run_random_simulation(params: dict):
    """
    Ejecuta la simulación con perturbaciones aleatorias y retorna un DataFrame.
    """
    duration = params['duration']
    target_temp = params['target']
    initial_temp = params['initial']
    
    hysteresis = 0.5
    cooling_power = 0.2
    
    current_temp = initial_temp
    compressor_on = False
    
    time_history, temp_history, compressor_history, error_history, disturbance_history = [0], [current_temp], [0], [current_temp - target_temp], [0]

    for t in range(1, duration + 1):
        # Generar posible perturbación en este instante de tiempo
        disturbance_val = generate_random_disturbance_with_params({
            'probability': params['prob'],
            'min_temp': params['min_temp'],
            'max_temp': params['max_temp']
        }) or 0.0

        current_temp += disturbance_val

        if not compressor_on and current_temp > target_temp + hysteresis:
            compressor_on = True
        elif compressor_on and current_temp < target_temp - hysteresis:
            compressor_on = False
        
        if compressor_on:
            current_temp -= cooling_power
            
        time_history.append(t)
        temp_history.append(current_temp)
        compressor_history.append(1 if compressor_on else 0)
        error_history.append(current_temp - target_temp)
        disturbance_history.append(disturbance_val)

    results_df = pd.DataFrame({
        'Time (min)': time_history,
        'Temperature (°C)': temp_history,
        'Compressor State': compressor_history,
        'Error (°C)': error_history,
        'Perturbation (°C)': disturbance_history
    })

    return results_df, {'corte_por_falla': False, 'minuto_falla': None}