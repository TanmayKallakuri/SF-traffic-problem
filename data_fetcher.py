"""
Transit Data Fetcher

Handles fetching and parsing data from 511 SF Bay Transit API (GTFS feeds)
"""

import httpx
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class TransitDataFetcher:
    """Fetches real-time and historical transit data from 511 API"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.511.org/transit"):
        """
        Initialize the transit data fetcher
        
        Args:
            api_key: 511 API key
            base_url: Base URL for 511 API
        """
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.Client(timeout=30.0)
        
    def fetch_vehicle_positions(self, operator: str = "SF") -> pd.DataFrame:
        """
        Fetch real-time vehicle positions for Muni buses
        
        Args:
            operator: Transit operator code (default: "SF" for Muni)
            
        Returns:
            DataFrame with vehicle positions and delays
        """
        try:
            url = f"{self.base_url}/VehicleMonitoring"
            params = {
                "api_key": self.api_key,
                "agency": operator,
                "format": "json"
            }
            
            response = self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            vehicles = self._parse_vehicle_positions(data)
            
            logger.info(f"Fetched {len(vehicles)} vehicle positions")
            return vehicles
            
        except Exception as e:
            logger.error(f"Error fetching vehicle positions: {e}")
            return pd.DataFrame()
    
    def fetch_stop_monitoring(
        self, 
        stop_id: str, 
        route_id: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch predictions for a specific stop
        
        Args:
            stop_id: Stop identifier
            route_id: Optional route filter
            
        Returns:
            DataFrame with stop predictions
        """
        try:
            url = f"{self.base_url}/StopMonitoring"
            params = {
                "api_key": self.api_key,
                "agency": "SF",
                "stopCode": stop_id,
                "format": "json"
            }
            
            response = self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            predictions = self._parse_stop_monitoring(data, route_id)
            
            logger.info(f"Fetched {len(predictions)} predictions for stop {stop_id}")
            return predictions
            
        except Exception as e:
            logger.error(f"Error fetching stop monitoring: {e}")
            return pd.DataFrame()
    
    def fetch_historical_data(
        self,
        start_date: datetime,
        end_date: datetime,
        route_ids: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Fetch historical transit performance data
        
        Args:
            start_date: Start of date range
            end_date: End of date range
            route_ids: Optional list of route IDs to filter
            
        Returns:
            DataFrame with historical transit data
        """
        # TODO: Implement historical data fetching
        # This may require using archived GTFS data or a different endpoint
        logger.warning("Historical data fetching not yet implemented")
        return pd.DataFrame()
    
    def _parse_vehicle_positions(self, data: Dict) -> pd.DataFrame:
        """Parse vehicle positions from API response"""
        vehicles = []
        
        try:
            service_delivery = data.get("Siri", {}).get("ServiceDelivery", {})
            vehicle_activities = service_delivery.get("VehicleMonitoringDelivery", [{}])[0].get("VehicleActivity", [])
            
            for activity in vehicle_activities:
                journey = activity.get("MonitoredVehicleJourney", {})
                
                vehicle = {
                    "vehicle_id": journey.get("VehicleRef"),
                    "route_id": journey.get("LineRef"),
                    "timestamp": journey.get("RecordedAtTime"),
                    "latitude": journey.get("VehicleLocation", {}).get("Latitude"),
                    "longitude": journey.get("VehicleLocation", {}).get("Longitude"),
                    "bearing": journey.get("Bearing"),
                    "delay_seconds": journey.get("Delay"),  # Delay in seconds
                    "next_stop_id": journey.get("MonitoredCall", {}).get("StopPointRef"),
                    "occupancy": journey.get("Occupancy")
                }
                vehicles.append(vehicle)
                
        except Exception as e:
            logger.error(f"Error parsing vehicle positions: {e}")
        
        return pd.DataFrame(vehicles)
    
    def _parse_stop_monitoring(self, data: Dict, route_filter: Optional[str]) -> pd.DataFrame:
        """Parse stop monitoring data from API response"""
        predictions = []
        
        try:
            service_delivery = data.get("Siri", {}).get("ServiceDelivery", {})
            stop_visits = service_delivery.get("StopMonitoringDelivery", [{}])[0].get("MonitoredStopVisit", [])
            
            for visit in stop_visits:
                journey = visit.get("MonitoredVehicleJourney", {})
                
                # Apply route filter if specified
                if route_filter and journey.get("LineRef") != route_filter:
                    continue
                
                prediction = {
                    "stop_id": visit.get("MonitoringRef"),
                    "route_id": journey.get("LineRef"),
                    "vehicle_id": journey.get("VehicleRef"),
                    "aimed_arrival": journey.get("MonitoredCall", {}).get("AimedArrivalTime"),
                    "expected_arrival": journey.get("MonitoredCall", {}).get("ExpectedArrivalTime"),
                    "timestamp": visit.get("RecordedAtTime")
                }
                predictions.append(prediction)
                
        except Exception as e:
            logger.error(f"Error parsing stop monitoring: {e}")
        
        return pd.DataFrame(predictions)
    
    def close(self):
        """Close the HTTP client"""
        self.client.close()
