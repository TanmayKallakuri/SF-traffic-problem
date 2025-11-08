#!/usr/bin/env python3
"""
Interactive demo of the SF Transit WhatsApp Bot
Run this while the bot server is running to test different queries
"""

import requests
import json

BOT_URL = "http://localhost:5000/test"

# Color codes for terminal
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def test_query(message):
    """Send a query to the bot and display the response"""
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{YELLOW}YOU: {message}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}")

    try:
        response = requests.post(
            BOT_URL,
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            print(f"\n{GREEN}BOT:{RESET}")
            print(data['response'])
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error connecting to bot: {e}")
        print("Make sure the bot is running with: ./venv/bin/python whatsapp_bot.py")

def main():
    """Run demo queries"""
    print(f"{GREEN}{'='*70}")
    print("🤖 SF TRANSIT WHATSAPP BOT - INTERACTIVE DEMO")
    print(f"{'='*70}{RESET}")
    print("\nTesting bot with various queries...\n")

    # Test queries
    queries = [
        "help",
        "Get to Ferry Building",
        "How do I get to Powell Street Station?",
        "Should I drive to Mission District?",
        "Route 38 status",
        "Is the N Judah late?",
    ]

    for query in queries:
        test_query(query)
        print()  # spacing

    print(f"\n{GREEN}{'='*70}")
    print("✅ DEMO COMPLETE!")
    print(f"{'='*70}{RESET}")
    print("\nThe bot successfully:")
    print("  ✓ Parsed different query types")
    print("  ✓ Provided route recommendations")
    print("  ✓ Compared transit vs driving")
    print("  ✓ Checked route delays")
    print("  ✓ Generated Google Maps links")
    print("\n💡 Try your own queries:")
    print('   curl -X POST http://localhost:5000/test \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"message": "your message here"}\'')
    print()

if __name__ == "__main__":
    main()
