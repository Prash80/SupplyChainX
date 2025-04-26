import numpy as np
from datetime import datetime

def predict_delay(shipment_data):
    """
    Predicts potential delay based on shipment data.
    This is a simplified prediction that considers:
    - Distance
    - Weight
    - Volume
    - Priority
    - Current status
    """
    try:
        # Base delay factor
        delay_factor = 0
        
        # Distance impact (longer distance = higher chance of delay)
        distance = float(shipment_data.get('distance', 0))
        if distance > 5000:
            delay_factor += 0.3
        elif distance > 2000:
            delay_factor += 0.2
        elif distance > 1000:
            delay_factor += 0.1
        
        # Weight impact (heavier shipments = higher chance of delay)
        weight = float(shipment_data.get('weight', 0))
        if weight > 2000:
            delay_factor += 0.2
        elif weight > 1000:
            delay_factor += 0.1
        
        # Volume impact (larger volume = higher chance of delay)
        volume = float(shipment_data.get('volume', 0))
        if volume > 30:
            delay_factor += 0.2
        elif volume > 20:
            delay_factor += 0.1
        
        # Priority impact (lower priority = higher chance of delay)
        priority = float(shipment_data.get('priority', 0))
        if priority == 3:  # Lowest priority
            delay_factor += 0.3
        elif priority == 2:
            delay_factor += 0.2
        elif priority == 1:
            delay_factor += 0.1
        
        # Status impact
        status = shipment_data.get('status', '')
        if status == 'Delayed':
            delay_factor += 0.4
        elif status == 'In Transit':
            delay_factor += 0.2
        
        # Calculate final delay in hours
        # Base delay is 0-48 hours, modified by delay_factor
        base_delay = np.random.uniform(0, 48)
        final_delay = base_delay * delay_factor
        
        return round(final_delay, 1)
    
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return 0  # Return 0 if there's any error 