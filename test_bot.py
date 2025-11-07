#!/usr/bin/env python3
"""
Quick test of WhatsApp bot functionality
Tests the bot logic without requiring Twilio/Google Maps API keys
"""

import sys
sys.path.insert(0, '.')

from whatsapp_bot import TransitBot

def test_bot():
    """Test bot functionality"""
    print("="*70)
    print("TESTING SF TRANSIT WHATSAPP BOT")
    print("="*70)

    # Initialize bot
    print("\n1. Initializing bot...")
    bot = TransitBot()
    print("   ✓ Bot initialized")

    # Test help intent
    print("\n2. Testing HELP intent...")
    response = bot.process_message("help", "test_user")
    assert "SF Transit Assistant" in response
    assert "WHAT I CAN DO" in response
    print("   ✓ Help response generated")
    print(f"   Response length: {len(response)} chars")

    # Test route query
    print("\n3. Testing ROUTE QUERY intent...")
    response = bot.process_message("Get to Ferry Building", "test_user")
    assert "Ferry Building" in response
    assert "RECOMMENDED ROUTE" in response
    assert "google.com/maps" in response
    print("   ✓ Route query response generated")
    print(f"   Response length: {len(response)} chars")

    # Test comparison
    print("\n4. Testing COMPARISON intent...")
    response = bot.process_message("Should I drive to Mission?", "test_user")
    assert "Transit vs Driving" in response
    assert "TRANSIT" in response
    assert "DRIVING" in response
    print("   ✓ Comparison response generated")
    print(f"   Response length: {len(response)} chars")

    # Test delay check
    print("\n5. Testing DELAY CHECK intent...")
    response = bot.process_message("Route 38 status", "test_user")
    assert "delay" in response.lower()
    print("   ✓ Delay check response generated")
    print(f"   Response length: {len(response)} chars")

    # Test intent parsing
    print("\n6. Testing INTENT PARSING...")
    test_cases = [
        ("help", "help"),
        ("Get to Ferry Building", "route_query"),
        ("should i drive", "comparison"),
        ("is the bus late", "delay_check"),
    ]

    for message, expected_intent in test_cases:
        intent = bot.parse_intent(message)
        assert intent == expected_intent, f"Expected {expected_intent}, got {intent}"
        print(f"   ✓ '{message}' → {intent}")

    # Test destination extraction
    print("\n7. Testing DESTINATION EXTRACTION...")
    test_messages = [
        ("Get to Ferry Building", "Ferry Building"),
        ("How do I go to Powell St", "Powell St"),
        ("route to Mission District", "Mission District"),
    ]

    for message, expected_dest in test_messages:
        dest = bot.extract_destination(message)
        assert expected_dest in dest
        print(f"   ✓ '{message}' → '{dest}'")

    # Test delay prediction
    print("\n8. Testing DELAY PREDICTION...")
    routes = ['1', '38', 'N', 'K']
    for route in routes:
        delay = bot.get_delay_prediction(route)
        assert isinstance(delay, (int, float))
        assert delay >= 0
        print(f"   ✓ Route {route}: {delay:.1f} min delay")

    # Test Google Maps link generation
    print("\n9. Testing GOOGLE MAPS LINKS...")
    link = bot.get_maps_link(None, "Ferry Building", "transit")
    assert "google.com/maps" in link
    assert "Ferry Building" in link
    assert "travelmode=transit" in link
    print(f"   ✓ Generated link: {link}")

    print("\n" + "="*70)
    print("ALL TESTS PASSED! ✅")
    print("="*70)
    print("\nBot is ready to deploy!")
    print("\nNext steps:")
    print("  1. Set up Twilio account (see BOT_SETUP_GUIDE.md)")
    print("  2. Get Google Maps API key")
    print("  3. Deploy to Railway/Render")
    print("  4. Configure webhooks")
    print("="*70)

if __name__ == "__main__":
    test_bot()
