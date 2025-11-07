#!/usr/bin/env python3
"""
Complete System Test

Demonstrates the full pipeline: data generation → analysis → visualization → predictions
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and show results"""
    print(f"\n{'='*70}")
    print(f"🔧 {description}")
    print(f"{'='*70}")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ SUCCESS")
        if result.stdout:
            print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
    else:
        print("❌ FAILED")
        print(result.stderr)

    return result.returncode == 0

def main():
    print("="*70)
    print("SF TRANSIT PREDICTION - COMPLETE SYSTEM TEST")
    print("="*70)
    print("\nTesting all components of the system...")

    # Test 1: Generate fresh mock data
    success = run_command(
        "./venv/bin/python generate_mock_data.py",
        "Step 1: Generate Mock Transit Data"
    )

    if not success:
        print("\n❌ Mock data generation failed!")
        sys.exit(1)

    # Test 2: Analyze data
    success = run_command(
        "./venv/bin/python analyze_data.py",
        "Step 2: Analyze Transit Data"
    )

    if not success:
        print("\n❌ Data analysis failed!")
        sys.exit(1)

    # Test 3: Create visualizations
    success = run_command(
        "./venv/bin/python visualize_data.py",
        "Step 3: Generate Visualizations"
    )

    if not success:
        print("\n❌ Visualization generation failed!")
        sys.exit(1)

    # Check outputs
    print(f"\n{'='*70}")
    print("📊 CHECKING OUTPUT FILES")
    print(f"{'='*70}")

    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    viz_dir = Path("visualizations")

    raw_files = list(raw_dir.glob("*.json"))
    processed_files = list(processed_dir.glob("*.csv"))
    viz_files = list(viz_dir.glob("*.png"))

    print(f"\n✓ Raw data files: {len(raw_files)}")
    print(f"✓ Processed CSV files: {len(processed_files)}")
    print(f"✓ Visualization charts: {len(viz_files)}")

    # Summary
    print(f"\n{'='*70}")
    print("🎉 SYSTEM TEST COMPLETE!")
    print(f"{'='*70}")
    print("\nAll components working successfully:")
    print("  ✅ Data Generation")
    print("  ✅ Data Analysis")
    print("  ✅ Visualizations")
    print("\nNext: Build ML model for delay predictions!")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
