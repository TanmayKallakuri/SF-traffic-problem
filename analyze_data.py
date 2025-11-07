#!/usr/bin/env python3
"""
Data Analysis Script

Analyzes collected transit data (real or mock) and prepares it for ML modeling.
"""

import json
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def load_data_files(raw_dir: Path, data_type: str):
    """Load all data files of a specific type"""
    pattern = f"{data_type}_*.json"
    files = list(raw_dir.glob(pattern))

    all_data = []
    for file in files:
        with open(file, 'r') as f:
            content = json.load(f)
            all_data.extend(content['data'])

    return pd.DataFrame(all_data)


def analyze_vehicle_positions(df: pd.DataFrame):
    """Analyze vehicle position data"""
    print("\n" + "="*70)
    print("VEHICLE POSITIONS ANALYSIS")
    print("="*70)

    print(f"\nTotal records: {len(df)}")
    print(f"\nUnique vehicles: {df['vehicle_id'].nunique()}")
    print(f"Routes covered: {sorted(df['route_id'].unique())}")

    # Delay analysis
    if 'delay_seconds' in df.columns:
        df['delay_minutes'] = df['delay_seconds'] / 60

        print(f"\n--- Delay Statistics ---")
        print(f"Average delay: {df['delay_minutes'].mean():.2f} minutes")
        print(f"Median delay: {df['delay_minutes'].median():.2f} minutes")
        print(f"Max delay: {df['delay_minutes'].max():.2f} minutes")
        print(f"Min delay: {df['delay_minutes'].min():.2f} minutes (negative = early)")

        # Count by delay category
        df['delay_category'] = pd.cut(
            df['delay_minutes'],
            bins=[-float('inf'), -1, 5, 10, float('inf')],
            labels=['Early', 'On-time', 'Minor delay', 'Major delay']
        )
        print(f"\n--- Delay Categories ---")
        print(df['delay_category'].value_counts().to_string())

    # Route statistics
    print(f"\n--- Vehicles by Route ---")
    print(df['route_id'].value_counts().head(10).to_string())

    return df


def analyze_stop_predictions(df: pd.DataFrame):
    """Analyze stop prediction data"""
    print("\n" + "="*70)
    print("STOP PREDICTIONS ANALYSIS")
    print("="*70)

    print(f"\nTotal predictions: {len(df)}")
    print(f"Unique stops: {df['stop_id'].nunique()}")
    print(f"Routes: {sorted(df['route_id'].unique())}")

    # Calculate actual delay from aimed vs expected arrival
    if 'aimed_arrival' in df.columns and 'expected_arrival' in df.columns:
        df['aimed_arrival_dt'] = pd.to_datetime(df['aimed_arrival'])
        df['expected_arrival_dt'] = pd.to_datetime(df['expected_arrival'])
        df['delay_minutes'] = (df['expected_arrival_dt'] - df['aimed_arrival_dt']).dt.total_seconds() / 60

        print(f"\n--- Prediction Delay Statistics ---")
        print(f"Average predicted delay: {df['delay_minutes'].mean():.2f} minutes")
        print(f"Median predicted delay: {df['delay_minutes'].median():.2f} minutes")
        print(f"Max predicted delay: {df['delay_minutes'].max():.2f} minutes")

    print(f"\n--- Predictions by Stop ---")
    print(df['stop_id'].value_counts().to_string())

    return df


def main():
    """Main analysis function"""
    print("="*70)
    print("TRANSIT DATA ANALYSIS")
    print("="*70)

    raw_dir = Path("data/raw")

    # Load vehicle positions
    try:
        vehicles_df = load_data_files(raw_dir, "vehicle_positions")
        vehicles_df = analyze_vehicle_positions(vehicles_df)

        # Save processed data
        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        vehicles_df.to_csv(processed_dir / "vehicles_processed.csv", index=False)
        print(f"\n✓ Processed vehicle data saved to: {processed_dir / 'vehicles_processed.csv'}")

    except Exception as e:
        print(f"\n⚠ No vehicle position data found: {e}")

    # Load stop predictions
    try:
        predictions_df = load_data_files(raw_dir, "stop_predictions")
        predictions_df = analyze_stop_predictions(predictions_df)

        # Save processed data
        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        predictions_df.to_csv(processed_dir / "predictions_processed.csv", index=False)
        print(f"\n✓ Processed prediction data saved to: {processed_dir / 'predictions_processed.csv'}")

    except Exception as e:
        print(f"\n⚠ No stop prediction data found: {e}")

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print("\n📊 Next steps:")
    print("  1. Generate more data: ./venv/bin/python generate_mock_data.py")
    print("  2. Build ML model: Ready to start feature engineering")
    print("  3. Visualize data: Check data/processed/ folder")
    print("\n💡 When you get a working API key, replace mock data with real data!")


if __name__ == "__main__":
    main()
