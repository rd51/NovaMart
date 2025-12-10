"""
NovaMart Marketing Analytics Dashboard
======================================
Masters of AI in Business - Data Visualization Assignment

A comprehensive Streamlit dashboard for analyzing NovaMart's marketing performance,
customer behavior, product sales, and ML model evaluation.

To run locally:
    streamlit run app.py

To deploy to Streamlit Cloud:
    1. Push code to GitHub
    2. Connect repository on streamlit.io/cloud
    3. Set data folder path in secrets if needed
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="NovaMart Marketing Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {padding-top: 2rem;}
    .metric-card {background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem;}
    h1 {color: #1f77b4;}
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# DATA LOADING (with caching)
# =============================================================================
@st.cache_data
def load_data():
    """Load all datasets with error handling"""
    data = {}
    
    # Data path - can be customized via Streamlit secrets
    data_path = "data/"
    
    try:
        # Load all CSV files
        data['campaigns'] = pd.read_csv(f"{data_path}campaign_performance.csv", parse_dates=['date'])
        data['customers'] = pd.read_csv(f"{data_path}customer_data.csv")
        data['products'] = pd.read_csv(f"{data_path}product_sales.csv")
        data['leads'] = pd.read_csv(f"{data_path}lead_scoring_results.csv")
        data['feature_importance'] = pd.read_csv(f"{data_path}feature_importance.csv")
        data['learning_curve'] = pd.read_csv(f"{data_path}learning_curve.csv")
        data['geographic'] = pd.read_csv(f"{data_path}geographic_data.csv")
        data['attribution'] = pd.read_csv(f"{data_path}channel_attribution.csv")
        data['funnel'] = pd.read_csv(f"{data_path}funnel_data.csv")
        data['journey'] = pd.read_csv(f"{data_path}customer_journey.csv")
        data['correlation'] = pd.read_csv(f"{data_path}correlation_matrix.csv", index_col=0)
        
        return data
    except FileNotFoundError as e:
        st.error(f"❌ Data file not found: {e}")
        st.info("📁 Please ensure all CSV files are in the 'data/' folder")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()

# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================
def sidebar():
    """Create sidebar navigation and info"""
    with st.sidebar:
        st.title("📊 NovaMart Analytics")
        st.markdown("---")
        
        page = st.radio(
            "Navigate to:",
            [
                "🏠 Executive Overview",
                "📈 Campaign Analytics",
                "👥 Customer Insights",
                "📦 Product Performance",
                "🗺️ Geographic Analysis",
                "🎯 Attribution & Funnel",
                "🤖 ML Model Evaluation"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.info("""
        **Masters of AI in Business**
        
        Data Visualization Assignment
        
        NovaMart - Omnichannel Retailer Analytics
        """)
        
        st.markdown("---")
        st.caption("📧 Questions? Contact your instructor")
    
    return page

# =============================================================================
# PAGE: EXECUTIVE OVERVIEW
# =============================================================================
def page_executive_overview(data):
    """Executive Overview - KPIs and key metrics"""
    st.title("🏠 Executive Overview")
    st.markdown("Key performance metrics and trends at a glance")
    
    campaigns = data['campaigns']
    customers = data['customers']
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = campaigns['revenue'].sum()
        st.metric(
            "Total Revenue",
            f"₹{total_revenue/1e7:.2f} Cr",
            delta="YoY Growth"
        )
    
    with col2:
        total_conversions = campaigns['conversions'].sum()
        st.metric(
            "Total Conversions",
            f"{total_conversions:,.0f}",
            delta="vs Last Period"
        )
    
    with col3:
        avg_roas = campaigns[campaigns['roas'] > 0]['roas'].mean()
        st.metric(
            "Average ROAS",
            f"{avg_roas:.2f}x",
            delta="Return on Ad Spend"
        )
    
    with col4:
        total_customers = len(customers)
        st.metric(
            "Total Customers",
            f"{total_customers:,}",
            delta="Active Customers"
        )
    
    st.markdown("---")
    
    # Revenue Trend
    st.subheader("📈 Revenue Trend Over Time")
    
    # Aggregation level selector
    col1, col2 = st.columns([3, 1])
    with col2:
        agg_level = st.selectbox(
            "Aggregation",
            ["Daily", "Weekly", "Monthly"],
            key="exec_agg"
        )
    
    freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "M"}
    monthly_revenue = campaigns.groupby(pd.Grouper(key='date', freq=freq_map[agg_level]))['revenue'].sum().reset_index()
    
    fig = px.line(
        monthly_revenue,
        x='date',
        y='revenue',
        title=f'{agg_level} Revenue Trend',
        labels={'date': 'Date', 'revenue': 'Revenue (₹)'},
        markers=True
    )
    fig.update_layout(
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Channel Performance
    st.subheader("📊 Revenue by Channel")
    
    # Metric selector
    col1, col2 = st.columns([3, 1])
    with col2:
        metric = st.selectbox(
            "Metric",
            ["Revenue", "Conversions", "ROAS"],
            key="channel_metric"
        )
    
    metric_col = metric.lower() if metric in ['Revenue', 'Conversions'] else 'roas'
    channel_data = campaigns.groupby('channel')[metric_col].sum().sort_values(ascending=True).reset_index()
    
    fig = px.bar(
        channel_data,
        x=metric_col,
        y='channel',
        orientation='h',
        title=f'Total {metric} by Marketing Channel',
        labels={metric_col: f'{metric} (₹)' if metric != 'ROAS' else f'{metric}', 'channel': 'Channel'},
        color='channel',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(height=400, showlegend=False, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: CAMPAIGN ANALYTICS
# =============================================================================
def page_campaign_analytics(data):
    """Campaign Analytics - Temporal and comparison analysis"""
    st.title("📈 Campaign Analytics")
    st.markdown("Analyze campaign performance across channels, regions, and time periods")
    
    campaigns = data['campaigns']
    
    # Filters in expandable section
    with st.expander("🔍 Filter Options", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_channels = st.multiselect(
                "Select Channels",
                options=sorted(campaigns['channel'].unique()),
                default=sorted(campaigns['channel'].unique())
            )
        
        with col2:
            selected_regions = st.multiselect(
                "Select Regions",
                options=sorted(campaigns['region'].unique()),
                default=sorted(campaigns['region'].unique())
            )
        
        with col3:
            date_range = st.date_input(
                "Date Range",
                value=(campaigns['date'].min(), campaigns['date'].max()),
                min_value=campaigns['date'].min(),
                max_value=campaigns['date'].max()
            )
    
    # Apply filters
    filtered = campaigns[
        (campaigns['channel'].isin(selected_channels)) &
        (campaigns['region'].isin(selected_regions)) &
        (campaigns['date'] >= pd.to_datetime(date_range[0])) &
        (campaigns['date'] <= pd.to_datetime(date_range[1]))
    ]
    
    if filtered.empty:
        st.warning("⚠️ No data available for selected filters")
        return
    
    st.markdown("---")
    
    # Regional Performance by Quarter
    st.subheader("📊 Regional Performance by Quarter")
    
    regional_quarterly = filtered.groupby(['region', 'quarter'])['revenue'].sum().reset_index()
    
    fig = px.bar(
        regional_quarterly,
        x='quarter',
        y='revenue',
        color='region',
        barmode='group',
        title='Revenue by Region and Quarter',
        labels={'revenue': 'Revenue (₹)', 'quarter': 'Quarter', 'region': 'Region'}
    )
    fig.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    # Channel Contribution Over Time
    st.subheader("📈 Channel Contribution Over Time")
    
    channel_time = filtered.groupby([pd.Grouper(key='date', freq='W'), 'channel'])['conversions'].sum().reset_index()
    
    fig = px.area(
        channel_time,
        x='date',
        y='conversions',
        color='channel',
        title='Weekly Conversions by Channel (Stacked)',
        labels={'date': 'Week', 'conversions': 'Conversions', 'channel': 'Channel'}
    )
    fig.update_layout(height=400, hovermode='x unified', template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    # Campaign Type Breakdown
    st.subheader("💰 Campaign Type Spend Distribution")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        view_type = st.selectbox("View", ["Absolute", "100% Stacked"], key="campaign_view")
    
    campaign_monthly = filtered.groupby([pd.Grouper(key='date', freq='M'), 'campaign_type'])['spend'].sum().reset_index()
    
    if view_type == "100% Stacked":
        fig = px.bar(
            campaign_monthly,
            x='date',
            y='spend',
            color='campaign_type',
            barmode='relative',
            title='Campaign Type Contribution (100% Stacked)',
            labels={'spend': 'Spend %', 'date': 'Month', 'campaign_type': 'Campaign Type'}
        )
    else:
        fig = px.bar(
            campaign_monthly,
            x='date',
            y='spend',
            color='campaign_type',
            barmode='stack',
            title='Campaign Type Spend (Absolute)',
            labels={'spend': 'Spend (₹)', 'date': 'Month', 'campaign_type': 'Campaign Type'}
        )
    
    fig.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: CUSTOMER INSIGHTS
# =============================================================================
def page_customer_insights(data):
    """Customer Insights - Distributions and relationships"""
    st.title("👥 Customer Insights")
    st.markdown("Analyze customer demographics, behavior, and lifetime value")
    
    customers = data['customers']
    
    col1, col2 = st.columns(2)
    
    # Age Distribution
    with col1:
        st.subheader("📊 Age Distribution")
        
        bin_size = st.slider("Bin Width", min_value=2, max_value=10, value=5, key="age_bin")
        
        fig = px.histogram(
            customers,
            x='age',
            nbins=int((customers['age'].max() - customers['age'].min()) / bin_size),
            title='Customer Age Distribution',
            labels={'age': 'Age', 'count': 'Number of Customers'},
            color_discrete_sequence=['#636EFA'],
            marginal='box'
        )
        fig.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    # LTV by Segment
    with col2:
        st.subheader("📦 Lifetime Value by Segment")
        
        fig = px.box(
            customers,
            x='customer_segment',
            y='lifetime_value',
            color='customer_segment',
            title='LTV Distribution by Customer Segment',
            labels={'customer_segment': 'Segment', 'lifetime_value': 'Lifetime Value (₹)'},
            points='outliers'
        )
        fig.update_layout(height=400, showlegend=False, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Income vs LTV Scatter
    st.subheader("🔵 Income vs Lifetime Value")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        show_trend = st.checkbox("Show Trend Line", value=False)
    
    # Create scatter plot
    fig = px.scatter(
        customers,
        x='income',
        y='lifetime_value',
        color='customer_segment',
        size='total_purchases',
        hover_data=['age', 'tenure_months', 'satisfaction_score'],
        title='Income vs Lifetime Value by Customer Segment',
        labels={'income': 'Annual Income (₹)', 'lifetime_value': 'Lifetime Value (₹)', 'customer_segment': 'Segment'},
        opacity=0.7
    )
    
    # Add trend line if selected (without grouping by color)
    if show_trend:
        try:
            from scipy import stats
            # Calculate overall trend line
            valid_data = customers.dropna(subset=['income', 'lifetime_value'])
            slope, intercept, r_value, p_value, std_err = stats.linregress(valid_data['income'], valid_data['lifetime_value'])
            x_trend = np.array([customers['income'].min(), customers['income'].max()])
            y_trend = slope * x_trend + intercept
            
            fig.add_trace(go.Scatter(
                x=x_trend, 
                y=y_trend,
                mode='lines',
                name=f'Trend (R²={r_value**2:.3f})',
                line=dict(color='red', width=2, dash='dash'),
                hovertemplate='Trend Line<br>Income: ₹%{x:,.0f}<br>LTV: ₹%{y:,.0f}<extra></extra>'
            ))
        except ImportError:
            st.warning("⚠️ Install scipy for trend line: pip install scipy")
    
    fig.update_layout(height=450, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Satisfaction Distribution
    st.subheader("😊 Satisfaction Score by NPS Category")
    
    fig = px.violin(
        customers,
        x='nps_category',
        y='satisfaction_score',
        color='nps_category',
        box=True,
        points='outliers',
        title='Satisfaction Distribution by NPS Category',
        labels={'nps_category': 'NPS Category', 'satisfaction_score': 'Satisfaction Score'}
    )
    fig.update_layout(height=400, showlegend=False, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: PRODUCT PERFORMANCE
# =============================================================================
def page_product_performance(data):
    """Product Performance - Hierarchy and category analysis"""
    st.title("📦 Product Performance")
    st.markdown("Explore product sales, margins, and category performance")
    
    products = data['products']
    
    # Product Hierarchy Treemap
    st.subheader("🌳 Product Sales Hierarchy")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        color_metric = st.selectbox(
            "Color by",
            ["profit_margin", "sales", "units_sold"],
            key="treemap_color"
        )
    
    fig = px.treemap(
        products,
        path=['category', 'subcategory', 'product_name'],
        values='sales',
        color=color_metric,
        color_continuous_scale='RdYlGn' if color_metric == 'profit_margin' else 'Blues',
        title=f'Product Sales Hierarchy (Size: Sales, Color: {color_metric.replace("_", " ").title()})',
        hover_data=['profit_margin', 'sales', 'units_sold']
    )
    fig.update_layout(height=600, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Category Performance
    st.subheader("📊 Category Performance by Region")
    
    category_region = products.groupby(['category', 'region']).agg({
        'sales': 'sum',
        'profit_margin': 'mean',
        'units_sold': 'sum'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.sunburst(
            category_region,
            path=['category', 'region'],
            values='sales',
            title='Sales Distribution: Category → Region',
            color='profit_margin',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=500, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top products table
        st.subheader("Top Products by Sales")
        
        top_products = products.nlargest(10, 'sales')[['product_name', 'category', 'sales', 'profit_margin', 'region']]
        
        st.dataframe(
            top_products.style.format({
                'sales': '₹{:,.0f}',
                'profit_margin': '{:.1f}%'
            }),
            use_container_width=True,
            height=500
        )

# =============================================================================
# PAGE: GEOGRAPHIC ANALYSIS
# =============================================================================
def page_geographic_analysis(data):
    """Geographic Analysis - State-level metrics"""
    st.title("🗺️ Geographic Analysis")
    st.markdown("Explore state-level performance metrics across India")
    
    geo = data['geographic']
    
    col1, col2 = st.columns([3, 1])
    with col2:
        metric = st.selectbox(
            "Metric",
            ['total_revenue', 'total_customers', 'market_penetration', 'yoy_growth', 'customer_satisfaction'],
            key="geo_metric"
        )
    
    # Bubble Map
    st.subheader("📍 State-wise Performance Map")
    
    fig = px.scatter_geo(
        geo,
        lat='latitude',
        lon='longitude',
        size=metric,
        color='customer_satisfaction',
        hover_name='state',
        hover_data=['total_revenue', 'total_customers', 'store_count', 'market_penetration'],
        title=f'State Performance - {metric.replace("_", " ").title()}',
        size_max=50,
        color_continuous_scale='RdYlGn',
        scope='asia',
        projection='natural earth'
    )
    
    fig.update_geos(
        center=dict(lat=20.5937, lon=78.9629),
        projection_scale=4,
        showland=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(200, 200, 200)'
    )
    fig.update_layout(height=600, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # State Metrics Table
    st.subheader("📊 State-wise Metrics Table")
    
    display_cols = ['state', 'region', 'total_customers', 'total_revenue', 'market_penetration', 'yoy_growth', 'customer_satisfaction']
    geo_display = geo[display_cols].sort_values('total_revenue', ascending=False)
    
    st.dataframe(
        geo_display.style.format({
            'total_revenue': '₹{:,.0f}',
            'market_penetration': '{:.1f}%',
            'yoy_growth': '{:.1f}%',
            'customer_satisfaction': '{:.1f}%'
        }),
        use_container_width=True
    )

# =============================================================================
# PAGE: ATTRIBUTION & FUNNEL
# =============================================================================
def page_attribution_funnel(data):
    """Attribution & Funnel - Attribution models and conversion funnel"""
    st.title("🎯 Attribution & Funnel Analysis")
    st.markdown("Understand channel attribution and customer journey conversion")
    
    attribution = data['attribution']
    funnel = data['funnel']
    correlation = data['correlation']
    
    col1, col2 = st.columns(2)
    
    # Attribution Model
    with col1:
        st.subheader("🍩 Channel Attribution")
        
        model = st.selectbox(
            "Select Attribution Model",
            ['first_touch', 'last_touch', 'linear', 'time_decay', 'position_based'],
            format_func=lambda x: x.replace('_', ' ').title(),
            key="attribution_model"
        )
        
        fig = px.pie(
            attribution,
            values=model,
            names='channel',
            hole=0.4,
            title=f'Channel Attribution - {model.replace("_", " ").title()}',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=500, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    # Funnel
    with col2:
        st.subheader("🔻 Conversion Funnel")
        
        funnel_sorted = funnel.sort_values('stage', ascending=True)
        
        # Use conversion_rate as the funnel metric if visitors not available
        funnel_metric = 'visitors' if 'visitors' in funnel_sorted.columns else 'conversion_rate'
        
        fig = go.Figure(go.Funnel(
            y=funnel_sorted['stage'],
            x=funnel_sorted[funnel_metric],
            textinfo="value+percent initial",
            marker=dict(color=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3'][:len(funnel)])
        ))
        fig.update_layout(
            title='Marketing Funnel - Conversion by Stage',
            height=500,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Funnel Metrics
    st.subheader("📈 Funnel Conversion Rates")
    
    funnel_calc = funnel.copy().sort_values('visitors', ascending=False)
    
    # Calculate conversion_rate if it doesn't exist, otherwise use existing
    if 'conversion_rate' not in funnel_calc.columns:
        funnel_calc['conversion_rate'] = (funnel_calc['conversions'] / funnel_calc['visitors'] * 100).round(2)
    else:
        # Ensure conversion_rate is numeric
        funnel_calc['conversion_rate'] = pd.to_numeric(funnel_calc['conversion_rate'], errors='coerce')
    
    # Calculate drop_off if conversions column exists
    if 'conversions' in funnel_calc.columns:
        funnel_calc['drop_off'] = funnel_calc['conversions'].shift(1) - funnel_calc['conversions']
        funnel_calc['drop_off_pct'] = (funnel_calc['drop_off'] / funnel_calc['conversions'].shift(1) * 100).round(2)
        
        st.dataframe(
            funnel_calc[['stage', 'conversions', 'conversion_rate', 'drop_off_pct']].style.format({
                'conversions': '{:,.0f}',
                'conversion_rate': '{:.2f}%',
                'drop_off_pct': '{:.2f}%'
            }),
            use_container_width=True
        )
    else:
        # If only conversion_rate data available, display that
        st.dataframe(
            funnel_calc[['stage', 'conversion_rate']].style.format({
                'conversion_rate': '{:.2f}%'
            }),
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Correlation Heatmap
    st.subheader("🔥 Metric Correlation Matrix")
    
    fig = px.imshow(
        correlation,
        text_auto='.2f',
        aspect='auto',
        color_continuous_scale='RdBu_r',
        color_continuous_midpoint=0,
        title='Correlation Between Marketing Metrics',
        labels=dict(color='Correlation')
    )
    fig.update_layout(height=600, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: ML MODEL EVALUATION
# =============================================================================
def page_ml_evaluation(data):
    """ML Model Evaluation - Confusion matrix, ROC, learning curve, feature importance"""
    st.title("🤖 ML Model Evaluation")
    st.markdown("Lead Scoring Model Performance Analysis")
    
    leads = data['leads']
    feature_imp = data['feature_importance']
    learning = data['learning_curve']
    
    col1, col2 = st.columns(2)
    
    # Confusion Matrix
    with col1:
        st.subheader("📊 Confusion Matrix")
        
        threshold = st.slider(
            "Classification Threshold",
            0.0, 1.0, 0.5, 0.05,
            key="confusion_threshold"
        )
        
        y_true = leads['actual_converted']
        y_pred = (leads['predicted_probability'] >= threshold).astype(int)
        
        cm = confusion_matrix(y_true, y_pred)
        
        fig = px.imshow(
            cm,
            labels=dict(x="Predicted", y="Actual", color="Count"),
            x=['Not Converted', 'Converted'],
            y=['Not Converted', 'Converted'],
            text_auto=True,
            color_continuous_scale='Blues',
            title=f'Confusion Matrix (Threshold: {threshold})',
            aspect='auto'
        )
        fig.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate metrics
        tn, fp, fn, tp = cm.ravel()
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        metric_cols = st.columns(4)
        with metric_cols[0]:
            st.metric("Accuracy", f"{accuracy:.3f}")
        with metric_cols[1]:
            st.metric("Precision", f"{precision:.3f}")
        with metric_cols[2]:
            st.metric("Recall", f"{recall:.3f}")
        with metric_cols[3]:
            st.metric("F1 Score", f"{f1:.3f}")
    
    # ROC Curve
    with col2:
        st.subheader("📈 ROC Curve & AUC")
        
        fpr, tpr, thresholds = roc_curve(leads['actual_converted'], leads['predicted_probability'])
        roc_auc = auc(fpr, tpr)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fpr, y=tpr,
            mode='lines',
            name=f'ROC Curve (AUC = {roc_auc:.3f})',
            line=dict(color='#636EFA', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1],
            mode='lines',
            name='Random Classifier',
            line=dict(color='gray', dash='dash')
        ))
        
        fig.update_layout(
            title='ROC Curve - Model Performance',
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate',
            height=400,
            template='plotly_white',
            legend=dict(x=0.6, y=0.1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("ROC AUC Score", f"{roc_auc:.3f}")
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    # Feature Importance
    with col3:
        st.subheader("🎯 Feature Importance")
        
        feature_imp_sorted = feature_imp.sort_values('importance', ascending=True)
        
        fig = px.bar(
            feature_imp_sorted,
            x='importance',
            y='feature',
            orientation='h',
            error_x='importance_std' if 'importance_std' in feature_imp_sorted.columns else None,
            title='Feature Importance with Standard Deviation',
            labels={'importance': 'Importance Score', 'feature': 'Feature'},
            color='importance',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400, showlegend=False, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    # Learning Curve
    with col4:
        st.subheader("📚 Learning Curve")
        
        fig = go.Figure()
        
        # Training score
        fig.add_trace(go.Scatter(
            x=learning['training_size'],
            y=learning['train_score'],
            mode='lines+markers',
            name='Training Score',
            line=dict(color='#636EFA', width=2),
            marker=dict(size=8)
        ))
        
        # Validation score
        fig.add_trace(go.Scatter(
            x=learning['training_size'],
            y=learning['validation_score'],
            mode='lines+markers',
            name='Validation Score',
            line=dict(color='#00CC96', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Learning Curve - Training vs Validation',
            xaxis_title='Training Set Size',
            yaxis_title='Score',
            height=400,
            template='plotly_white',
            yaxis=dict(range=[0.4, 1.0])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Precision-Recall Curve (Bonus)
    st.subheader("📊 Precision-Recall Curve")
    
    precision_vals, recall_vals, _ = precision_recall_curve(leads['actual_converted'], leads['predicted_probability'])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=recall_vals, y=precision_vals,
        mode='lines',
        name='Precision-Recall',
        line=dict(color='#AB63FA', width=3)
    ))
    
    fig.update_layout(
        title='Precision-Recall Curve',
        xaxis_title='Recall',
        yaxis_title='Precision',
        height=400,
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# MAIN APPLICATION
# =============================================================================
def main():
    """Main application router"""
    
    # Load data
    data = load_data()
    
    if data is None:
        st.stop()
    
    # Sidebar navigation
    page = sidebar()
    
    # Route to pages
    if page == "🏠 Executive Overview":
        page_executive_overview(data)
    elif page == "📈 Campaign Analytics":
        page_campaign_analytics(data)
    elif page == "👥 Customer Insights":
        page_customer_insights(data)
    elif page == "📦 Product Performance":
        page_product_performance(data)
    elif page == "🗺️ Geographic Analysis":
        page_geographic_analysis(data)
    elif page == "🎯 Attribution & Funnel":
        page_attribution_funnel(data)
    elif page == "🤖 ML Model Evaluation":
        page_ml_evaluation(data)

if __name__ == "__main__":
    main()
