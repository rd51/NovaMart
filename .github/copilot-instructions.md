# NovaMart Marketing Analytics Dashboard - AI Agent Instructions

## 🎯 Project Overview

This is a **Streamlit-based data visualization dashboard** for a fictional omnichannel retailer (NovaMart). The project requires building **20+ interactive visualizations** across 7 dashboard pages analyzing 11 interconnected CSV datasets containing 2 years of marketing, customer, product, and ML model performance data.

**Key Context**: This is an educational assignment (Masters of AI in Business) evaluating visualization appropriateness, design quality, interactivity, business insights, and code quality. Charts must reveal specific business insights, not just display data.

---

## 📂 Architecture & Data Flow

### Dataset Structure
All data comes from CSV files in the `data/` directory:

| File | Purpose | Key Fields |
|------|---------|-----------|
| `campaign_performance.csv` (5,858 rows) | Daily marketing metrics | channel, region, date, revenue, conversions, spend, CTR, CPA, ROAS |
| `customer_data.csv` (5,000 rows) | Customer demographics | age, income, lifetime_value, customer_segment, satisfaction_score, churn |
| `product_sales.csv` (1,440 rows) | Hierarchical product sales | category, subcategory, product_name, sales, units, profit_margin, region, quarter |
| `lead_scoring_results.csv` (2,000 rows) | ML predictions | actual_converted, predicted_probability, predicted_class |
| `geographic_data.csv` (15 rows) | State-level metrics | state, latitude, longitude, revenue, customers, market_penetration, satisfaction |
| `feature_importance.csv` (11 rows) | Feature importance with errors | feature, importance, std_deviation |
| `learning_curve.csv` (11 rows) | Training dynamics | train_size, training_score, validation_score |
| `channel_attribution.csv` (8 rows) | Attribution models | channel, first_touch, last_touch, linear, time_decay, position_based |
| `funnel_data.csv` (6 rows) | Marketing funnel | stage, visitors, conversions |
| `customer_journey.csv` (8 rows) | Multi-touch paths | touchpoint_sequence, flow_count |
| `correlation_matrix.csv` (10x10 matrix) | Metric correlations | Pre-computed correlation values |

### Dashboard Pages Architecture
The app uses a **sidebar-driven page navigation pattern**:

```
streamlit_starter_app.py (575 lines)
├── sidebar() → Radio button navigation
├── load_data() → Cached CSV loading (all files loaded once)
└── 7 Page Functions:
    ├── page_executive_overview() → KPI cards + 2 charts
    ├── page_campaign_analytics() → Temporal & comparison charts
    ├── page_customer_insights() → Distributions & relationships
    ├── page_product_performance() → Hierarchy & category breakdowns
    ├── page_geographic_analysis() → Maps (choropleth, bubble)
    ├── page_attribution_funnel() → Attribution models & funnels
    └── page_ml_evaluation() → Confusion matrix, ROC, learning curve
```

**Data Loading Pattern**: `@st.cache_data` decorator ensures data loads once per session, not on every interaction.

---

## 🔑 Critical Implementation Patterns

### 1. Chart Selection Framework
**DO NOT choose charts arbitrarily.** The Assignment.txt specifies exact chart types with expected business insights. Match:
- **Comparison**: Horizontal bar (channel revenue), grouped bar (region × quarter), stacked bar (monthly campaign types)
- **Temporal**: Line chart (daily/weekly/monthly aggregation), area chart (cumulative by channel)
- **Distribution**: Histogram (age bins), box plot (LTV by segment), violin plot (satisfaction by NPS)
- **Relationship**: Scatter (income vs. LTV), bubble (CTR vs. conversion rate vs. spend)
- **Part-to-Whole**: Pie/donut (attribution models), treemap (product hierarchy), sunburst (region→tier→segment)
- **Geographic**: Choropleth (state-wise revenue), bubble map (store performance)
- **ML Evaluation**: Confusion matrix, ROC curve, learning curve, feature importance bar

### 2. Plotly as Primary Library
All visualizations use **Plotly** (not matplotlib/seaborn). Plotly provides:
- Interactive hover tooltips (essential for business users)
- Native interactivity (zoom, pan, select)
- `use_container_width=True` for responsive layouts
- `update_layout()` for customizing axes, legends, fonts

Example pattern:
```python
fig = px.line(df, x='date', y='revenue', color='channel', 
              title='Revenue Trend', labels={'revenue': 'Revenue (₹)'})
fig.update_layout(hovermode='x unified')  # Better tooltip grouping
st.plotly_chart(fig, use_container_width=True)
```

### 3. Data Aggregation by Time Period
Campaign data requires flexible time aggregation:
- **Daily**: Raw data (shows weekend/weekday patterns)
- **Weekly**: `pd.Grouper(key='date', freq='W')` aggregation
- **Monthly**: `pd.Grouper(key='date', freq='M')` aggregation

