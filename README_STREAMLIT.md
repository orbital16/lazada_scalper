# 🚀 Deploy to Streamlit Cloud

## Quick Deploy

### 1. Push to GitHub
```bash
./deploy_to_streamlit.sh
```

### 2. Deploy on Streamlit
1. Go to: https://share.streamlit.io/deploy
2. Sign in with GitHub
3. Fill in:
   - **Repository**: `orbital16/lazada-stock-monitor`
   - **Branch**: `main`
   - **Main file**: `stock_monitor_ui.py`
4. Click "Deploy!"

## 🔒 Important: Privacy Settings

### For Public Deployment
Streamlit free tier requires **public** repositories.

**Before making public:**
```bash
# Remove any sensitive files
rm -f lazada_cookies.json
rm -f *.har
git add -u
git commit -m "Remove sensitive files for public deployment"
git push
```

**Then change repo to public:**
1. Go to: https://github.com/orbital16/lazada-stock-monitor/settings
2. Scroll to "Danger Zone"
3. Click "Change visibility" → Public

### For Private Deployment
Need Streamlit Teams plan ($250/month) for private repos.

## 🎯 After Deployment

Your app will be live at:
```
https://your-chosen-name.streamlit.app
```

## 🧪 Testing Deployment

1. Open your Streamlit app URL
2. Add a Lazada product URL in sidebar
3. Click "Add Product"
4. Start monitoring
5. Check activity log

## ⚠️ Limitations on Streamlit Cloud

### Free Tier
- Public repos only
- 1 GB RAM
- 1 CPU core
- Can sleep after inactivity

### Workarounds
- **Cookies**: Won't work on deployed version (no local file access)
- **Monitoring**: Set reasonable intervals (2-5 seconds)
- **Storage**: `products.json` resets on restart (use CSV export)

## 🔧 Streamlit-Specific Configuration

Created files:
- `.streamlit/config.toml` - Theme and server settings
- `requirements.txt` - Dependencies (auto-detected)

## 💡 Pro Deployment

### Option 1: Streamlit Cloud (Easiest)
- ✅ Free (public repos)
- ✅ Auto-deploy on git push
- ✅ SSL certificate included
- ❌ Sleeps after inactivity
- ❌ Limited resources

### Option 2: Self-Host
```bash
# On your server
git clone git@github.com-orbital16:orbital16/lazada-stock-monitor.git
cd lazada-stock-monitor
pip install -r requirements.txt
streamlit run stock_monitor_ui.py --server.port 80
```

### Option 3: Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "stock_monitor_ui.py"]
```

## 🌐 Access Your App

After deployment:
1. **Desktop**: Open app URL in browser
2. **Mobile**: Works on phone browsers
3. **Share**: Send URL to others (if public)

## 📊 Monitoring Deployment

Streamlit Cloud dashboard shows:
- App status (running/sleeping)
- Resource usage
- Error logs
- Visitor stats

Access at: https://share.streamlit.io/

## 🐛 Troubleshooting

### "Module not found"
- Check `requirements.txt` includes all dependencies
- Redeploy after updating requirements

### "App is sleeping"
- Free tier sleeps after inactivity
- Just reload - wakes up in ~30 seconds

### "Repository not found"
- Check repo name exactly matches
- Ensure repo is public (for free tier)
- Verify Streamlit has GitHub access

### "Cannot read products.json"
- Expected on cloud deployment
- Products won't persist between restarts
- Use Export/Import instead

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Sensitive files removed (cookies, HAR)
- [ ] Repository is public (or have Teams plan)
- [ ] Deployed on Streamlit Cloud
- [ ] Tested with real Lazada URL
- [ ] Bookmarked app URL

## 🎉 Success!

Once deployed, you can:
- Access from anywhere
- Share with others (public repo)
- Monitor products 24/7
- No local setup needed

---

**Deploy now**: `./deploy_to_streamlit.sh`
