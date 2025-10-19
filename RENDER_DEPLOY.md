# Deploy to Render.com - Step by Step Guide

## 🚀 Get Your Live App Link in 5 Minutes (100% FREE)

### Step 1: Sign Up for Render.com

1. Go to **https://render.com**
2. Click **"Get Started for Free"**
3. Sign in with your **GitHub account** (easier) or create an account

---

### Step 2: Create New Web Service

1. Once logged in, click the **"New +"** button (top right)
2. Select **"Web Service"**
3. You'll see a list of your GitHub repositories
4. Find and click **"Connect"** next to **GrievanceFilingService**

   *If you don't see it:*
   - Click "Configure account" to grant Render access to your repos
   - Select "All repositories" or just "GrievanceFilingService"
   - Save and return

---

### Step 3: Configure the Service (Auto-Configured!)

Render will automatically detect the `render.yaml` file and configure:

- ✅ **Name:** grievance-filing-service
- ✅ **Environment:** Python
- ✅ **Build Command:** `pip install -r requirements.txt`
- ✅ **Start Command:** `gunicorn app:app`
- ✅ **Python Version:** 3.11.0

**You don't need to change anything!**

---

### Step 4: Deploy!

1. Scroll down and click **"Create Web Service"**
2. Wait 2-4 minutes while Render:
   - Pulls your code from GitHub
   - Installs dependencies
   - Starts your app
3. Watch the deployment logs (you'll see progress)

---

### Step 5: Get Your Live Link! 🎉

Once deployment is complete (you'll see "Live" with a green dot), your app will be at:

**`https://grievance-filing-service-XXXX.onrender.com`**

(The XXXX will be a unique identifier assigned by Render)

---

## What Happens Next?

✅ **Your app is live** and accessible to anyone worldwide
✅ **Auto-deploys** whenever you push to GitHub
✅ **FREE tier** includes:
   - 750 hours/month (enough for hobby projects)
   - Automatic HTTPS/SSL
   - Custom domains (optional)
   - Database support

⚠️ **Note:** Free tier apps "sleep" after 15 minutes of inactivity. First request after sleeping takes ~30 seconds to wake up.

---

## Testing Your Live App

1. Visit your Render.com URL
2. Click **"Register"** to create an account
3. Fill out a test complaint
4. Upload documents
5. Share the link with others!

---

## Customize Your Domain (Optional)

### Add a Custom Domain:
1. In Render dashboard, go to your service
2. Click "Settings" → "Custom Domain"
3. Add your domain (e.g., `grievances.edmundbogen.com`)
4. Follow DNS setup instructions

---

## Environment Variables (Already Set)

Render automatically sets:
- `PORT` - Server port
- `SECRET_KEY` - Auto-generated secure key
- `PYTHON_VERSION` - 3.11.0

To add more:
1. Go to service settings
2. Click "Environment"
3. Add variables like:
   - `DATABASE_URL` (if using external database)
   - `MAIL_SERVER` (for email notifications)

---

## Troubleshooting

### Deployment Failed?
- Check the build logs in Render dashboard
- Verify all files are pushed to GitHub
- Ensure `requirements.txt` is present

### App Won't Load?
- Check the service logs in Render
- Verify the app shows "Live" status
- Try refreshing after 30 seconds (wake from sleep)

### Need a Database Upgrade?
- Free tier uses SQLite (file-based)
- For production, add a PostgreSQL database:
  - Click "New +" → "PostgreSQL"
  - Connect to your web service
  - Render auto-configures DATABASE_URL

---

## Monitoring Your App

In Render dashboard you can see:
- ✅ Deploy history
- ✅ Live logs
- ✅ Resource usage
- ✅ Request metrics

---

## Upgrade Options (If Needed)

**Free Tier:** Perfect for testing and demos
**Starter ($7/mo):** No sleep, faster, more resources
**Standard ($25/mo):** Production-ready with autoscaling

---

## Your App is Now Live! 🚀

Once deployed, anyone can:
- Register and create accounts
- File complaints
- Upload documents
- Track deadlines
- Learn about NAR Code of Ethics

**Share your live link with clients, colleagues, or the public!**

---

## Questions?

- Render Docs: https://render.com/docs
- GitHub Repo: https://github.com/edmundbogen/GrievanceFilingService
- Support: support@render.com
