import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.5s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-change {
        font-size: 12px;
        margin-top: 8px;
        font-weight: 600;
    }
    
    .positive {
        color: #4ade80;
    }
    
    .negative {
        color: #f87171;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .header-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 20px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    
    .stMetric {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'data' not in st.session_state:
    st.session_state.data = None
if 'date_range' not in st.session_state:
    st.session_state.date_range = None

@st.cache_data
def generate_sample_data(n_records=1000):
    """Generate realistic synthetic e-commerce data"""
    np.random.seed(42)
    
    dates = pd.date_range(start='2023-01-01', end='2024-03-20', freq='D')
    data = []
    
    for _ in range(n_records):
        date = np.random.choice(dates)
        product = np.random.choice(['Laptop', 'Phone', 'Tablet', 'Headphones', 'Monitor', 'Keyboard', 'Mouse', 'Charger'])
        quantity = np.random.randint(1, 5)
        
        # Price varies by product
        prices = {
            'Laptop': 1200, 'Phone': 800, 'Tablet': 500, 'Headphones': 150,
            'Monitor': 400, 'Keyboard': 100, 'Mouse': 50, 'Charger': 30
        }
        unit_price = prices[product] + np.random.randint(-50, 50)
        revenue = quantity * unit_price
        cost = revenue * np.random.uniform(0.4, 0.6)
        profit = revenue - cost
        
        customer_id = np.random.randint(1000, 5000)
        category = np.random.choice(['Electronics', 'Accessories'])
        
        data.append({
            'Date': date,
            'Product': product,
            'Category': category,
            'Quantity': quantity,
            'Unit_Price': unit_price,
            'Revenue': revenue,
            'Cost': cost,
            'Profit': profit,
            'Customer_ID': customer_id,
            'Region': np.random.choice(['North', 'South', 'East', 'West'])
        })
    
    return pd.DataFrame(data)

@st.cache_data
def load_data(uploaded_file=None):
    """Load data from file or generate sample data"""
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return generate_sample_data()

def format_currency(value):
    """Format value as currency"""
    return f"${value:,.0f}"

def calculate_metrics(df, date_range=None):
    """Calculate key metrics"""
    if date_range:
        df = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]
    
    total_revenue = df['Revenue'].sum()
    total_profit = df['Profit'].sum()
    total_orders = len(df)
    unique_customers = df['Customer_ID'].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    return {
        'revenue': total_revenue,
        'profit': total_profit,
        'orders': total_orders,
        'customers': unique_customers,
        'avg_order_value': avg_order_value,
        'profit_margin': profit_margin
    }

def render_metric_card(col, label, value, change=None, icon="📊"):
    """Render a styled metric card"""
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 24px; margin-bottom: 5px;">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {f'<div class="metric-change"><span class="positive">▲ {change}%</span></div>' if change and change > 0 else f'<div class="metric-change"><span class="negative">▼ {abs(change) if change else 0}%</span></div>' if change else ''}
        </div>
        """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Dashboard Controls")
    
    # Data source selection
    data_source = st.radio("Data Source", ["Sample Data", "Upload CSV"])
    
    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file:
            st.session_state.data = load_data(uploaded_file)
    else:
        st.session_state.data = load_data()
    
    if st.session_state.data is not None:
        st.markdown("---")
        st.markdown("### 📅 Date Range Filter")
        
        min_date = st.session_state.data['Date'].min().date()
        max_date = st.session_state.data['Date'].max().date()
        
        date_range = st.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            st.session_state.date_range = (pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]))
        
        st.markdown("---")
        st.markdown("### 🎯 Quick Filters")
        
        selected_category = st.multiselect(
            "Category",
            options=st.session_state.data['Category'].unique(),
            default=st.session_state.data['Category'].unique()
        )
        
        selected_region = st.multiselect(
            "Region",
            options=st.session_state.data['Region'].unique(),
            default=st.session_state.data['Region'].unique()
        )

# Main content
if st.session_state.data is not None:
    df = st.session_state.data.copy()
    
    # Apply filters
    if 'selected_category' in locals():
        df = df[df['Category'].isin(selected_category)]
    if 'selected_region' in locals():
        df = df[df['Region'].isin(selected_region)]
    
    st.markdown('<div class="header-title">📊 E-Commerce Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # KPI Cards
    metrics = calculate_metrics(df, st.session_state.date_range)
    
    col1, col2, col3, col4 = st.columns(4)
    render_metric_card(col1, "Total Revenue", format_currency(metrics['revenue']), icon="💰")
    render_metric_card(col2, "Total Profit", format_currency(metrics['profit']), icon="📈")
    render_metric_card(col3, "Total Orders", f"{metrics['orders']:,}", icon="🛒")
    render_metric_card(col4, "Customers", f"{metrics['customers']:,}", icon="👥")
    
    st.markdown("---")
    
    # Revenue and Profit Trends
    st.markdown('<div class="section-header">📈 Revenue & Profit Trends</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        daily_revenue = df.groupby(df['Date'].dt.date)['Revenue'].sum().reset_index()
        fig_revenue = px.line(
            daily_revenue,
            x='Date',
            y='Revenue',
            title='Daily Revenue Trend',
            markers=True,
            template='plotly_white'
        )
        fig_revenue.update_traces(line=dict(color='#667eea', width=3))
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        daily_profit = df.groupby(df['Date'].dt.date)['Profit'].sum().reset_index()
        fig_profit = px.line(
            daily_profit,
            x='Date',
            y='Profit',
            title='Daily Profit Trend',
            markers=True,
            template='plotly_white'
        )
        fig_profit.update_traces(line=dict(color='#764ba2', width=3))
        st.plotly_chart(fig_profit, use_container_width=True)
    
    st.markdown("---")
    
    # Product Performance
    st.markdown('<div class="section-header">🏆 Top Products by Revenue</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_revenue = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(8)
        fig_products = px.bar(
            x=product_revenue.values,
            y=product_revenue.index,
            orientation='h',
            title='Top 8 Products by Revenue',
            template='plotly_white',
            color=product_revenue.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_products, use_container_width=True)
    
    with col2:
        product_profit = df.groupby('Product')['Profit'].sum().sort_values(ascending=False).head(8)
        fig_profit_products = px.bar(
            x=product_profit.values,
            y=product_profit.index,
            orientation='h',
            title='Top 8 Products by Profit',
            template='plotly_white',
            color=product_profit.values,
            color_continuous_scale='Plasma'
        )
        st.plotly_chart(fig_profit_products, use_container_width=True)
    
    st.markdown("---")
    
    # Category and Region Analysis
    st.markdown('<div class="section-header">🗺️ Sales by Category & Region</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        category_sales = df.groupby('Category')['Revenue'].sum()
        fig_category = px.pie(
            values=category_sales.values,
            names=category_sales.index,
            title='Revenue Distribution by Category',
            template='plotly_white'
        )
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        region_sales = df.groupby('Region')['Revenue'].sum()
        fig_region = px.pie(
            values=region_sales.values,
            names=region_sales.index,
            title='Revenue Distribution by Region',
            template='plotly_white'
        )
        st.plotly_chart(fig_region, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed Metrics
    st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Order Value", format_currency(metrics['avg_order_value']))
    with col2:
        st.metric("Profit Margin", f"{metrics['profit_margin']:.1f}%")
    with col3:
        repeat_customers = df.groupby('Customer_ID').size()
        repeat_rate = (repeat_customers[repeat_customers > 1].count() / len(repeat_customers) * 100)
        st.metric("Repeat Customer Rate", f"{repeat_rate:.1f}%")
    with col4:
        customer_ltv = df.groupby('Customer_ID')['Profit'].sum().mean()
        st.metric("Avg Customer LTV", format_currency(customer_ltv))
    
    st.markdown("---")
    
    # Data Table
    st.markdown('<div class="section-header">📋 Recent Transactions</div>', unsafe_allow_html=True)
    
    display_df = df.sort_values('Date', ascending=False).head(20).copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f"${x:,.0f}")
    display_df['Profit'] = display_df['Profit'].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #667eea; font-size: 12px; margin-top: 20px;'>📊 E-Commerce Analytics Dashboard | Last Updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "</div>", unsafe_allow_html=True)

else:
    st.info("👈 Please configure your data source in the sidebar to get started!")
