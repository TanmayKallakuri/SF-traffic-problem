#!/usr/bin/env python3
"""
WhatsApp Bot Prototype

Simulates how the messaging bot would work (without actual WhatsApp connection)
"""

import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import random

class TransitBot:
    """Prototype of SF Transit Chatbot"""

    def __init__(self):
        # Load our processed data
        data_path = Path("data/processed/vehicles_processed.csv")
        if data_path.exists():
            self.data = pd.read_csv(data_path)
        else:
            self.data = None

    def get_delay_prediction(self, route_id):
        """Predict delay for a route using our ML data"""
        if self.data is None or route_id not in self.data['route_id'].values:
            return random.uniform(2, 6)  # Default estimate

        # Get average delay for this route
        route_data = self.data[self.data['route_id'] == route_id]
        avg_delay = route_data['delay_minutes'].mean()
        return round(avg_delay, 1)

    def format_transit_response(self, destination):
        """Format a nice response like WhatsApp would show"""

        # Simulate route options
        routes = ['38', '1', 'N', 'K']
        selected_route = random.choice(routes)

        predicted_delay = self.get_delay_prediction(selected_route)
        base_time = 8
        total_time = base_time + predicted_delay

        response = f"""
🚌 SF Transit Assistant
━━━━━━━━━━━━━━━━━━━
📍 To: {destination}

🏆 RECOMMENDED ROUTE

Route {selected_route} - Geary Blvd
━━━━━━━━━━━━━━━━━━━
🚏 Nearest stop: 0.2 miles
🚶 Walk time: 4 mins

⏰ Next bus: 6 mins
⚠️ Predicted delay: +{predicted_delay:.1f} mins
🕐 Total time: ~{total_time:.0f} mins

🗺️ Google Maps: https://maps.google.com/?q=Route+{selected_route}+SF

━━━━━━━━━━━━━━━━━━━
💡 Actions:
   1️⃣ Get walking directions
   2️⃣ Set arrival reminder
   3️⃣ See alternatives
   4️⃣ Compare with driving
━━━━━━━━━━━━━━━━━━━
"""
        return response

    def compare_options(self, destination):
        """Compare transit vs driving"""

        transit_delay = self.get_delay_prediction('38')
        transit_time = 15 + transit_delay

        response = f"""
🚗💭 Transit vs Driving Comparison
━━━━━━━━━━━━━━━━━━━
📍 To: {destination}

🚌 TRANSIT (Route 38)
━━━━━━━━━━━━━━━━━━━
⏱️ Time: {transit_time:.0f} mins
⚠️ Expected delay: +{transit_delay:.1f} mins
💰 Cost: $2.50
🌍 CO2: 0.5 kg
👍 Recommended!

🚗 DRIVING
━━━━━━━━━━━━━━━━━━━
⏱️ Drive: 12 mins
🅿️ Parking search: ~8 mins
💰 Cost: $15 (parking)
🌍 CO2: 3.2 kg
⚠️ Parking 55% full

━━━━━━━━━━━━━━━━━━━
💡 VERDICT: Take transit!
   ✅ Saves $12.50
   ✅ Similar arrival time
   ✅ More eco-friendly
━━━━━━━━━━━━━━━━━━━
"""
        return response

    def get_delay_alert(self, route_id):
        """Generate delay alert notification"""

        delay = self.get_delay_prediction(route_id)

        if delay > 5:
            severity = "⚠️ MAJOR DELAY"
            emoji = "🚨"
        else:
            severity = "⏰ Minor Delay"
            emoji = "⚡"

        response = f"""
{emoji} {severity}
━━━━━━━━━━━━━━━━━━━
Route {route_id} - Your usual route

Current delay: +{delay:.1f} minutes

🔍 ALTERNATIVES:
  • Route 1 California: +2 mins
  • BART Powell St: 10 min walk
  • Uber Pool: 8 mins, $6

Would you like directions to an alternative?
"""
        return response

    def get_google_maps_link(self, origin, destination, mode="transit"):
        """Generate Google Maps deeplink"""

        base_url = "https://www.google.com/maps/dir/?api=1"
        link = f"{base_url}&origin={origin}&destination={destination}&travelmode={mode}"

        return link


def demo():
    """Demo the bot functionality"""

    print("="*60)
    print("🤖 SF TRANSIT BOT - INTERACTIVE DEMO")
    print("="*60)
    print("\nThis simulates how the WhatsApp/Messenger bot would work!\n")

    bot = TransitBot()

    # Demo 1: Route query
    print("\n" + "="*60)
    print("📱 USER MESSAGE: 'I need to get to Powell St Station'")
    print("="*60)
    response = bot.format_transit_response("Powell St Station")
    print(response)

    print("\n" + "-"*60 + "\n")

    # Demo 2: Comparison
    print("\n" + "="*60)
    print("📱 USER MESSAGE: 'Should I drive to Mission District?'")
    print("="*60)
    response = bot.compare_options("Mission District")
    print(response)

    print("\n" + "-"*60 + "\n")

    # Demo 3: Delay alert
    print("\n" + "="*60)
    print("🔔 PROACTIVE NOTIFICATION (Bot sends automatically)")
    print("="*60)
    response = bot.get_delay_alert("38")
    print(response)

    # Demo 4: Google Maps integration
    print("\n" + "="*60)
    print("🗺️ GOOGLE MAPS INTEGRATION")
    print("="*60)

    origin = "Civic Center Station, SF"
    destination = "Ferry Building, SF"

    transit_link = bot.get_google_maps_link(origin, destination, "transit")
    driving_link = bot.get_google_maps_link(origin, destination, "driving")
    walking_link = bot.get_google_maps_link(origin, destination, "walking")

    print(f"\n📍 From: {origin}")
    print(f"📍 To: {destination}\n")
    print(f"🚌 Transit directions:\n   {transit_link}\n")
    print(f"🚗 Driving directions:\n   {driving_link}\n")
    print(f"🚶 Walking directions:\n   {walking_link}\n")

    # Summary
    print("\n" + "="*60)
    print("✨ MESSAGING BOT FEATURES DEMONSTRATED")
    print("="*60)
    print("""
    ✅ Real-time delay predictions (from ML model)
    ✅ Route recommendations with timing
    ✅ Transit vs Driving comparisons
    ✅ Proactive delay alerts
    ✅ Google Maps integration
    ✅ Interactive buttons/actions
    ✅ Rich formatting with emojis

    🚀 READY TO BUILD THE REAL BOT!

    Next Steps:
    1. Set up Twilio WhatsApp Business API
    2. Create Flask webhook server
    3. Connect to Google Maps API
    4. Deploy to cloud (Railway/Render)
    5. Launch to beta users!
    """)


if __name__ == "__main__":
    demo()
