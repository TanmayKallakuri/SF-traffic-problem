#!/usr/bin/env python3
"""
Quick test script to verify 511 API connection
"""

import sys
import yaml
import logging
from data_fetcher import TransitDataFetcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load config
    try:
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        sys.exit(1)

    api_key = config['api_keys']['transit_511']

    if api_key == "YOUR_511_API_KEY_HERE":
        logger.error("Please set your 511 API key in config/config.yaml first!")
        sys.exit(1)

    logger.info("Testing 511 SF Bay API connection...")
    logger.info(f"API Key: {api_key[:10]}..." if len(api_key) > 10 else "***")

    # Initialize fetcher
    fetcher = TransitDataFetcher(api_key=api_key)

    # Test vehicle positions
    logger.info("\nFetching vehicle positions for SF Muni...")
    vehicles = fetcher.fetch_vehicle_positions(operator="SF")

    if not vehicles.empty:
        logger.info(f"✓ SUCCESS! Retrieved {len(vehicles)} vehicles")
        logger.info("\nSample data:")
        logger.info(f"\nColumns: {list(vehicles.columns)}")
        logger.info(f"\n{vehicles.head(3)}")
    else:
        logger.warning("✗ No vehicle data received. Check your API key and permissions.")

    fetcher.close()
    logger.info("\nAPI connection test complete!")

if __name__ == "__main__":
    main()
