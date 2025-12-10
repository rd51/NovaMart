# 🚀 Deployment Guide - GitHub to Streamlit Cloud

Complete step-by-step guide to deploy the NovaMart Marketing Analytics Dashboard to Streamlit Cloud.

---

## 📋 Prerequisites

✅ GitHub account (free at [github.com](https://github.com))  
✅ Streamlit Community Cloud account (free at [streamlit.io/cloud](https://streamlit.io/cloud))  
✅ All project files locally (app.py, requirements.txt, README.md, .github/, data/)  

---

## 🔧 Step 1: Prepare Your GitHub Repository

### 1.1 Initialize Git Locally

```bash
cd your-project-directory
git init
git add .
git commit -m "Initial commit: NovaMart Marketing Dashboard"
```

### 1.2 Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Name: `novamart-dashboard`
3. Description: "Interactive Streamlit dashboard for marketing analytics"
4. Select **Public** (needed for Streamlit Cloud free tier)
5. Click **Create repository**

### 1.3 Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/novamart-dashboard.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## 📊 Step 2: Verify Repository Structure

Your GitHub repository should have this structure:

```
novamart-dashboard/
├── .github/
│   └── copilot-instructions.md    ✅
├── .gitignore                      ✅
├── .streamlit/
│   └── config.toml                 ✅
├── app.py                          ✅
├── requirements.txt                ✅
├── README.md                       ✅
└── data/                           ✅ (all 11 CSV files)
```

**Important:** Make sure `data/` folder contains all 11 CSV files:
- campaign_performance.csv
- customer_data.csv
- product_sales.csv
- lead_scoring_results.csv
- feature_importance.csv
- learning_curve.csv
- geographic_data.csv
- channel_attribution.csv
- funnel_data.csv
- customer_journey.csv
- correlation_matrix.csv

---

## ☁️ Step 3: Deploy to Streamlit Cloud

### 3.1 Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub (click "Sign in with GitHub")
3. Authorize Streamlit to access your repositories

### 3.2 Create New App

1. Click **"Create app"** button
2. Select:
   - **Repository:** `yourusername/novamart-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`

3. Click **Deploy**

⏳ **Wait 2-3 minutes** for deployment to complete. You'll see:
- Building phase
- Running phase
- Live app link

### 3.3 Verify Deployment

Your app is live when you see:
- ✅ Green checkmark
- 🔗 URL like: `https://yourusername-novamart-dashboard.streamlit.app`

---

## 🔐 Step 4: Optional - Use Streamlit Secrets

If you need to store sensitive data (API keys, custom data paths):

### 4.1 Local Secrets (Development)

Create `.streamlit/secrets.toml` locally:

```toml
# .streamlit/secrets.toml
data_path = "data/"
api_key = "your-secret-key"
```

### 4.2 Cloud Secrets (Production)

1. Go to your Streamlit Cloud app settings (gear icon)
2. Click **Secrets**
3. Paste contents of `secrets.toml`
4. Save

### 4.3 Access in Code

```python
import streamlit as st
data_path = st.secrets.get("data_path", "data/")
```

---

## 📤 Step 5: Update Code & Redeploy

### 5.1 Make Changes Locally

```bash
# Edit files
# Test locally: streamlit run app.py
```

### 5.2 Push to GitHub

```bash
git add .
git commit -m "Update: Added new visualization"
git push origin main
```

### 5.3 Auto-Redeploy

✅ Streamlit Cloud automatically redeploys when you push to main branch  
⏳ Wait 1-2 minutes for changes to appear online

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas'"

**Solution:**
- Ensure `requirements.txt` has all dependencies
- Check syntax: `pip install -r requirements.txt` locally first
- Redeploy and check Streamlit logs

### Issue: "FileNotFoundError: data/ folder not found"

**Solution:**
- Verify `data/` folder is in GitHub repository
- Check CSV filenames match exactly (case-sensitive)
- Verify CSV files are not in .gitignore

### Issue: App takes too long to load

**Solution:**
- Check if data loading is cached with `@st.cache_data`
- Monitor Streamlit logs for performance issues
- Consider reducing data size if using large files

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
- Requirements.txt is missing or malformed
- Check for correct package names and versions
- Try: `pip freeze | grep streamlit`

### Issue: Deployment stuck on "Building"

**Solution:**
- Check Streamlit Cloud logs
- Verify repository is public
- Try redeploying from Streamlit dashboard
- Check for syntax errors: `python -m py_compile app.py`

---

## 📊 Live Dashboard Checklist

Before sharing link with stakeholders:

- [ ] ✅ App loads without errors
- [ ] ✅ All 7 pages are accessible
- [ ] ✅ Filters and interactions work
- [ ] ✅ Charts display correctly
- [ ] ✅ Hover tooltips show data
- [ ] ✅ No console errors in browser dev tools
- [ ] ✅ Mobile responsiveness tested
- [ ] ✅ Performance acceptable (< 3s page loads)

---

## 🔗 Sharing Your Dashboard

### Share Public Link

```
https://yourusername-novamart-dashboard.streamlit.app
```

### Embed in Website

```html
<iframe 
  src="https://yourusername-novamart-dashboard.streamlit.app" 
  style="width:100%;height:800px;border:none;">
</iframe>
```

### Share with Team

1. Streamlit app is publicly accessible
2. No login required for viewers
3. Share link via email, Slack, or Teams

---

## 📈 Performance Tips

### Optimize Load Time

```python
# DO use caching
@st.cache_data
def load_data():
    return pd.read_csv('data/file.csv')

# DON'T reload data on every interaction
df = pd.read_csv('data/file.csv')  # ❌ Slow
```

### Reduce Chart Complexity

```python
# Limit data points for real-time updates
data = data.tail(1000)  # Last 1000 rows

# Use aggregated data for large datasets
data = data.groupby('month').sum()
```

### Optimize Images

- Use SVG or compressed PNG for logos
- Limit image sizes to < 500KB

---

## 📚 Useful Resources

- **Streamlit Docs:** [docs.streamlit.io](https://docs.streamlit.io)
- **Plotly Docs:** [plotly.com/python](https://plotly.com/python)
- **GitHub Help:** [docs.github.com](https://docs.github.com)
- **Streamlit Cloud Help:** [discuss.streamlit.io](https://discuss.streamlit.io)

---

## ✅ Success Indicators

Your deployment is successful when:

✅ App URL is live and accessible  
✅ All data loads within 3 seconds  
✅ All visualizations render correctly  
✅ Filters and interactions work  
✅ No error messages in browser console  
✅ Mobile view is responsive  

---

## 🆘 Need Help?

1. **Streamlit Issues:** Check [Streamlit Docs](https://docs.streamlit.io)
2. **GitHub Issues:** Check [GitHub Help](https://github.com/contact)
3. **Python Issues:** Stack Overflow or ChatGPT
4. **Assignment Help:** Contact your instructor

---

**Deployment Guide v1.0**  
**Last Updated:** December 2025  
**Happy Deploying! 🚀**
