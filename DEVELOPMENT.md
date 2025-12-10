# 👨‍💻 Development Guide

Guide for developers working on the NovaMart Marketing Analytics Dashboard.

---

## 🛠️ Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/novamart-dashboard.git
cd novamart-dashboard
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
streamlit run app.py
```

Application will open at: `http://localhost:8501`

---

## 📂 Project Structure

```
app.py                    # Main application file
├── load_data()           # Cached data loading
├── sidebar()             # Navigation menu
├── page_executive_overview()
├── page_campaign_analytics()
├── page_customer_insights()
├── page_product_performance()
├── page_geographic_analysis()
├── page_attribution_funnel()
└── page_ml_evaluation()

data/                     # CSV datasets (11 files)
.streamlit/              # Streamlit configuration
.github/                 # GitHub metadata
└── copilot-instructions.md
├── DEPLOYMENT.md
requirements.txt         # Python dependencies
README.md               # User documentation
```

---

## 🔑 Key Architecture Patterns

### 1. Data Caching

All data loads use `@st.cache_data` to prevent reloading on every interaction:

```python
@st.cache_data
def load_data():
    """Load all CSV files once per session"""
    data = {}
    data['campaigns'] = pd.read_csv('data/campaign_performance.csv', parse_dates=['date'])
    # ... load other files
    return data
```

**Why:** Dramatically improves performance for interactive elements like filters.

### 2. Page Navigation

Sidebar radio button routes to page functions:

```python
page = sidebar()  # Returns selected page name

if page == "🏠 Executive Overview":
    page_executive_overview(data)
elif page == "📈 Campaign Analytics":
    page_campaign_analytics(data)
# ... etc
```

### 3. Filter Pattern

Data filtered before visualization:

```python
# Get filter values from UI
selected_channels = st.multiselect("Channels", options=data.unique())

# Apply filters
filtered = data[data['channel'].isin(selected_channels)]

# Visualize filtered data
fig = px.bar(filtered, ...)
```

### 4. Responsive Layout

Use `st.columns()` for multi-column layouts:

```python
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Revenue", "₹100 Cr")
with col2:
    st.metric("Conversions", "50K")
with col3:
    st.metric("ROAS", "2.5x")
```

---

## 📊 Adding a New Visualization

### Step 1: Identify Data Source

From Assignment.txt, find which CSV contains your data:
- Campaign data → `campaign_performance.csv`
- Customer data → `customer_data.csv`
- Geographic data → `geographic_data.csv`
- Etc.

### Step 2: Aggregate Data

```python
# Example: Revenue by channel
channel_revenue = (campaigns
    .groupby('channel')['revenue']
    .sum()
    .sort_values(ascending=True)
    .reset_index())
```

**Key:** Always use `.reset_index()` after `.groupby()`

### Step 3: Create Plotly Figure

```python
fig = px.bar(
    channel_revenue,
    x='revenue',
    y='channel',
    orientation='h',
    title='Total Revenue by Channel',
    labels={'revenue': 'Revenue (₹)', 'channel': 'Channel'},
    color_discrete_sequence=px.colors.qualitative.Set2
)
```

### Step 4: Customize & Display

```python
fig.update_layout(
    height=400,
    template='plotly_white',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)
```

### Step 5: Add Interaction (Optional)

```python
# Filter option
selected_region = st.selectbox("Region", options=data['region'].unique())
filtered = data[data['region'] == selected_region]

# Recreate visualization with filtered data
fig = px.bar(filtered, ...)
```

---

## 🎨 Styling Guidelines

### Color Palettes

**For categorical data:**
```python
color_discrete_sequence=px.colors.qualitative.Set2
color_discrete_sequence=px.colors.qualitative.Set3
color_discrete_sequence=px.colors.qualitative.Pastel
```

**For sequential data:**
```python
color_continuous_scale='Blues'
color_continuous_scale='Viridis'
color_continuous_scale='Purples'
```

**For diverging data:**
```python
color_continuous_scale='RdBu_r'  # Red-Blue (reversed)
color_continuous_scale='RdYlGn'  # Red-Yellow-Green
```

### Typography

```python
# Titles
st.title("📊 Main Title")           # Largest
st.header("## Subheader")           # Large
st.subheader("### Section Title")   # Medium

# Text
st.markdown("**Bold text** and *italic*")
st.write("Regular text with formatting")
```

### Formatting

```python
# Currency
f"₹{value/1e7:.2f} Cr"  # Crores
f"₹{value:,.0f}"        # Rupees with commas

# Percentages
f"{value:.1f}%"         # 1 decimal place

# Large numbers
f"{value:,.0f}"         # Add commas
```

---

## 🧪 Testing Locally

### Test Data Loading

```python
# In terminal
python -c "import pandas as pd; df = pd.read_csv('data/campaign_performance.csv'); print(df.shape)"
```

### Test Specific Page

Edit `app.py` main():
```python
# Comment out other pages, test one:
page_executive_overview(data)
```

### Test Individual Function

```bash
streamlit run app.py --logger.level=debug
```

### Clear Cache for Testing

```bash
streamlit cache clear
```

---

## 🔍 Debugging Tips

