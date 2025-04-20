import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

class AIEngine:
    def __init__(self):
        self.model = None
        self.model_path = 'models/delay_predictor.pkl'
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            # Initialize a new model if none exists
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            # Note: In a real application, you would train the model here
            # For now, we'll use a dummy model

    def predict_delay(self, shipment_data):
        if self.model is None:
            return 0  # Default prediction if no model is available
        
        # Extract features from shipment data
        features = self._extract_features(shipment_data)
        
        # Make prediction
        prediction = self.model.predict([features])[0]
        return max(0, prediction)  # Ensure prediction is not negative

    def _extract_features(self, shipment):
        # Extract relevant features from shipment data
        # This is a simplified version - you would need to adjust based on your actual data
        features = [
            float(shipment.get('distance', 0)),
            float(shipment.get('weight', 0)),
            float(shipment.get('volume', 0)),
            float(shipment.get('priority', 0)),
            # Add more features as needed
        ]
        return features

# Global instance
ai_engine = AIEngine()

def predict_delay(shipment_data):
    return ai_engine.predict_delay(shipment_data) 