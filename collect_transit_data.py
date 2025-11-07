#!/usr/bin/env python3
"""
Transit Data Collection Script

Continuously fetches real-time transit data from 511 SF Bay API and stores it locally.
This builds up the historical dataset needed for model training.
"""

import os
import sys
import yaml
import json
import logging
from datetime import datetime
from pathlib import Path
import time
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import TransitDataFetcher

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/data_collection.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def load_config(config_path: str = "config/config.yaml") -> dict:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        sys.exit(1)


def save_data_to_file(data: pd.DataFrame, data_type: str, raw_dir: Path):
    """Save fetched data to a timestamped JSON file"""
    if data.empty:
        logger.warning(f"No {data_type} data to save")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{data_type}_{timestamp}.json"
    filepath = raw_dir / filename

    try:
        # Convert DataFrame to JSON format
        data_dict = data.to_dict(orient='records')

        # Save to file
        with open(filepath, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'data_type': data_type,
                'count': len(data_dict),
                'data': data_dict
            }, f, indent=2)

        logger.info(f"Saved {len(data)} {data_type} records to {filename}")
    except Exception as e:
        logger.error(f"Failed to save data: {e}")


def collect_vehicle_positions(fetcher: TransitDataFetcher, raw_dir: Path):
    """Fetch and save current vehicle positions"""
    logger.info("Fetching vehicle positions...")
    vehicles = fetcher.fetch_vehicle_positions(operator="SF")

    if not vehicles.empty:
        save_data_to_file(vehicles, "vehicle_positions", raw_dir)
        logger.info(f"Collected {len(vehicles)} vehicle positions")
    else:
        logger.warning("No vehicle data retrieved")

    return vehicles


def collect_stop_predictions(fetcher: TransitDataFetcher, raw_dir: Path, sample_stops: list):
    """Fetch and save stop predictions for sample stops"""
    all_predictions = []

    for stop_id in sample_stops:
        logger.info(f"Fetching predictions for stop {stop_id}...")
        predictions = fetcher.fetch_stop_monitoring(stop_id)

        if not predictions.empty:
            all_predictions.append(predictions)
            logger.info(f"Collected {len(predictions)} predictions for stop {stop_id}")

    if all_predictions:
        combined = pd.concat(all_predictions, ignore_index=True)
        save_data_to_file(combined, "stop_predictions", raw_dir)
        logger.info(f"Total predictions collected: {len(combined)}")
        return combined
    else:
        logger.warning("No stop prediction data retrieved")
        return pd.DataFrame()


def main():
    """Main data collection loop"""
    logger.info("=" * 60)
    logger.info("Starting SF Transit Data Collection")
    logger.info("=" * 60)

    # Load configuration
    config = load_config()
    api_key = config['api_keys']['transit_511']

    if api_key == "YOUR_511_API_KEY_HERE":
        logger.error("Please set your 511 API key in config/config.yaml")
        sys.exit(1)

    # Setup directories
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Initialize data fetcher
    base_url = config['endpoints']['transit_511_base']
    fetcher = TransitDataFetcher(api_key=api_key, base_url=base_url)

    # Sample stops to monitor (major Muni stops)
    # These are example stop codes - you can expand this list
    sample_stops = [
        "13690",  # Powell St Station
        "15184",  # Montgomery St Station
        "17217",  # Civic Center Station
    ]

    # Get update interval from config
    update_interval = config['data_collection']['transit_update_interval_seconds']

    logger.info(f"Configuration loaded:")
    logger.info(f"  - Update interval: {update_interval} seconds")
    logger.info(f"  - Monitoring {len(sample_stops)} sample stops")
    logger.info(f"  - Data directory: {raw_dir.absolute()}")

    # Data collection loop
    collection_count = 0
    try:
        while True:
            collection_count += 1
            logger.info(f"\n--- Collection cycle {collection_count} ---")

            # Collect vehicle positions
            vehicles = collect_vehicle_positions(fetcher, raw_dir)

            # Collect stop predictions
            predictions = collect_stop_predictions(fetcher, raw_dir, sample_stops)

            # Summary
            logger.info(f"Cycle {collection_count} complete:")
            logger.info(f"  - Vehicles: {len(vehicles) if not vehicles.empty else 0}")
            logger.info(f"  - Predictions: {len(predictions) if not predictions.empty else 0}")
            logger.info(f"  - Next collection in {update_interval} seconds")

            # Wait before next collection
            time.sleep(update_interval)

    except KeyboardInterrupt:
        logger.info("\n" + "=" * 60)
        logger.info("Data collection stopped by user")
        logger.info(f"Total collections: {collection_count}")
        logger.info("=" * 60)
    except Exception as e:
        logger.error(f"Error in collection loop: {e}", exc_info=True)
    finally:
        fetcher.close()


if __name__ == "__main__":
    main()
