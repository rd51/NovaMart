# 🚀 Quick Start Guide

Get the NovaMart Marketing Analytics Dashboard running in **5 minutes**.

---

## ⚡ 5-Minute Local Setup

### 1️⃣ Install Python Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

Expected output: ✅ Successfully installed streamlit, pandas, plotly, scikit-learn...

### 2️⃣ Run the Application (30 seconds)

```bash
streamlit run app.py
```

Expected output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### 3️⃣ Open in Browser (30 seconds)

Click the link or open: `http://localhost:8501`

### 4️⃣ Explore the Dashboard (3 minutes)

- 🏠 Click through all 7 pages in sidebar
- 📊 Try the filters and dropdowns
- 🎨 Hover over charts for details
- ✅ Verify all visualizations load

**Done! ✅** Your dashboard is running locally.

---

## ☁️ 2-Minute Cloud Deployment

### 1️⃣ Push to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "NovaMart Dashboard"
git remote add origin https://github.com/USERNAME/novamart-dashboard.git
git push -u origin main
```

### 2️⃣ Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select repository: `novamart-dashboard`
5. Set main file: `app.py`
6. Click **Deploy**

⏳ Wait 2-3 minutes for deployment...

✅ Your live dashboard URL: `https://yourusername-novamart-dashboard.streamlit.app`

---

## 🎯 What to Do First

### ✅ Verify Everything Works

After launching (locally or cloud):

1. **Executive Overview page:**
   - See 4 KPI cards at top
   - See revenue trend chart
   - See channel performance bar chart

2. **Campaign Analytics page:**
   - Expand filter options
   - Select different channels
   - Try date range selector

3. **Customer Insights page:**
   - Move age distribution bin slider
   - Hover over scatter plot
   - Try trend line toggle

4. **Product Performance page:**
   - Click treemap to drill down
   - View top products table

5. **Geographic Analysis page:**
   - See bubble map of India
   - Select different metrics
   - View state table

6. **Attribution & Funnel page:**
   - Switch attribution models
   - View funnel visualization
   - See correlation heatmap

7. **ML Model Evaluation page:**
   - Adjust confusion matrix threshold
   - View ROC curve
   - Check feature importance
   - See learning curve

### 🔍 Troubleshoot If Needed

| Issue | Solution |
|-------|----------|
| "Data file not found" | Verify all 11 CSV files in `data/` folder |
| Slow to load | First load may take 30 seconds (caching) |
| Charts are blank | Check browser console (F12) for errors |
| Filter not working | Refresh page or clear Streamlit cache |

---

## 📚 Next Steps

### Want to Modify the Dashboard?

See `DEVELOPMENT.md` for:
- Adding new visualizations
- Changing colors
- Modifying filters
- Optimizing performance

### Want to Deploy to Production?

See `.github/DEPLOYMENT.md` for:
- GitHub setup
- Streamlit Cloud deployment
- Custom domain (if applicable)
- Performance optimization

### Want to Understand Architecture?

See `.github/copilot-instructions.md` for:
- Code structure
- Data flow
- Implementation patterns
- Common conventions

---

## 🎨 Key Features to Try

### 1. **Dynamic Time Aggregation**
Executive Overview page:
- Toggle between Daily, Weekly, Monthly revenue views
- See patterns emerge at different time scales

### 2. **Multi-Select Filters**
Campaign Analytics page:
- Select multiple channels
- Select multiple regions
- Pick date range
- Watch charts update instantly

### 3. **Threshold Adjustment**
ML Model Evaluation page:
- Slide confusion matrix threshold
- Watch metrics change in real-time
- Understand precision-recall tradeoff

### 4. **Interactive Hover Tooltips**
All pages:
- Hover over any chart
- See detailed values
- Click to interact (on some charts)

### 5. **Metric Switching**
Executive Overview page:
- Switch between Revenue, Conversions, ROAS
- Compare channel performance by different metrics

---

## 📞 Common Questions

### Q: How do I change the data?
**A:** Replace CSV files in `data/` folder with your own. Ensure column names match what app.py expects.

### Q: Can I add more pages?
**A:** Yes! See `DEVELOPMENT.md` for adding new page functions. Follow the existing pattern.

### Q: How do I customize colors?
**A:** Edit color scales in app.py. See `DEVELOPMENT.md` → "Color Palettes" section.

### Q: Can I deploy for free?
**A:** Yes! Streamlit Cloud's free tier includes dashboard hosting.

### Q: How do I secure sensitive data?
**A:** Use Streamlit Secrets. See `.github/DEPLOYMENT.md` → "Streamlit Secrets" section.

### Q: What if the dashboard is slow?
**A:** Check caching is working. See `DEVELOPMENT.md` → "Performance Optimization" section.

---

## 🔗 File Reference

| File | Purpose | Read if... |
|------|---------|-----------|
| `app.py` | Main dashboard | You want to modify code |
| `README.md` | User guide | You want overview |
| `DEVELOPMENT.md` | Dev guide | You want to develop |
| `.github/DEPLOYMENT.md` | Deploy guide | You want to deploy |
| `.github/copilot-instructions.md` | Architecture | You want to understand design |
| `requirements.txt` | Dependencies | You want to install packages |

---

## ✅ Success Indicators

Your dashboard is working correctly when:

✅ Page loads in < 3 seconds  
✅ All 4 KPI cards show values  
✅ Charts render with data  
✅ Filters update charts instantly  
✅ Hover tooltips appear on charts  
✅ No red error messages  
✅ Mobile view is responsive  

---

## 🚀 You're Ready!

Your NovaMart Marketing Analytics Dashboard is ready to:

- ✅ Run locally for development
- ✅ Deploy to cloud for sharing
- ✅ Explore marketing data interactively
- ✅ Generate business insights visually
- ✅ Present to stakeholders

**Start here → `streamlit run app.py`**

---

**Version:** 1.0.0  
**Last Updated:** December 2025  
**Status:** ✅ Ready to Use
