"""
Transit Feature Engineering

Creates features for transit delay prediction model
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class TransitFeatureEngine:
    """Feature engineering for transit delay prediction"""
    
    def __init__(self, lag_hours: List[int] = [1, 3, 24, 168]):
        """
        Initialize feature engine
        
        Args:
            lag_hours: Hours to create lag features for
        """
        self.lag_hours = lag_hours
        
    def create_features(
        self, 
        df: pd.DataFrame,
        include_weather: bool = False,
        include_events: bool = False
    ) -> pd.DataFrame:
        """
        Create features from raw transit data
        
        Args:
            df: Raw transit data
            include_weather: Whether to include weather features
            include_events: Whether to include event features
            
        Returns:
            DataFrame with engineered features
        """
        df = df.copy()
        
        # Ensure timestamp is datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
        
        # Temporal features
        df = self._add_temporal_features(df)
        
        # Delay features (target variable)
        df = self._add_delay_features(df)
        
        # Lag features
        df = self._add_lag_features(df)
        
        # Route-specific features
        df = self._add_route_features(df)
        
        # Optional features
        if include_weather:
            df = self._add_weather_features(df)
            
        if include_events:
            df = self._add_event_features(df)
        
        logger.info(f"Created {len(df.columns)} features")
        return df
    
    def _add_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add time-based features"""
        if 'timestamp' not in df.columns:
            return df
            
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['day_of_month'] = df['timestamp'].dt.day
        df['month'] = df['timestamp'].dt.month
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # Peak hours
        df['is_morning_peak'] = df['hour'].between(7, 9).astype(int)
        df['is_evening_peak'] = df['hour'].between(16, 18).astype(int)
        df['is_peak_hour'] = (df['is_morning_peak'] | df['is_evening_peak']).astype(int)
        
        # Cyclical encoding for hour
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        
        # Cyclical encoding for day of week
        df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        return df
    
    def _add_delay_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate delay from schedule deviation"""
        if 'delay_seconds' in df.columns:
            df['delay_minutes'] = df['delay_seconds'] / 60
        elif 'aimed_arrival' in df.columns and 'expected_arrival' in df.columns:
            df['aimed_arrival'] = pd.to_datetime(df['aimed_arrival'])
            df['expected_arrival'] = pd.to_datetime(df['expected_arrival'])
            df['delay_minutes'] = (df['expected_arrival'] - df['aimed_arrival']).dt.total_seconds() / 60
        
        return df
    
    def _add_lag_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add lagged delay features"""
        if 'delay_minutes' not in df.columns or 'route_id' not in df.columns:
            return df
        
        for hours in self.lag_hours:
            col_name = f'delay_lag_{hours}h'
            df[col_name] = df.groupby('route_id')['delay_minutes'].shift(
                freq=f'{hours}H'
            )
        
        # Rolling statistics
        for window in [3, 6, 12]:
            df[f'delay_rolling_mean_{window}h'] = df.groupby('route_id')['delay_minutes'].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )
            df[f'delay_rolling_std_{window}h'] = df.groupby('route_id')['delay_minutes'].transform(
                lambda x: x.rolling(window=window, min_periods=1).std()
            )
        
        return df
    
    def _add_route_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add route-specific features"""
        if 'route_id' not in df.columns:
            return df
        
        # Average delay by route
        route_avg_delay = df.groupby('route_id')['delay_minutes'].mean()
        df['route_avg_delay'] = df['route_id'].map(route_avg_delay)
        
        # Route variance
        route_delay_std = df.groupby('route_id')['delay_minutes'].std()
        df['route_delay_std'] = df['route_id'].map(route_delay_std)
        
        return df
    
    def _add_weather_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add weather features (placeholder)"""
        # TODO: Integrate with weather API
        # For now, add placeholder columns
        df['temperature'] = np.nan
        df['precipitation'] = np.nan
        df['is_rainy'] = 0
        
        logger.warning("Weather features are placeholders - integrate weather API")
        return df
    
    def _add_event_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add special event features (placeholder)"""
        # TODO: Integrate with SF events calendar
        df['is_holiday'] = 0
        df['nearby_event'] = 0
        
        logger.warning("Event features are placeholders - integrate events calendar")
        return df
    
    def get_feature_names(self) -> List[str]:
        """Get list of all feature names"""
        base_features = [
            'hour', 'day_of_week', 'day_of_month', 'month',
            'is_weekend', 'is_morning_peak', 'is_evening_peak', 'is_peak_hour',
            'hour_sin', 'hour_cos', 'dow_sin', 'dow_cos'
        ]
        
        lag_features = [f'delay_lag_{h}h' for h in self.lag_hours]
        
        rolling_features = []
        for window in [3, 6, 12]:
            rolling_features.extend([
                f'delay_rolling_mean_{window}h',
                f'delay_rolling_std_{window}h'
            ])
        
        route_features = ['route_avg_delay', 'route_delay_std']
        
        return base_features + lag_features + rolling_features + route_features
