#!/usr/bin/env python3
"""
Mock Transit Data Generator

Creates realistic sample transit data for testing without API access.
Simulates real 511 SF Bay API responses.
"""

import json
import pandas as pd
from datetime import datetime, timedelta
import random
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_mock_vehicle_positions(num_vehicles=50):
    """Generate mock vehicle position data"""

    # SF Muni route samples
    routes = ["1", "5", "14", "22", "38", "N", "K", "L", "M", "T"]

    # SF geographic bounds
    lat_min, lat_max = 37.7, 37.8
    lon_min, lon_max = -122.5, -122.4

    vehicles = []
    timestamp = datetime.now()

    for i in range(num_vehicles):
        vehicle = {
            "vehicle_id": f"MUNI_{random.randint(1000, 9999)}",
            "route_id": random.choice(routes),
            "timestamp": timestamp.isoformat(),
            "latitude": random.uniform(lat_min, lat_max),
            "longitude": random.uniform(lon_min, lon_max),
            "bearing": random.uniform(0, 360),
            "delay_seconds": random.randint(-120, 600),  # -2 min to +10 min delay
            "next_stop_id": f"{random.randint(10000, 20000)}",
            "occupancy": random.choice(["EMPTY", "MANY_SEATS_AVAILABLE", "FEW_SEATS_AVAILABLE", "STANDING_ROOM_ONLY", "FULL"])
        }
        vehicles.append(vehicle)

    return pd.DataFrame(vehicles)


def generate_mock_stop_predictions(stop_ids, num_predictions_per_stop=5):
    """Generate mock stop prediction data"""

    routes = ["1", "5", "14", "22", "38", "N", "K", "L", "M", "T"]
    predictions = []

    for stop_id in stop_ids:
        for _ in range(num_predictions_per_stop):
            now = datetime.now()
            aimed_arrival = now + timedelta(minutes=random.randint(2, 20))
            delay = random.randint(-2, 8)  # -2 to +8 minutes
            expected_arrival = aimed_arrival + timedelta(minutes=delay)

            prediction = {
                "stop_id": stop_id,
                "route_id": random.choice(routes),
                "vehicle_id": f"MUNI_{random.randint(1000, 9999)}",
                "aimed_arrival": aimed_arrival.isoformat(),
                "expected_arrival": expected_arrival.isoformat(),
                "timestamp": now.isoformat()
            }
            predictions.append(prediction)

    return pd.DataFrame(predictions)


def save_mock_data(data: pd.DataFrame, data_type: str, raw_dir: Path):
    """Save mock data in the same format as real API data"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{data_type}_{timestamp}_MOCK.json"
    filepath = raw_dir / filename

    data_dict = data.to_dict(orient='records')

    with open(filepath, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'data_type': data_type,
            'count': len(data_dict),
            'source': 'MOCK_DATA_GENERATOR',
            'data': data_dict
        }, f, indent=2)

    logger.info(f"✓ Saved {len(data)} mock {data_type} records to {filename}")
    return filepath


def main():
    """Generate mock data for testing"""

    logger.info("=" * 60)
    logger.info("Mock Transit Data Generator")
    logger.info("=" * 60)
    logger.info("\nGenerating realistic sample data for testing...\n")

    # Setup directory
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Generate vehicle positions
    logger.info("Generating vehicle positions...")
    vehicles = generate_mock_vehicle_positions(num_vehicles=75)
    vehicle_file = save_mock_data(vehicles, "vehicle_positions", raw_dir)

    logger.info(f"\nSample vehicle data:")
    logger.info(vehicles.head(3).to_string())

    # Generate stop predictions
    logger.info("\nGenerating stop predictions...")
    sample_stops = ["13690", "15184", "17217"]
    predictions = generate_mock_stop_predictions(sample_stops, num_predictions_per_stop=8)
    prediction_file = save_mock_data(predictions, "stop_predictions", raw_dir)

    logger.info(f"\nSample prediction data:")
    logger.info(predictions.head(3).to_string())

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Mock Data Generation Complete!")
    logger.info("=" * 60)
    logger.info(f"\nGenerated:")
    logger.info(f"  - {len(vehicles)} vehicle positions")
    logger.info(f"  - {len(predictions)} stop predictions")
    logger.info(f"\nFiles saved to: {raw_dir.absolute()}")
    logger.info(f"  - {vehicle_file.name}")
    logger.info(f"  - {prediction_file.name}")
    logger.info("\nYou can now test:")
    logger.info("  - Data loading and processing")
    logger.info("  - Feature engineering")
    logger.info("  - ML model training")
    logger.info("  - Visualization and analysis")
    logger.info("\n💡 Tip: Run this script multiple times to generate more data samples!")


if __name__ == "__main__":
    main()