Implement as dropdown or toggle—don't hardcode.

### 4. Filtering Patterns
Each page uses consistent Streamlit filters in `st.columns()`:
```python
col1, col2, col3 = st.columns(3)
with col1:
    channels = st.multiselect("Channels", options=data.unique())
with col2:
    regions = st.multiselect("Regions", options=data.unique())
with col3:
    date_range = st.date_input("Date Range", value=(min_date, max_date))

# Apply filters as boolean masks
filtered = data[(data['channel'].isin(channels)) & 
                (data['region'].isin(regions)) &
                (data['date'] >= date_range[0])]
```

### 5. Insight-Driven Design
**Every chart must reveal the expected business insight** (from Assignment.txt). Examples:
- **Channel revenue bar chart** → Shows Google Ads & Email revenue dominance, LinkedIn lower volume
- **Seasonal line chart** → Diwali (Oct-Nov) & Christmas (Dec) peaks visible in raw daily data
- **LTV box plot** → Premium segment median 2.5x higher than Budget; Churned has low median but high outliers
- **Age distribution histogram** → Skew toward 25-40 age range
- **Feature importance** → Webinar attendance & form submissions are strongest ML predictors

If the chart doesn't clearly show these patterns, adjust aggregations or filtering.

### 6. ML Model Evaluation Pattern
For `lead_scoring_results.csv`:
```python
from sklearn.metrics import confusion_matrix, roc_curve, auc

# Confusion matrix
cm = confusion_matrix(df['actual_converted'], df['predicted_class'])
fig = px.imshow(cm, labels=dict(x='Predicted', y='Actual'),
                 text_auto=True, title='Lead Scoring Confusion Matrix')

# ROC curve
fpr, tpr, thresholds = roc_curve(df['actual_converted'], df['predicted_probability'])
roc_auc = auc(fpr, tpr)
fig = px.area(x=fpr, y=tpr, title=f'ROC Curve (AUC = {roc_auc:.3f})')
```

---

## 💻 Critical Developer Workflows

### Running the Dashboard
```bash
# Install dependencies (one-time)
pip install -r requirements.txt

# Run locally
streamlit run streamlit_starter_app.py

# Will open at http://localhost:8501
```

### Data Path Configuration
Edit the `load_data()` function in `streamlit_starter_app.py`:
```python
data_path = "data/"  # Update to match your data folder location
```
If data files are in same directory as app, use `data_path = "./"`

### Debugging Tips
- **Data not loading?** Check `st.error()` message—will show FileNotFoundError with exact path
- **Chart not appearing?** Verify `use_container_width=True` is set; check for NaN values in data
- **Slow performance?** Ensure `@st.cache_data` is on `load_data()` function
- **Cache stale?** Use browser dev tools → Clear cache, or restart Streamlit

### Testing Visualizations
When implementing new charts:
1. First filter/aggregate data manually using pandas (test in notebook/REPL)
2. Then wrap in plotly figure
3. Test with different filter selections to verify responsiveness
4. Check tooltip labels are readable (use `labels={}` parameter)

---

## 🎨 Code Quality Standards from Assignment

