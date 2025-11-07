#!/usr/bin/env python3
"""
Transit Data Visualizations

Creates comprehensive visualizations of transit delay patterns.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
from datetime import datetime
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def load_all_data(raw_dir: Path, data_type: str):
    """Load all data files"""
    pattern = f"{data_type}_*.json"
    files = list(raw_dir.glob(pattern))

    all_data = []
    for file in files:
        with open(file, 'r') as f:
            content = json.load(f)
            all_data.extend(content['data'])

    return pd.DataFrame(all_data)


def create_delay_distribution_plot(df, output_path):
    """Create delay distribution histogram"""
    plt.figure(figsize=(12, 6))

    df['delay_minutes'] = df['delay_seconds'] / 60

    plt.subplot(1, 2, 1)
    plt.hist(df['delay_minutes'], bins=30, edgecolor='black', alpha=0.7)
    plt.axvline(df['delay_minutes'].mean(), color='red', linestyle='--',
                label=f'Mean: {df["delay_minutes"].mean():.2f} min')
    plt.axvline(df['delay_minutes'].median(), color='green', linestyle='--',
                label=f'Median: {df["delay_minutes"].median():.2f} min')
    plt.xlabel('Delay (minutes)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Transit Delays')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Box plot
    plt.subplot(1, 2, 2)
    plt.boxplot(df['delay_minutes'], vert=True)
    plt.ylabel('Delay (minutes)')
    plt.title('Delay Distribution (Box Plot)')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def create_route_delay_plot(df, output_path):
    """Create delay comparison by route"""
    plt.figure(figsize=(14, 6))

    df['delay_minutes'] = df['delay_seconds'] / 60

    # Sort routes by average delay
    route_delays = df.groupby('route_id')['delay_minutes'].mean().sort_values(ascending=False)

    plt.subplot(1, 2, 1)
    route_delays.plot(kind='barh', color='steelblue')
    plt.xlabel('Average Delay (minutes)')
    plt.ylabel('Route')
    plt.title('Average Delay by Route')
    plt.grid(True, alpha=0.3)

    # Violin plot
    plt.subplot(1, 2, 2)
    routes_sorted = route_delays.index.tolist()
    data_to_plot = [df[df['route_id'] == route]['delay_minutes'].values
                    for route in routes_sorted]

    plt.violinplot(data_to_plot, vert=False)
    plt.yticks(range(1, len(routes_sorted) + 1), routes_sorted)
    plt.xlabel('Delay (minutes)')
    plt.ylabel('Route')
    plt.title('Delay Distribution by Route (Violin Plot)')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def create_occupancy_plot(df, output_path):
    """Create vehicle occupancy analysis"""
    plt.figure(figsize=(12, 6))

    # Count by occupancy level
    occupancy_counts = df['occupancy'].value_counts()

    plt.subplot(1, 2, 1)
    occupancy_counts.plot(kind='bar', color='coral')
    plt.xlabel('Occupancy Level')
    plt.ylabel('Count')
    plt.title('Vehicle Occupancy Distribution')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3)

    # Pie chart
    plt.subplot(1, 2, 2)
    plt.pie(occupancy_counts.values, labels=occupancy_counts.index,
            autopct='%1.1f%%', startangle=90)
    plt.title('Occupancy Percentage')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def create_delay_heatmap(df, output_path):
    """Create heatmap of delays by route and category"""
    plt.figure(figsize=(10, 8))

    df['delay_minutes'] = df['delay_seconds'] / 60

    # Create delay categories
    df['delay_category'] = pd.cut(
        df['delay_minutes'],
        bins=[-float('inf'), 0, 2, 5, 10, float('inf')],
        labels=['Early', 'On-time (0-2)', 'Small (2-5)', 'Medium (5-10)', 'Large (>10)']
    )

    # Create pivot table
    heatmap_data = pd.crosstab(df['route_id'], df['delay_category'])

    sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd',
                cbar_kws={'label': 'Count'})
    plt.xlabel('Delay Category')
    plt.ylabel('Route')
    plt.title('Delay Frequency by Route and Category')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def create_location_scatter(df, output_path):
    """Create geographic scatter plot of vehicle positions"""
    plt.figure(figsize=(12, 10))

    df['delay_minutes'] = df['delay_seconds'] / 60

    # Create scatter plot colored by delay
    scatter = plt.scatter(df['longitude'], df['latitude'],
                         c=df['delay_minutes'], cmap='RdYlGn_r',
                         alpha=0.6, s=50, edgecolors='black', linewidth=0.5)

    plt.colorbar(scatter, label='Delay (minutes)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Vehicle Positions Colored by Delay\n(San Francisco Geographic Distribution)')
    plt.grid(True, alpha=0.3)

    # Add SF boundary reference
    plt.xlim(-122.52, -122.35)
    plt.ylim(37.68, 37.82)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def create_summary_statistics_plot(df, output_path):
    """Create summary statistics visualization"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    df['delay_minutes'] = df['delay_seconds'] / 60

    # 1. Route frequency
    route_counts = df['route_id'].value_counts()
    axes[0, 0].barh(route_counts.index, route_counts.values, color='skyblue')
    axes[0, 0].set_xlabel('Number of Records')
    axes[0, 0].set_ylabel('Route')
    axes[0, 0].set_title('Data Coverage by Route')
    axes[0, 0].grid(True, alpha=0.3)

    # 2. Delay over "time" (using record index as proxy)
    axes[0, 1].plot(df.index, df['delay_minutes'], alpha=0.5, linewidth=0.5)
    axes[0, 1].axhline(df['delay_minutes'].mean(), color='red',
                       linestyle='--', label='Mean')
    axes[0, 1].set_xlabel('Record Index')
    axes[0, 1].set_ylabel('Delay (minutes)')
    axes[0, 1].set_title('Delay Pattern Over Collection Period')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # 3. Delay by occupancy
    occupancy_order = ['EMPTY', 'MANY_SEATS_AVAILABLE', 'FEW_SEATS_AVAILABLE',
                       'STANDING_ROOM_ONLY', 'FULL']
    occupancy_data = []
    labels = []
    for occ in occupancy_order:
        if occ in df['occupancy'].values:
            occupancy_data.append(df[df['occupancy'] == occ]['delay_minutes'].values)
            labels.append(occ.replace('_', ' ').title())

    axes[1, 0].boxplot(occupancy_data, labels=labels)
    axes[1, 0].set_ylabel('Delay (minutes)')
    axes[1, 0].set_title('Delay vs Occupancy Level')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(True, alpha=0.3)

    # 4. Statistics summary table
    axes[1, 1].axis('off')
    stats_text = f"""
    DATASET SUMMARY

    Total Records: {len(df):,}
    Unique Vehicles: {df['vehicle_id'].nunique():,}
    Routes Covered: {df['route_id'].nunique()}

    DELAY STATISTICS
    Mean Delay: {df['delay_minutes'].mean():.2f} min
    Median Delay: {df['delay_minutes'].median():.2f} min
    Std Dev: {df['delay_minutes'].std():.2f} min
    Min Delay: {df['delay_minutes'].min():.2f} min
    Max Delay: {df['delay_minutes'].max():.2f} min

    ON-TIME PERFORMANCE
    Early: {(df['delay_minutes'] < 0).sum()} ({(df['delay_minutes'] < 0).sum()/len(df)*100:.1f}%)
    On-time: {((df['delay_minutes'] >= 0) & (df['delay_minutes'] <= 5)).sum()} ({((df['delay_minutes'] >= 0) & (df['delay_minutes'] <= 5)).sum()/len(df)*100:.1f}%)
    Delayed: {(df['delay_minutes'] > 5).sum()} ({(df['delay_minutes'] > 5).sum()/len(df)*100:.1f}%)
    """

    axes[1, 1].text(0.1, 0.5, stats_text, fontsize=10,
                    verticalalignment='center', fontfamily='monospace',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    axes[1, 1].set_title('Summary Statistics', fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def main():
    """Generate all visualizations"""
    print("=" * 70)
    print("TRANSIT DATA VISUALIZATION")
    print("=" * 70)
    print("\nLoading data...")

    raw_dir = Path("data/raw")
    viz_dir = Path("visualizations")
    viz_dir.mkdir(exist_ok=True)

    # Load vehicle data
    vehicles_df = load_all_data(raw_dir, "vehicle_positions")
    print(f"✓ Loaded {len(vehicles_df)} vehicle records")

    print("\nGenerating visualizations...")
    print("-" * 70)

    # Create visualizations
    create_delay_distribution_plot(vehicles_df, viz_dir / "1_delay_distribution.png")
    create_route_delay_plot(vehicles_df, viz_dir / "2_delay_by_route.png")
    create_occupancy_plot(vehicles_df, viz_dir / "3_occupancy_analysis.png")
    create_delay_heatmap(vehicles_df, viz_dir / "4_delay_heatmap.png")
    create_location_scatter(vehicles_df, viz_dir / "5_geographic_distribution.png")
    create_summary_statistics_plot(vehicles_df, viz_dir / "6_summary_dashboard.png")

    print("-" * 70)
    print("\n" + "=" * 70)
    print("VISUALIZATION COMPLETE!")
    print("=" * 70)
    print(f"\n📊 All visualizations saved to: {viz_dir.absolute()}/")
    print("\nGenerated files:")
    for viz_file in sorted(viz_dir.glob("*.png")):
        print(f"  - {viz_file.name}")
    print("\n💡 Tip: Open these PNG files to explore your transit data patterns!")


if __name__ == "__main__":
    main()
