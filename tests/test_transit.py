"""
Unit tests for transit prediction module
"""

import pytest
import pandas as pd
import numpy as np
from src.transit import TransitFeatureEngine, TransitDelayPredictor


class TestTransitFeatureEngine:
    """Test transit feature engineering"""
    
    def test_temporal_features(self):
        """Test temporal feature creation"""
        # Create sample data
        data = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=24, freq='H'),
            'route_id': ['14'] * 24,
            'delay_seconds': np.random.randint(-60, 300, 24)
        })
        
        engine = TransitFeatureEngine()
        features = engine.create_features(data)
        
        # Check features exist
        assert 'hour' in features.columns
        assert 'day_of_week' in features.columns
        assert 'is_weekend' in features.columns
        assert 'hour_sin' in features.columns
    
    def test_delay_calculation(self):
        """Test delay calculation from seconds"""
        data = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=10, freq='H'),
            'route_id': ['14'] * 10,
            'delay_seconds': [0, 60, 120, 180, 240, 300, -60, -120, 0, 180]
        })
        
        engine = TransitFeatureEngine()
        features = engine.create_features(data)
        
        assert 'delay_minutes' in features.columns
        assert features['delay_minutes'].iloc[1] == 1.0  # 60 seconds = 1 minute
        assert features['delay_minutes'].iloc[2] == 2.0  # 120 seconds = 2 minutes


class TestTransitDelayPredictor:
    """Test transit delay prediction model"""
    
    def test_model_initialization(self):
        """Test model can be initialized"""
        model = TransitDelayPredictor(model_type='random_forest')
        assert model.model is not None
        assert not model.is_trained
    
    def test_model_training(self):
        """Test model training"""
        # Create synthetic training data
        n_samples = 100
        X = pd.DataFrame({
            'hour': np.random.randint(0, 24, n_samples),
            'day_of_week': np.random.randint(0, 7, n_samples),
            'is_peak_hour': np.random.randint(0, 2, n_samples),
        })
        y = pd.Series(np.random.randint(0, 10, n_samples))
        
        model = TransitDelayPredictor(model_type='random_forest')
        metrics = model.train(X, y)
        
        assert model.is_trained
        assert 'mae' in metrics
        assert 'rmse' in metrics
        assert metrics['mae'] >= 0
    
    def test_prediction(self):
        """Test making predictions"""
        # Train on synthetic data
        n_samples = 100
        X_train = pd.DataFrame({
            'hour': np.random.randint(0, 24, n_samples),
            'day_of_week': np.random.randint(0, 7, n_samples),
            'is_peak_hour': np.random.randint(0, 2, n_samples),
        })
        y_train = pd.Series(np.random.randint(0, 10, n_samples))
        
        model = TransitDelayPredictor(model_type='random_forest')
        model.train(X_train, y_train)
        
        # Make predictions
        X_test = X_train.head(5)
        predictions = model.predict(X_test)
        
        assert len(predictions) == 5
        assert all(-10 <= p <= 60 for p in predictions)  # Within reasonable bounds


if __name__ == '__main__':
    pytest.main([__file__])