### Required Practices
- **Modular functions**: Separate function for each visualization (don't inline 20+ charts in one function)
- **Caching**: All data loads use `@st.cache_data` decorator
- **Responsive layout**: Use `st.columns()` for multi-column layouts; `use_container_width=True` for charts
- **Clear naming**: Variable names like `channel_revenue`, `regional_quarterly` (not `df`, `temp`)
- **Docstrings**: Each function starts with `"""Purpose and inputs"""` 
- **Error handling**: Try/except around CSV loading; graceful message for missing data

### Visual Design Conventions
- Use **consistent color schemes**: Plotly's default "plotly" theme works; or specify `color_discrete_sequence`
- **India Rupee formatting**: Use `f"₹{value/1e7:.2f} Cr"` for millions/crores
- **Axis labels**: Always include units (₹, %, customers, etc.)
- **Title clarity**: "Revenue by Channel" (not "Channel Revenue"), "Age Distribution" (not "Histogram")
- **Legend placement**: For crowded charts, move legend outside: `update_layout(legend=dict(x=1.05, y=1))`

### Example Well-Structured Visualization
```python
def visualize_channel_performance(data):
    """
    Horizontal bar chart of total revenue by marketing channel.
    Reveals: Google Ads and Email drive highest revenue.
    """
    channel_revenue = (data.groupby('channel')['revenue']
                       .sum()
                       .sort_values(ascending=True)
                       .reset_index())
    
    fig = px.bar(channel_revenue, x='revenue', y='channel', 
                 orientation='h', title='Total Revenue by Marketing Channel',
                 labels={'revenue': 'Revenue (₹)', 'channel': 'Channel'},
                 color_discrete_sequence=['#3366cc'])
    fig.update_xaxes(tickformat='$,.0f')  # Format as currency
    return fig

st.subheader("📊 Revenue by Channel")
fig = visualize_channel_performance(campaigns)
st.plotly_chart(fig, use_container_width=True)
```

---

## 🚀 Common Implementation Tasks

### Adding a New Visualization
1. **Identify the data source** from Assignment.txt (e.g., "campaign_performance.csv")
2. **Determine aggregation** (by channel? by region×quarter? daily?)
3. **Choose chart type** from specified list (not your preference)
4. **Aggregate with pandas**:
   ```python
   metric = data.groupby(['groupby_col1', 'groupby_col2'])['metric_col'].sum().reset_index()
   ```
5. **Create Plotly figure** using `px.bar()`, `px.line()`, etc.
6. **Add to page function** and test with filters
7. **Verify insight clarity**: Does the chart reveal the expected finding?

### Adding Filters
Template for new filter:
```python
col1, col2, col3 = st.columns(3)
with col1:
    selected_value = st.multiselect(
        "Label", 
        options=data['column'].unique(),
        default=data['column'].unique()  # Pre-select all
    )
# Apply filter
filtered = data[data['column'].isin(selected_value)]
```

### Time-Based Aggregation Toggle
```python
freq_option = st.radio("Time Period", ["Daily", "Weekly", "Monthly"])
freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "M"}

agg_data = (data.groupby(pd.Grouper(key='date', freq=freq_map[freq_option]))
            [['revenue', 'conversions']].sum().reset_index())
```

---

## 📋 Evaluation Criteria (Weight Your Decisions)

When implementing features, prioritize by assignment weight:
1. **Chart Type Appropriateness (25%)** → Use EXACT chart types from Assignment.txt
2. **Visual Design Quality (20%)** → Color schemes, labeling, accessibility
3. **Interactivity & UX (20%)** → Filters, tooltips, responsive layout
4. **Insight Generation (20%)** → Charts must reveal expected business insights
5. **Code Quality (15%)** → Modularity, caching, documentation

**DO NOT spend 80% of effort on code quality if charts don't reveal insights.**

---

## 🎁 Bonus Features (Optional, +5-15%)

- **Sankey Diagram** (+5%): `plotly.graph_objects.Sankey` from `customer_journey.csv`
- **Animated Charts** (+5%): `animation_frame='quarter'` parameter in plotly
- **Precision-Recall Curve** (+3%): Use `sklearn.metrics.precision_recall_curve` alongside ROC
- **Dark Mode** (+3%): Toggle with `st.select_slider` → adjust Plotly template
- **Data Export** (+4%): `st.download_button` for filtered data as CSV

---

## 📚 Key Library Functions

| Task | Library | Function | Notes |
|------|---------|----------|-------|
| Load data | pandas | `pd.read_csv(path, parse_dates=['date'])` | Use parse_dates for date columns |
| Group & aggregate | pandas | `.groupby()`, `.reset_index()` | Always reset_index() after groupby |
| Time aggregation | pandas | `pd.Grouper(key='date', freq='M')` | freq: D/W/M/Y |
| Create chart | plotly.express | `px.bar()`, `px.line()`, `px.scatter()` | 20+ chart types available |
| Customize chart | plotly.graph_objects | `fig.update_layout()`, `fig.update_xaxes()` | Fine-grained control |
| Build layout | streamlit | `st.columns()`, `st.tabs()`, `st.expander()` | Responsive design |
| Add filters | streamlit | `st.multiselect()`, `st.slider()`, `st.radio()` | Return list/value to filter data |
| ML metrics | scikit-learn | `confusion_matrix()`, `roc_curve()`, `auc()` | For model evaluation charts |
| Caching | streamlit | `@st.cache_data` | Decorate load_data() to prevent recomputation |

---

## ⚠️ Common Pitfalls

- **Not resetting index after groupby**: Results in MultiIndex; use `.reset_index()`
- **Hardcoding data paths**: Update `load_data()` to match your data folder location
- **Missing `use_container_width=True`**: Charts won't fill dashboard width
- **Inline all 20+ charts**: Makes code unmaintainable; use separate functions per visualization
- **Ignoring the "Expected Insight"**: Chart must visually reveal the insight in Assignment.txt
- **Using matplotlib/seaborn**: Plotly is required for interactivity
- **Not filtering data before groupby**: Creates performance bottlenecks with 5K+ row datasets

---

## 🔗 Quick Reference Files

- **Assignment Details**: `Assignment.txt` (210 lines) — Exact chart requirements & expected insights
- **Data Dictionary**: `README.md` (120 lines) — Dataset descriptions & visualization mapping
- **Starter App**: `streamlit_starter_app.py` (575 lines) — Base structure with 2 pages partially implemented
- **Dependencies**: `requirements.txt` — Install with `pip install -r requirements.txt`
- **Data Folder**: `data/` — All 11 CSV files must be here for app to run

---

**Last Updated**: December 2025 | **Assignment**: Masters of AI in Business - Data Visualization
