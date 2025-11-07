# How to Get Your 511.org API Key

## Step-by-Step Registration

### 1. Go to the Token Request Page
Visit: **https://511.org/open-data/token**

### 2. Fill Out the Form
You'll see a form asking for:
- **Email Address** (your email)
- **Organization** (optional - can put "Personal Project" or your name)
- **Purpose** (e.g., "Building SF transit delay prediction ML model")

### 3. Submit the Form
Click "Request Token" or "Submit"

### 4. Check Your Email
- You should receive an email from 511.org
- **Check spam/junk folder** if you don't see it in inbox
- The email will contain:
  - A verification link (click this!)
  - Your API token/key (a UUID like: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

### 5. Verify Your Email
- **IMPORTANT**: Click the verification link in the email
- This activates your API key

### 6. Copy Your API Key
- Once verified, copy the API key from the email
- It will look like: `dfb7b5a1-604f-4cc2-8826-1f717c7eedce`

## Update the Configuration

Once you have your new API key:

```bash
# Edit the config file
nano config/config.yaml

# Or use any text editor to update line 6:
# Change: transit_511: "YOUR_OLD_KEY"
# To:     transit_511: "your-new-key-here"
```

## Test the New Key

```bash
# Activate virtual environment
source venv/bin/activate

# Test the API connection
python test_operators.py
```

You should see:
```
✓ SUCCESS! API key is working!
Found XX transit operators:
```

## Troubleshooting

If you still get 403 errors:

1. **Did you click the verification link in the email?**
   - This is REQUIRED to activate the key

2. **Check the email again**
   - Make sure you copied the entire UUID
   - No extra spaces or characters

3. **Wait a few minutes**
   - Sometimes activation takes 5-10 minutes

4. **Contact 511.org Support**
   - Email: 511sfbaydeveloperresources@googlegroups.com
   - Or use: developer@511.org

## Current API Key Status

Your current key: `dfb7b5a1-604f-4cc2-8826-1f717c7eedce`
Status: **Not working** (403 Forbidden on all endpoints)

This means you need to either:
- Register a new key (recommended)
- Contact 511.org if you registered this key and it should work
