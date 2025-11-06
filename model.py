"""
Transit Delay Prediction Model

Time-series regression model for predicting Muni bus delays
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import logging
from typing import Tuple, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class TransitDelayPredictor:
    """Predicts bus delays using time-series regression"""
    
    def __init__(self, model_type: str = "random_forest"):
        """
        Initialize predictor
        
        Args:
            model_type: Type of model ('random_forest', 'gradient_boosting', 'xgboost')
        """
        self.model_type = model_type
        self.model = None
        self.feature_names = None
        self.is_trained = False
        
        if model_type == "random_forest":
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=42,
                n_jobs=-1
            )
        elif model_type == "gradient_boosting":
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def train(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        validation_split: float = 0.2
    ) -> Dict[str, float]:
        """
        Train the model
        
        Args:
            X: Feature DataFrame
            y: Target variable (delay in minutes)
            validation_split: Fraction of data for validation
            
        Returns:
            Dictionary of evaluation metrics
        """
        logger.info(f"Training {self.model_type} model with {len(X)} samples")
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        # Time series split for validation
        tscv = TimeSeriesSplit(n_splits=5)
        
        # For final training, use all data
        # But first validate with time series split
        cv_scores = []
        for train_idx, val_idx in tscv.split(X):
            X_train_cv, X_val_cv = X.iloc[train_idx], X.iloc[val_idx]
            y_train_cv, y_val_cv = y.iloc[train_idx], y.iloc[val_idx]
            
            self.model.fit(X_train_cv, y_train_cv)
            y_pred = self.model.predict(X_val_cv)
            mae = mean_absolute_error(y_val_cv, y_pred)
            cv_scores.append(mae)
        
        logger.info(f"Cross-validation MAE: {np.mean(cv_scores):.2f} ± {np.std(cv_scores):.2f} minutes")
        
        # Final training on all data
        self.model.fit(X, y)
        self.is_trained = True
        
        # Evaluation on training data (for reference)
        y_pred = self.model.predict(X)
        
        metrics = {
            "mae": mean_absolute_error(y, y_pred),
            "rmse": np.sqrt(mean_squared_error(y, y_pred)),
            "r2": r2_score(y, y_pred),
            "cv_mae_mean": np.mean(cv_scores),
            "cv_mae_std": np.std(cv_scores)
        }
        
        logger.info(f"Training metrics - MAE: {metrics['mae']:.2f}, RMSE: {metrics['rmse']:.2f}, R²: {metrics['r2']:.3f}")
        
        return metrics
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Array of predicted delays in minutes
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Ensure features match training
        if list(X.columns) != self.feature_names:
            logger.warning("Feature names don't match training data, reordering...")
            X = X[self.feature_names]
        
        predictions = self.model.predict(X)
        
        # Clip predictions to reasonable range (e.g., -10 to 60 minutes)
        predictions = np.clip(predictions, -10, 60)
        
        return predictions
    
    def predict_with_confidence(
        self, 
        X: pd.DataFrame
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions with confidence intervals
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Tuple of (predictions, standard_deviations)
        """
        predictions = self.predict(X)
        
        # For ensemble models, use predictions from individual trees
        if hasattr(self.model, 'estimators_'):
            tree_predictions = np.array([
                tree.predict(X) for tree in self.model.estimators_
            ])
            std_devs = np.std(tree_predictions, axis=0)
        else:
            # Fallback: use global std
            std_devs = np.full_like(predictions, 2.0)
        
        return predictions, std_devs
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importances
        
        Returns:
            DataFrame with features and their importances
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        if not hasattr(self.model, 'feature_importances_'):
            logger.warning("Model doesn't support feature importance")
            return pd.DataFrame()
        
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    def save(self, path: Path):
        """
        Save model to disk
        
        Args:
            path: Path to save model
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        model_data = {
            'model': self.model,
            'model_type': self.model_type,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, path)
        logger.info(f"Model saved to {path}")
    
    @classmethod
    def load(cls, path: Path) -> 'TransitDelayPredictor':
        """
        Load model from disk
        
        Args:
            path: Path to model file
            
        Returns:
            Loaded TransitDelayPredictor instance
        """
        model_data = joblib.load(path)
        
        predictor = cls(model_type=model_data['model_type'])
        predictor.model = model_data['model']
        predictor.feature_names = model_data['feature_names']
        predictor.is_trained = model_data['is_trained']
        
        logger.info(f"Model loaded from {path}")
        return predictor
