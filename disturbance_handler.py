import random

def get_disturbance_parameters():
    """Get user input for disturbance parameters."""
    print("\nRandom Disturbance Configuration")
    print("Note: Disturbances can only increase temperature (cooling-only system)")
    
    try:
        prob = float(input("Enter disturbance probability per minute (0-1, default=0.005): ") or "0.005")
        min_temp = float(input("Enter minimum temperature variation (default=0.6): ") or "0.6")
        max_temp = float(input("Enter maximum temperature variation (default=1.2): ") or "1.2")
        
        # Ensure values are positive
        min_temp = max(0.1, min_temp)
        max_temp = max(min_temp, max_temp)
        
        return {
            'probability': prob,
            'min_temp': min_temp,
            'max_temp': max_temp
        }
    except ValueError:
        print("Using default values due to invalid input")
        return {
            'probability': 0.005,
            'min_temp': 0.6,
            'max_temp': 1.2
        }

def generate_random_disturbance_with_params(params):
    """Generate a random temperature disturbance using custom parameters."""
    if random.random() < params['probability']:
        temperature_change = random.uniform(params['min_temp'], params['max_temp'])
        return temperature_change
    return None

def generate_custom_disturbances(events, duration):
    """Genera un array de perturbaciones para cada minuto, según los eventos personalizados."""
    disturbances = [0.0] * (duration + 1)
    for event in events:
        start = int(event['start'])
        end = min(int(event['start']) + int(event['duration']), duration)
        for t in range(start, end):
            disturbances[t] += event['intensity']
    return disturbances