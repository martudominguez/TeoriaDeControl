import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

def create_simulation_directory():
    """Create a new directory for the simulation results with timestamp."""
    results_dir = "simulation_results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    simulation_dir = os.path.join(results_dir, f"simulation_{timestamp}")
    os.makedirs(simulation_dir)
    return simulation_dir

def save_simulation_data(simulation_dir, time_points, temperature_history):
    """Save simulation data to CSV file."""
    simulation_data = pd.DataFrame({
        'Time (min)': time_points,
        'Temperature (°C)': temperature_history,
    })
    
    csv_filename = os.path.join(simulation_dir, 'simulation_data.csv')
    simulation_data.to_csv(csv_filename, index=False)
    return simulation_data, csv_filename

def create_temperature_plot(simulation_data, target_temperature):
    """Create and return the temperature plot."""
    plt.figure(figsize=(12, 6))
    
    plt.plot(simulation_data['Time (min)'], simulation_data['Temperature (°C)'], 
             color='#006400',
             linewidth=2,
             label='Room Temperature')
    
    plt.axhline(y=target_temperature, 
               color='#4CAF50',
               linestyle='--', 
               linewidth=2,
               label='Target Temperature')
    
    plt.xlabel('Time (min)')
    plt.ylabel('Temperature (°C)')
    plt.title('Air Conditioning Temperature Control Simulation (Cooling Only)')
    plt.legend()
    plt.grid(True)

    # Marcas del eje Y cada 0.5 grados
    ymin = simulation_data['Temperature (°C)'].min()
    ymax = simulation_data['Temperature (°C)'].max()
    plt.yticks(np.arange(np.floor(ymin), np.ceil(ymax) + 0.5, 0.5))
    
    plt.tight_layout()
    
    return plt.gcf()

def save_plot(simulation_dir, figure):
    """Save the plot to a file."""
    plot_filename = os.path.join(simulation_dir, 'temperature_plot.png')
    figure.savefig(plot_filename)
    plt.show()
    return plot_filename

def save_summary(simulation_dir, temperature_history, simulation_duration, target_temperature, simulation_data):
    """Save simulation summary to a text file."""
    summary_filename = os.path.join(simulation_dir, 'simulation_summary.txt')
    with open(summary_filename, 'w') as f:
        f.write(f"Final room temperature: {temperature_history[-1]:.2f} °C\n")
        f.write(f"Simulation duration: {simulation_duration} minutes\n")
        f.write(f"Target temperature: {target_temperature} °C\n")
        f.write("\nSimulation statistics:\n")
        f.write(str(simulation_data.describe()))
    return summary_filename

def print_results_info(simulation_dir, csv_filename, plot_filename, summary_filename):
    """Print information about saved results."""
    print(f"\nResults saved in '{simulation_dir}' directory:")
    print(f"- Data: {csv_filename}")
    print(f"- Plot: {plot_filename}")
    print(f"- Summary: {summary_filename}")

def save_simulation_results(temperature_history, time_points, target_temperature, simulation_duration):
    """Main function to save all simulation results."""
    simulation_dir = create_simulation_directory()
    
    simulation_data, csv_filename = save_simulation_data(simulation_dir, time_points, temperature_history)
    
    figure = create_temperature_plot(simulation_data, target_temperature)
    plot_filename = save_plot(simulation_dir, figure)
    
    summary_filename = save_summary(simulation_dir, temperature_history, 
                                  simulation_duration, target_temperature, 
                                  simulation_data)
    
    print_results_info(simulation_dir, csv_filename, plot_filename, summary_filename)
    
    return simulation_dir 