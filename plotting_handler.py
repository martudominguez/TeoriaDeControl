# plotting_handler.py

import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.ticker import MultipleLocator # <--- 1. IMPORTAR LA HERRAMIENTA NECESARIA

def create_and_save_plots(simulation_data: pd.DataFrame, params: dict, simulation_dir: str):
    """
    Crea y guarda un gráfico con 4 subplots para analizar las señales del sistema.
    """
    fig, axs = plt.subplots(4, 1, figsize=(12, 15), sharex=True)
    fig.suptitle('Análisis de Señales del Sistema de Control de Temperatura', fontsize=16)

    time = simulation_data['Time (min)']
    target_temp = params['target']

    # 1. Gráfico de Perturbaciones
    axs[0].plot(time, simulation_data['Perturbation (°C)'], label='Perturbación Aplicada', color='orange')
    axs[0].set_ylabel('Intensidad (°C)')
    axs[0].set_title('Señal de Perturbación')
    axs[0].grid(True)
    axs[0].legend()
    axs[0].yaxis.set_major_locator(MultipleLocator(1)) # Opcional: Marcas cada 1 grado para perturbación

    # 2. Gráfico de Respuesta del Sistema (Temperatura)
    axs[1].plot(time, simulation_data['Temperature (°C)'], label='Temperatura del Ambiente', color='darkgreen')
    axs[1].axhline(y=target_temp, color='limegreen', linestyle='--', label=f'Objetivo ({target_temp}°C)')
    axs[1].set_ylabel('Temperatura (°C)')
    axs[1].set_title('Respuesta del Sistema')
    axs[1].grid(True)
    axs[1].legend()
    axs[1].yaxis.set_major_locator(MultipleLocator(0.5)) # <--- 2. AÑADIR ESTA LÍNEA (LA SOLUCIÓN)

    # 3. Gráfico de la Señal de Error
    axs[2].plot(time, simulation_data['Error (°C)'], label='Señal de Error (e = T_amb - T_obj)', color='crimson')
    axs[2].axhline(y=0, color='grey', linestyle='--')
    axs[2].set_ylabel('Error (°C)')
    axs[2].set_title('Señal de Error')
    axs[2].grid(True)
    axs[2].legend()
    axs[2].yaxis.set_major_locator(MultipleLocator(0.5)) # <--- 3. AÑADIR ESTA LÍNEA TAMBIÉN

    # 4. Gráfico de la Acción de Control
    axs[3].plot(time, simulation_data['Compressor State'], label='Estado del Compresor', color='dodgerblue', drawstyle='steps-post')
    axs[3].set_yticks([0, 1])
    axs[3].set_yticklabels(['OFF', 'ON'])
    axs[3].set_ylabel('Acción de Control')
    axs[3].set_title('Acción de Control (ON/OFF)')
    axs[3].set_xlabel('Tiempo (min)')
    axs[3].grid(True)
    axs[3].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Guardar el gráfico
    plot_filename = os.path.join(simulation_dir, 'full_analysis_plot.png')
    fig.savefig(plot_filename)
    
    return fig, plot_filename