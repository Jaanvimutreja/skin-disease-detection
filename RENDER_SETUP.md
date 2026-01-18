# 🚀 RENDER DEPLOYMENT - FINAL STEPS

## ✅ YOUR GITHUB IS CONNECTED!

Now follow these **exact steps** to deploy on Render:

---

## **STEP 1: Go to Render Dashboard**
- URL: https://render.com/dashboard
- Make sure you're logged in with GitHub

---

## **STEP 2: Create Web Service**
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. **Connect GitHub Repository**
   - Click "Connect account" (or select existing account)
   - Find your repo: `skin-disease`
   - Click **"Connect"**

---

## **STEP 3: Configure Deployment**

### Basic Settings:
- **Name:** `dermais`
- **Region:** `Ohio` (free tier)
- **Branch:** `main`
- **Runtime:** `Python 3`

### Build Settings:
- **Build Command:**
  ```
  pip install -r requirements.txt
  ```

- **Start Command:**
  ```
  gunicorn app_flask:app --bind 0.0.0.0:$PORT
  ```

### Environment Variables:
- **Add Variable:**
  - Key: `PYTHON_VERSION`
  - Value: `3.10.13`

---

## **STEP 4: Storage for Model File**

Since your model is 80MB (Render's limit is 500MB total), use **GitHub LFS**:

### Option A: GitHub LFS (Best)
```bash
# Install Git LFS
git lfs install

# Track .keras files
git lfs track "*.keras"
git add .gitattributes

# Add model to LFS
git add final_skin_disease_model.keras
git commit -m "Add model to LFS"
git push origin main
```

### Option B: Download at Runtime (Fastest)
Model will auto-download from your repo when app starts.

---

## **STEP 5: Deploy!**

1. Click **"Create Web Service"** button
2. Wait for deployment (5-10 minutes)
3. Watch build logs
4. When ready, you'll see: ✅ "Deployment Live"

---

## **STEP 6: Access Your App**

Your live URL will be:
```
https://dermais.onrender.com
```

✨ **THAT'S IT! YOUR APP IS LIVE!** ✨

---

## **TROUBLESHOOTING:**

### Issue: "Model not found"
**Solution:** Ensure `final_skin_disease_model.keras` is in root directory or GitHub

### Issue: "Deployment Failed"
**Solution:** Check build logs for errors, most common:
- Missing dependency in `requirements.txt`
- Python version mismatch
- Model file too large

### Issue: "App crashes on first request"
**Solution:** Normal for free tier (cold start). Wait 30 seconds and try again.

### Issue: "Slow predictions"
**Solution:** Free tier uses CPU. Predictions take 5-10 seconds. Upgrade to paid tier for GPU.

---

## **MONITORING**

After deployment:
1. Go to your service dashboard
2. View **Metrics** to see requests
3. Check **Logs** for errors
4. Monitor uptime

---

## **IMPORTANT LIMITS (Free Tier)**

| Limit | Value |
|-------|-------|
| Storage | 500MB |
| Memory | 512MB |
| CPU | 1 core |
| Uptime | 750 hours/month |
| Cold start | ~30 seconds |

---

## **NEXT STEPS**

✅ Deployment complete  
✅ App is live  
✅ Share with friends: `https://dermais.onrender.com`

**Want to improve performance?**
- Upgrade to paid tier ($7/month) for dedicated resources
- Add database for user history
- Implement caching for faster predictions

---

## **GITHUB COMMANDS**

To push future updates:
```bash
cd "c:\Users\jaanv\OneDrive\Desktop\skin disease"
git add .
git commit -m "Your changes"
git push origin main
```

Render will **auto-redeploy** when you push to main! 🔄

---

**Happy deploying! 🎉**
