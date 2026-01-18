# 🚀 DermAI - DEPLOYMENT GUIDE

## **Option 1: RENDER.COM (Recommended)**

### Why Render?
✅ Free tier: 750 hours/month  
✅ Auto-deploy from GitHub  
✅ Perfect for Python + TensorFlow  
✅ No credit card required  

### Steps:

1. **Push code to GitHub:**
```bash
git init
git add .
git commit -m "DermAI - Skin Disease Detection"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/skin-disease.git
git push -u origin main
```

2. **Create Render account:**
   - Go to https://render.com
   - Sign up with GitHub

3. **Deploy:**
   - Click "New +" → "Web Service"
   - Connect GitHub repo
   - Configure:
     - **Name:** `dermais`
     - **Runtime:** Python 3.10
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app_flask:app --bind 0.0.0.0:$PORT`
   - Click **Deploy**

4. **Access your app:**
   ```
   https://dermais.onrender.com
   ```

---

## **Option 2: RAILWAY.APP**

### Why Railway?
✅ $5/month free credit (usually enough)  
✅ Easy GitHub integration  
✅ Great for beginners  

### Steps:
1. Go to https://railway.app
2. Sign up with GitHub
3. New Project → Import from GitHub
4. Select repo → Deploy
5. Get URL from deployment info

---

## **Option 3: ORACLE CLOUD (ALWAYS FREE)**

### Why Oracle?
✅ **ALWAYS FREE** - doesn't expire  
✅ 2GB RAM VM included  
✅ Best for long-term hosting  

### Steps:
1. Create account: https://www.oracle.com/cloud/free/
2. Create VM (Ubuntu 22.04)
3. SSH into VM
4. Clone repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/skin-disease.git
   cd skin-disease
   ```
5. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   pip install -r requirements.txt
   ```
6. Run app:
   ```bash
   python3 app_flask.py
   ```
7. Access via: `http://YOUR_IP:5000`

---

## **Option 4: PYTHONANYWHERE**

### Why PythonAnywhere?
✅ Free tier available  
✅ Python-specific hosting  
✅ No terminal needed  

### Steps:
1. Go to https://www.pythonanywhere.com/
2. Create account
3. Upload files
4. Configure web app
5. Deploy

---

## **⚠️ IMPORTANT NOTES:**

### Model File Size
- Your `final_skin_disease_model.keras` is ~80MB
- Render free tier: **Only 500MB total storage**
- **Solution:** Host model on cloud storage (AWS S3, Google Cloud Storage)
  
```python
# In app_flask.py, download model on startup:
import urllib.request
MODEL_URL = "https://your-storage.com/final_skin_disease_model.keras"
urllib.request.urlretrieve(MODEL_URL, "final_skin_disease_model.keras")
```

### Cold Start Issue
- Free tier apps sleep after 15 min of inactivity
- First request takes 10-30 seconds
- Solution: Use paid tier or keep pinging the app

### Performance
- CPU: Single-core (slow inference)
- GPU: Not available on free tier
- Prediction time: ~5-10 seconds on free tier

---

## **🏆 RECOMMENDED SETUP:**

1. **For Testing:** Render.com (easiest)
2. **For Production:** Oracle Cloud (free + powerful)
3. **For Portfolio:** Railway.app (looks professional)

---

## **QUICK CHECKLIST:**

- [ ] GitHub repo created
- [ ] `requirements.txt` updated
- [ ] `Procfile` created
- [ ] `app_flask.py` ready
- [ ] `index.html` ready
- [ ] Model file included
- [ ] Deployment platform chosen
- [ ] App deployed and tested

---

## **LIVE DEPLOYMENT EXAMPLES:**

When deployed, your app will be at:
- **Render:** `https://yourdomain.onrender.com`
- **Railway:** `https://yourdomain-prod.up.railway.app`
- **Oracle:** `http://your-vm-ip:5000`

---

**Ready to deploy? Choose Render.com for fastest setup!** 🚀
