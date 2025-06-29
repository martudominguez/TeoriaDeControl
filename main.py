import numpy as np
from results_handler import save_simulation_results
from disturbance_handler import get_disturbance_parameters, generate_random_disturbance_with_params

def get_simulation_parameters():
    """Get simulation parameters from user input."""
    print("\nSimulation Configuration")
    
    try:
        duration = float(input("Enter total simulation duration in minutes (default=1000): ") or "1000")
        target = float(input("Enter target temperature in Celsius (default=22): ") or "22")
        initial = float(input("Enter initial room temperature in Celsius (default=26): ") or "26")
        
        return {
            'duration': int(duration),
            'target': target,
            'initial': initial
        }
    except ValueError:
        print("Using default values due to invalid input")
        return {
            'duration': 1000,
            'target': 22,
            'initial': 26
        }

# Get simulation parameters
params = get_simulation_parameters()
simulation_interval = 1
simulation_duration = params['duration']
target_temperature = params['target']
initial_temperature = params['initial']

# Get disturbance parameters
disturbance_params = get_disturbance_parameters()

# Initialize simulation variables
current_temperature = initial_temperature
temperature_history = [current_temperature]
time_points = [0]

# Hysteresis control
hysteresis = 0.5  # +/- °C
cooling_power = 0.2  # Effect of compressor when on (°C per minute)


# Main simulation loop
for current_time in range(1, simulation_duration + 1):
    # Generate and apply random disturbance
    disturbance = generate_random_disturbance_with_params(disturbance_params)
    if disturbance is not None:
        current_temperature += disturbance
        print(f"\nRandom disturbance at t={current_time} min: {disturbance:.2f}°C")
    
    # Track compressor state
    if current_time == 1:
        compressor_on = False  # Initial state

    if not compressor_on and current_temperature >= target_temperature + hysteresis:
        compressor_on = True
    elif compressor_on and current_temperature <= target_temperature - hysteresis:
        compressor_on = False

    # Apply cooling if compressor is on
    if compressor_on:
        current_temperature -= cooling_power

    # Guardar la temperatura y el tiempo en cada iteración
    temperature_history.append(current_temperature)
    time_points.append(current_time)

# Save results
save_simulation_results(temperature_history, time_points, target_temperature, simulation_duration)