### Print Debug Info

```python
st.write("Debug:", variable)  # Display in app
st.write(df.head())            # Show dataframe
st.write(df.info())            # Show structure
st.write(df.describe())        # Show statistics
```

### Check Data Types

```python
st.write(df.dtypes)  # Show column types
```

### Inspect Filters

```python
st.write("Selected:", selected_channels)
st.write("Filtered shape:", filtered.shape)
```

### Browser Console

1. Press **F12** in browser
2. Check **Console** tab for JavaScript errors
3. Check **Network** tab for load times

---

## 📦 Common Tasks

### Add a New CSV File

1. Place CSV in `data/` folder
2. Add to `load_data()`:
   ```python
   data['new_file'] = pd.read_csv("data/new_file.csv")
   ```
3. Use in visualization:
   ```python
   new_data = data['new_file']
   ```

### Add a New Filter

```python
col1, col2 = st.columns(2)

with col1:
    selected_category = st.multiselect(
        "Category",
        options=data['category'].unique(),
        default=data['category'].unique()
    )

with col2:
    selected_year = st.selectbox(
        "Year",
        options=sorted(data['year'].unique()),
        index=0
    )

# Apply filters
filtered = data[
    (data['category'].isin(selected_category)) &
    (data['year'] == selected_year)
]
```

### Add a Metric Card

```python
col1, col2, col3 = st.columns(3)

with col1:
    value = data['revenue'].sum()
    st.metric("Total Revenue", f"₹{value/1e7:.2f} Cr")

with col2:
    value = data['conversions'].sum()
    st.metric("Conversions", f"{value:,.0f}")

with col3:
    value = data['roas'].mean()
    st.metric("Avg ROAS", f"{value:.2f}x")
```

### Time-Series Aggregation

```python
# Daily
daily = data.groupby('date')['revenue'].sum()

# Weekly
weekly = data.groupby(pd.Grouper(key='date', freq='W'))['revenue'].sum()

# Monthly
monthly = data.groupby(pd.Grouper(key='date', freq='M'))['revenue'].sum()

# Quarterly
quarterly = data.groupby(pd.Grouper(key='date', freq='Q'))['revenue'].sum()
```

---

## 🚀 Performance Optimization

### Cache Expensive Operations

```python
@st.cache_data
def expensive_calculation(df):
    # Long-running operation
    result = df.groupby(...).apply(complex_function)
    return result

result = expensive_calculation(data)
```

### Limit Data Points

```python
# For real-time dashboards, limit rows
if len(data) > 10000:
    data = data.sample(10000)  # Random sample

# Or show recent data
data = data.tail(10000)  # Last 10k rows
```

### Use `use_container_width=True`

```python
# Fills available width (better performance)
st.plotly_chart(fig, use_container_width=True)

# Not this:
st.plotly_chart(fig, width=800)  # Fixed width
```

---

## 📝 Code Standards

### Function Documentation

```python
def page_executive_overview(data):
    """
    Executive Overview Dashboard
    
    Shows KPIs and key metrics at a glance.
    
    Args:
        data (dict): Dictionary of DataFrames from load_data()
    
    Returns:
        None (displays Streamlit components)
    """
```

### Variable Naming

```python
# Good ✅
total_revenue = campaigns['revenue'].sum()
customer_count = len(customers)
monthly_sales = data.groupby('month')['sales'].sum()

# Avoid ❌
tr = campaigns['revenue'].sum()
x = len(customers)
temp = data.groupby('month')['sales'].sum()
```

### Comments

```python
# Use for WHY, not WHAT
# This filter removes test accounts
filtered = data[data['account_type'] != 'test']

# Avoid obvious comments
total = data['revenue'].sum()  # Sum the revenue ❌
```

---

## 🐛 Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `KeyError: 'column'` | Column doesn't exist | Check CSV headers and rename() if needed |
| `ValueError: cannot convert` | Wrong data type | Use `.astype()` to convert |
| `FileNotFoundError` | Wrong file path | Check path is relative to project root |
| `ModuleNotFoundError` | Package not installed | `pip install -r requirements.txt` |
| `Chart not displaying` | NaN values in data | Use `.dropna()` or `.fillna()` |
| `Memory error` | Too much data | Filter or sample data before visualizing |

---

## 🔄 Version Control

### Create Feature Branch

```bash
git checkout -b feature/new-chart-type
```

### Commit Changes

```bash
git add .
git commit -m "Add: Customer satisfaction violin plot"
```

### Push & Create Pull Request

```bash
git push origin feature/new-chart-type
```

Then create PR on GitHub for code review.

### Merge to Main

```bash
git checkout main
git merge feature/new-chart-type
git push origin main
```

---

## 📚 Resources

- **Streamlit API:** [docs.streamlit.io](https://docs.streamlit.io)
- **Plotly Express:** [plotly.com/python/plotly-express](https://plotly.com/python/plotly-express)
- **Pandas:** [pandas.pydata.org](https://pandas.pydata.org)
- **Python:** [python.org](https://python.org)

---

**Development Guide v1.0**  
**Last Updated:** December 2025  
**Happy Coding! 💻**
