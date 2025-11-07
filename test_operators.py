#!/usr/bin/env python3
"""
Test 511 API with operators endpoint (simpler test)
"""

import yaml
import requests
import json

# Load API key
with open('config/config.yaml') as f:
    config = yaml.safe_load(f)
api_key = config['api_keys']['transit_511']

print("=" * 70)
print("Testing 511 API with Operators Endpoint (Simpler Test)")
print("=" * 70)
print(f"\nAPI Key: {api_key[:10]}...{api_key[-4:]}\n")

# Test operators endpoint first (simpler, should work if key is valid)
print("Test 1: Operators List (Basic API test)")
print("-" * 70)
url = f"http://api.511.org/transit/operators?api_key={api_key}"
print(f"URL: {url[:50]}...")

try:
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print("✓ SUCCESS! API key is working!\n")
        data = response.json()

        # Show available operators
        if isinstance(data, list):
            print(f"Found {len(data)} transit operators:")
            for op in data[:10]:  # Show first 10
                if isinstance(op, dict):
                    print(f"  - {op.get('Id', 'N/A')}: {op.get('Name', 'N/A')}")
        else:
            print("Response structure:", list(data.keys()) if isinstance(data, dict) else type(data))

        # Save full response for inspection
        with open('operators_response.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\nFull response saved to: operators_response.json")

    elif response.status_code == 403:
        print("❌ 403 Forbidden")
        print(f"Response: {response.text}")
    else:
        print(f"Unexpected status: {response.status_code}")
        print(f"Response: {response.text[:200]}")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)

# Test 2: Try VehicleMonitoring with format parameter
print("\nTest 2: VehicleMonitoring with explicit format")
print("-" * 70)
url2 = f"http://api.511.org/transit/VehicleMonitoring?api_key={api_key}&agency=SF&format=json"
print(f"URL: {url2[:50]}...")

try:
    response = requests.get(url2, timeout=10)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print("✓ SUCCESS!")
        data = response.json()
        print("Response keys:", list(data.keys()) if isinstance(data, dict) else "Not a dict")
    elif response.status_code == 403:
        print("❌ 403 Forbidden")
        print(f"Response: {response.text}")
    else:
        print(f"Response: {response.text[:200]}")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("Next Steps:")
print("=" * 70)
print("1. If Test 1 succeeds: API key is valid, VehicleMonitoring might have restrictions")
print("2. If Test 1 fails: API key needs activation or is invalid")
print("3. Check operators_response.json for valid agency codes")
print("=" * 70)
