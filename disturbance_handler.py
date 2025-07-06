import random

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