# 🤖 SF Transit WhatsApp Bot - Setup Guide

Complete guide to deploying and running your WhatsApp transit assistant bot!

---

## 📋 Prerequisites

Before you begin, you'll need:

1. **Twilio Account** (free tier available)
2. **Google Maps API Key** (free tier: $200 credit/month)
3. **Cloud Hosting** (Railway, Render, or Heroku - all have free tiers)
4. Basic familiarity with terminal/command line

**Estimated setup time:** 30-45 minutes

---

## 🔑 Step 1: Get Twilio WhatsApp Access

### 1.1 Create Twilio Account

1. Go to [twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Sign up for a free account
3. Verify your email and phone number

### 1.2 Access WhatsApp Sandbox

Twilio provides a WhatsApp sandbox for testing:

1. In Twilio Console, go to **Messaging → Try it out → Send a WhatsApp message**
2. You'll see a number like `+1 415 523 8886`
3. You'll get a unique code like `join <your-code>`
4. **On your phone:** Send a WhatsApp message to the Twilio number with that code
5. You should receive a confirmation message!

### 1.3 Get Your Credentials

In Twilio Console, find these values:

```
Account SID: ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Auth Token: [click to reveal]
WhatsApp Number: whatsapp:+14155238886
```

**Save these!** You'll need them in Step 3.

---

## 🗺️ Step 2: Get Google Maps API Key

### 2.1 Create Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project: "SF Transit Bot"
3. Enable billing (required, but $200/month free credit covers testing)

### 2.2 Enable APIs

Enable these APIs in your project:

- **Directions API** (for route calculations)
- **Geocoding API** (for address lookups)
- **Maps JavaScript API** (for map links)

Navigate to: **APIs & Services → Enable APIs and Services**

### 2.3 Create API Key

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → API Key**
3. Copy your key: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

### 2.4 Restrict Your Key (Important!)

1. Click **Edit API Key**
2. Under **Application restrictions**, select **HTTP referrers**
3. Add your deployment URL when you have it
4. Under **API restrictions**, select **Restrict key** and choose only the 3 APIs above

**Save your API key!** You'll need it in Step 3.

---

## 🚀 Step 3: Deploy to Cloud

Choose one of these platforms:

### Option A: Railway (Recommended)

**Why Railway?** Easiest setup, great free tier, automatic HTTPS.

1. **Sign up:** [railway.app](https://railway.app)
2. **Create new project:** Click "New Project → Deploy from GitHub repo"
3. **Connect repo:** Authorize GitHub and select your SF-traffic-problem repo
4. **Add environment variables:**
   - Click your service → Variables → Add variables
   - Add these:
     ```
     TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
     TWILIO_AUTH_TOKEN=your_auth_token_here
     TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
     GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
     FLASK_ENV=production
     FLASK_DEBUG=False
     ```
5. **Deploy:** Railway will automatically build and deploy!
6. **Get your URL:** Settings → Generate Domain
   - You'll get: `https://your-bot.railway.app`

### Option B: Render

1. **Sign up:** [render.com](https://render.com)
2. **New Web Service:** Dashboard → New → Web Service
3. **Connect repo:** Select your GitHub repo
4. **Configure:**
   - Environment: Docker
   - Use `render.yaml` blueprint
5. **Add environment variables** (same as Railway)
6. **Deploy:** Render will build from Dockerfile
7. **Get your URL:** `https://your-bot.onrender.com`

### Option C: Heroku

1. **Install Heroku CLI:** [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
2. **Login and create app:**
   ```bash
   heroku login
   heroku create sf-transit-bot
   ```
3. **Set environment variables:**
   ```bash
   heroku config:set TWILIO_ACCOUNT_SID=ACxxxxxx...
   heroku config:set TWILIO_AUTH_TOKEN=your_token
   heroku config:set TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   heroku config:set GOOGLE_MAPS_API_KEY=AIzaSyxxxxxx...
   ```
4. **Deploy:**
   ```bash
   git push heroku main
   ```

---

## 🔗 Step 4: Connect Twilio Webhook

Now connect your deployed bot to Twilio:

1. **Copy your bot URL:**
   - Railway: `https://your-bot.railway.app`
   - Render: `https://your-bot.onrender.com`
   - Heroku: `https://sf-transit-bot.herokuapp.com`

2. **Configure Twilio webhook:**
   - Go to Twilio Console → Messaging → Settings → WhatsApp Sandbox Settings
   - Under **"When a message comes in":**
     - Paste: `https://your-bot.railway.app/webhook/whatsapp`
     - Method: POST
   - Under **"Status callback URL":**
     - Paste: `https://your-bot.railway.app/webhook/status`
   - Click **Save**

---

## ✅ Step 5: Test Your Bot!

### 5.1 Check Health

Visit your bot URL in a browser:
```
https://your-bot.railway.app/
```

You should see:
```json
{
  "status": "online",
  "service": "SF Transit WhatsApp Bot",
  "twilio_configured": true,
  "gmaps_configured": true
}
```

### 5.2 Send Test Messages

On WhatsApp, send messages to your Twilio number:

**Test 1: Help**
```
help
```
Expected: Help menu with all bot commands

**Test 2: Route Query**
```
Get to Ferry Building
```
Expected: Route recommendation with predicted delays

**Test 3: Comparison**
```
Should I drive to Mission?
```
Expected: Transit vs driving comparison

**Test 4: Delay Check**
```
Route 38 status
```
Expected: Current delay prediction for Route 38

---

## 🐛 Troubleshooting

### Bot not responding?

1. **Check webhook URL:**
   - Twilio Console → WhatsApp Sandbox Settings
   - Verify URL is correct and includes `/webhook/whatsapp`

2. **Check logs:**
   - Railway: Click service → Deployments → View logs
   - Render: Dashboard → your service → Logs
   - Heroku: `heroku logs --tail`

3. **Check environment variables:**
   - All 4 required variables set?
   - No typos in keys?

### "Access denied" errors?

- Check your Google Maps API key is enabled for the right APIs
- Verify API key restrictions aren't too strict

### Bot responds but with errors?

- Check if mock data files exist in `data/processed/`
- Run locally first to debug (see Step 6)

---

## 💻 Step 6: Run Locally (Optional)

For development and testing:

### 6.1 Install Dependencies

```bash
# Navigate to project
cd SF-traffic-problem

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install bot dependencies
pip install -r requirements-bot.txt
```

### 6.2 Create .env File

```bash
# Copy example
cp .env.example .env

# Edit with your values
nano .env  # or use any text editor
```

Add your actual credentials:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

### 6.3 Run the Bot

```bash
python whatsapp_bot.py
```

You should see:
```
============================================================
🚀 Starting SF Transit WhatsApp Bot
============================================================
Port: 5000
Twilio configured: True
Google Maps configured: True
Data loaded: True
============================================================
* Running on http://0.0.0.0:5000
```

### 6.4 Expose with ngrok (for Twilio)

Twilio needs a public URL. Use ngrok:

```bash
# Install ngrok: https://ngrok.com/download
ngrok http 5000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`) and use it in Twilio webhook settings:
```
https://abc123.ngrok.io/webhook/whatsapp
```

### 6.5 Test Endpoint

Open browser and test:
```
http://localhost:5000/test
```

Or use curl:
```bash
curl -X POST http://localhost:5000/test \
  -H "Content-Type: application/json" \
  -d '{"message": "Get to Ferry Building"}'
```

---

## 📊 Monitoring & Maintenance

### Check Bot Status

Visit your bot's health endpoint anytime:
```
https://your-bot.railway.app/
```

### View Logs

- **Railway:** Dashboard → Service → Logs tab
- **Render:** Dashboard → Service → Logs
- **Heroku:** `heroku logs --tail`

### Update Bot

Push changes to GitHub, and Railway/Render will auto-deploy:

```bash
git add .
git commit -m "Update bot feature"
git push origin main
```

---

## 🎯 Next Steps

Your bot is now live! Consider:

1. **Add more routes:** Update route list in `whatsapp_bot.py:132`
2. **Improve NLP:** Use spaCy or Rasa for better intent recognition
3. **Add real-time data:** Replace mock data with actual 511 API when key works
4. **Set up alerts:** Implement proactive delay notifications
5. **Add more features:**
   - Save favorite locations
   - Multi-language support
   - Voice message responses
   - Calendar integration

---

## 📞 Support

### Resources

- **Twilio WhatsApp Docs:** [twilio.com/docs/whatsapp](https://www.twilio.com/docs/whatsapp)
- **Google Maps API Docs:** [developers.google.com/maps](https://developers.google.com/maps)
- **Flask Documentation:** [flask.palletsprojects.com](https://flask.palletsprojects.com)

### Common Issues

**Issue:** WhatsApp message says "join [code]" but bot doesn't respond
- **Fix:** You need to join the sandbox first! Send that exact message to the Twilio number

**Issue:** Bot responds but delays are always the same
- **Fix:** This is expected with mock data. Delays are randomly generated or from cached data

**Issue:** Google Maps links don't work
- **Fix:** Check that Google Maps API key is correctly set in environment variables

---

## 💡 Tips for Best Experience

1. **Warm up the bot:** First message might be slow (free tier cold starts)
2. **Be specific:** "Get to Powell St Station" works better than just "Powell"
3. **Use natural language:** Bot understands conversational queries
4. **Try comparisons:** "Should I drive or take transit?" works great
5. **Check help:** Send "help" to see all available commands

---

## 🎉 You're All Set!

Your SF Transit WhatsApp Bot is now live and helping commuters!

Share it with friends and start collecting user feedback. Remember:
- Twilio free tier: 1,000 messages/month
- Google Maps free tier: $200 credit/month
- Perfect for testing and small user base

**Ready to scale?** When you have real users, consider:
- Upgrading to Twilio's paid plan for production WhatsApp number
- Adding Redis for session management
- Implementing caching to reduce API calls
- Setting up monitoring (Sentry, LogRocket)

Happy bot building! 🚀🚌
