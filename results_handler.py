import os
import pandas as pd
from datetime import datetime

def create_simulation_directory():
    """Crea un directorio único para cada simulación."""
    results_dir = "simulation_results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    simulation_dir = os.path.join(results_dir, f"simulation_{timestamp}")
    os.makedirs(simulation_dir)
    return simulation_dir

def save_simulation_data(simulation_dir: str, simulation_df: pd.DataFrame):
    """Guarda los datos de la simulación en un archivo CSV."""
    csv_filename = os.path.join(simulation_dir, 'simulation_data.csv')
    simulation_df.to_csv(csv_filename, index=False)
    return csv_filename

def save_summary(simulation_dir: str, simulation_df: pd.DataFrame, params: dict):
    """Guarda un resumen estadístico de la simulación."""
    summary_filename = os.path.join(simulation_dir, 'simulation_summary.txt')
    with open(summary_filename, 'w') as f:
        f.write(f"Temperatura Objetivo: {params['target']:.2f} °C\n")
        f.write(f"Temperatura Inicial: {params['initial']:.2f} °C\n")
        f.write(f"Duración de Simulación: {params['duration']} minutos\n\n")
        f.write("Estadísticas de la simulación:\n")
        f.write(str(simulation_df.describe()))
    return summary_filename