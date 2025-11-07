#!/usr/bin/env python3
"""
Diagnostic script to test 511 API with different configurations
"""

import yaml
import requests

# Load API key
with open('config/config.yaml') as f:
    config = yaml.safe_load(f)
api_key = config['api_keys']['transit_511']

print("=" * 60)
print("511 SF Bay API Diagnostics")
print("=" * 60)
print(f"\nAPI Key: {api_key[:10]}...{api_key[-4:]}")
print()

# Test 1: HTTP endpoint
print("Test 1: HTTP endpoint")
url1 = f"http://api.511.org/transit/VehicleMonitoring?api_key={api_key}&agency=SF"
print(f"URL: {url1[:60]}...")
try:
    response = requests.get(url1, timeout=10, allow_redirects=False)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 301 or response.status_code == 302:
        print(f"Redirect to: {response.headers.get('Location', 'N/A')}")
    elif response.status_code == 403:
        print("❌ 403 Forbidden - API key might not be activated or lacks permissions")
    elif response.status_code == 200:
        print("✓ SUCCESS!")
        data = response.json()
        print(f"Response keys: {list(data.keys())}")
except Exception as e:
    print(f"Error: {e}")

print()

# Test 2: HTTPS endpoint
print("Test 2: HTTPS endpoint")
url2 = f"https://api.511.org/transit/VehicleMonitoring?api_key={api_key}&agency=SF"
print(f"URL: {url2[:60]}...")
try:
    response = requests.get(url2, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 403:
        print("❌ 403 Forbidden - API key might not be activated or lacks permissions")
        print("\nResponse body:")
        print(response.text[:500])
    elif response.status_code == 200:
        print("✓ SUCCESS!")
except Exception as e:
    print(f"Error: {e}")

print()
print("=" * 60)
print("Diagnosis Complete")
print("=" * 60)
print("\nIf both tests show 403 Forbidden, please:")
print("1. Check your email for a verification link from 511.org")
print("2. Verify your API key is activated at: https://511.org/open-data/token")
print("3. Make sure you've clicked the email verification link")
print()
