import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu
from streamlit_extras.colored_header import colored_header
import warnings
import os
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="E-Commerce Analytics Pro",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.gradient-text {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    font-size: 2.5rem;
}
.metric-card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in {
    animation: fadeIn 0.8s ease-out;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df' not in st.session_state:
    st.session_state.df = None

@st.cache_data(ttl=3600)
def load_olist_data():
    """Load Olist dataset with flexible file detection"""
    try:
        # Check which files are available
        files = {
            'customers': 'olist_customers_dataset.csv',
            'orders': 'olist_orders_dataset.csv',
            'order_items': 'olist_order_items_dataset.csv',
            'products': 'olist_products_dataset.csv',
            'payments': 'olist_order_payments_dataset.csv',
            'reviews': 'olist_order_reviews_dataset.csv',
        }
        
        available = {k: os.path.exists(v) for k, v in files.items()}
        
        # Load customers (required)
        if not available['customers']:
            st.error("❌ Customers dataset not found!")
            return None
        
        customers = pd.read_csv(files['customers'])
        st.success("✅ Customers dataset loaded")
        
        # If only customers available, return it
        if not available['orders']:
            st.warning("⚠️ Orders dataset not found. Using customers data only.")
            df = customers.copy()
            df['order_date'] = pd.Timestamp.now()
            df['sales_amount'] = 0
            df['profit'] = 0
            df['customer_segment'] = 'Customer'
            df['region'] = df.get('customer_state', 'Unknown')
            df['city'] = df.get('customer_city', 'Unknown')
            return df
        
        # Load orders
        orders = pd.read_csv(files['orders'])
        st.success("✅ Orders dataset loaded")
        df = orders.copy()
        
        # Load and merge other datasets
        if available['order_items']:
            order_items = pd.read_csv(files['order_items'])
            df = df.merge(order_items, on='order_id', how='left')
            st.success("✅ Order items dataset loaded")
        
        if available['products']:
            products = pd.read_csv(files['products'])
            if 'product_id' in df.columns:
                df = df.merge(products, on='product_id', how='left')
                st.success("✅ Products dataset loaded")
        
        if available['payments']:
            payments = pd.read_csv(files['payments'])
            df = df.merge(payments, on='order_id', how='left')
            st.success("✅ Payments dataset loaded")
        
        if available['reviews']:
            reviews = pd.read_csv(files['reviews'])
            df = df.merge(reviews, on='order_id', how='left')
            st.success("✅ Reviews dataset loaded")
        
        # Merge customers
        df = df.merge(customers, on='customer_id', how='left')
        st.success("✅ Customers dataset merged")
        
        # Data preprocessing
        if 'order_purchase_timestamp' in df.columns:
            df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
            df['order_date'] = df['order_purchase_timestamp']
        
        if 'order_delivered_customer_date' in df.columns:
            df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'], errors='coerce')
        
        # Calculate metrics
        if 'price' in df.columns:
            df['cost'] = df['price'] * 0.7
            df['profit'] = df['price'] - df['cost']
            df['profit_margin'] = (df['profit'] / df['price'] * 100).fillna(0)
            df['sales_amount'] = df['price']
        else:
            df['sales_amount'] = 0
            df['profit'] = 0
            df['profit_margin'] = 0
        
        # Set default values
        if 'customer_segment' not in df.columns:
            df['customer_segment'] = 'Customer'
        
        if 'region' not in df.columns:
            df['region'] = df.get('customer_state', 'Unknown')
        
        if 'city' not in df.columns:
            df['city'] = df.get('customer_city', 'Unknown')
        
        if 'product_category' not in df.columns:
            df['product_category'] = df.get('product_category_name', 'Unknown')
        
        if 'product_name' not in df.columns:
            df['product_name'] = 'Product'
        
        if 'review_score' in df.columns:
            df['customer_rating'] = df['review_score']
        elif 'customer_rating' not in df.columns:
            df['customer_rating'] = 0
        
        # Extract date features
        if 'order_date' in df.columns:
            df['year'] = df['order_date'].dt.year
            df['month'] = df['order_date'].dt.month
            df['quarter'] = df['order_date'].dt.quarter
            df['day_of_week'] = df['order_date'].dt.day_name()
            df['hour'] = df['order_date'].dt.hour
        
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

@st.cache_data
def load_sample_data():
    """Generate sample data"""
    np.random.seed(42)
    categories = {
        'Electronics': ['Smartphones', 'Laptops', 'Tablets'],
        'Fashion': ['Men\'s Clothing', 'Women\'s Clothing'],
        'Home': ['Furniture', 'Decor'],
    }
    
    data = []
    for i in range(1000):
        category = np.random.choice(list(categories.keys()))
        data.append({
            'order_id': f'ORD-{i:05d}',
            'order_date': pd.Timestamp('2023-01-01') + pd.Timedelta(days=np.random.randint(0, 365)),
            'customer_id': f'CUST-{np.random.randint(1000, 2000):04d}',
            'customer_segment': np.random.choice(['Premium', 'Regular', 'Occasional']),
            'region': np.random.choice(['North', 'South', 'East', 'West']),
            'city': np.random.choice(['New York', 'Los Angeles', 'Chicago']),
            'product_category': category,
            'product_name': f'{category} Product {i}',
            'quantity': np.random.randint(1, 5),
            'sales_amount': np.random.uniform(50, 500),
            'profit': np.random.uniform(10, 200),
            'profit_margin': np.random.uniform(10, 50),
            'customer_rating': np.random.choice([1, 2, 3, 4, 5]),
        })
    return pd.DataFrame(data)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/null/shopaholic.png", width=80)
    st.markdown("<h1 style='text-align: center;'>E‑COMMERCE<br>ANALYTICS</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Products", "Customers", "Geography", "Forecast", "Reports"],
        icons=["speedometer2", "box", "people", "geo-alt", "graph-up", "file-text"],
        menu_icon="cast",
        default_index=0,
    )
    
    st.markdown("---")
    
    data_source = st.radio("📊 Data Source", ["Olist Dataset", "Sample Data", "Upload CSV"])
    
    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
        if uploaded_file:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.session_state.data_loaded = True
            st.success("✅ Data loaded!")
    elif data_source == "Olist Dataset":
        if st.button("📥 Load Olist Data"):
            with st.spinner("Loading Olist dataset..."):
                st.session_state.df = load_olist_data()
                if st.session_state.df is not None:
                    st.session_state.data_loaded = True
    else:
        st.session_state.df = load_sample_data()
        st.session_state.data_loaded = True
        st.info("📊 Using sample data")

# Main content
if st.session_state.data_loaded and st.session_state.df is not None:
    df = st.session_state.df.copy()
    
    if selected == "Dashboard":
        st.markdown("<h1 class='gradient-text fade-in'>📊 Executive Dashboard</h1>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_revenue = df['sales_amount'].sum()
            st.markdown(f"""
            <div class='metric-card fade-in'>
            <h3 style='color: #666; font-size: 14px;'>TOTAL REVENUE</h3>
            <h2 style='color: #2c3e50; font-size: 28px;'>${total_revenue:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_profit = df['profit'].sum()
            st.markdown(f"""
            <div class='metric-card fade-in'>
            <h3 style='color: #666; font-size: 14px;'>TOTAL PROFIT</h3>
            <h2 style='color: #2c3e50; font-size: 28px;'>${total_profit:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_orders = df['order_id'].nunique()
            st.markdown(f"""
            <div class='metric-card fade-in'>
            <h3 style='color: #666; font-size: 14px;'>TOTAL ORDERS</h3>
            <h2 style='color: #2c3e50; font-size: 28px;'>{total_orders:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_customers = df['customer_id'].nunique()
            st.markdown(f"""
            <div class='metric-card fade-in'>
            <h3 style='color: #666; font-size: 14px;'>CUSTOMERS</h3>
            <h2 style='color: #2c3e50; font-size: 28px;'>{total_customers:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if 'order_date' in df.columns and df['order_date'].notna().any():
                daily_sales = df.groupby(df['order_date'].dt.date)['sales_amount'].sum().reset_index()
                fig = px.line(daily_sales, x='order_date', y='sales_amount', title='Daily Revenue', markers=True)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'product_category' in df.columns:
                category_sales = df.groupby('product_category')['sales_amount'].sum()
                fig = px.pie(values=category_sales.values, names=category_sales.index, title='Revenue by Category')
                st.plotly_chart(fig, use_container_width=True)
    
    elif selected == "Products":
        st.markdown("<h1 class='gradient-text'>📦 Product Analysis</h1>", unsafe_allow_html=True)
        
        if 'product_name' in df.columns:
            product_stats = df.groupby('product_name').agg({
                'sales_amount': 'sum',
                'profit': 'sum',
                'order_id': 'count'
            }).sort_values('profit', ascending=False).head(10)
            
            st.dataframe(product_stats, use_container_width=True)
            
            fig = px.bar(product_stats.reset_index(), x='profit', y='product_name', orientation='h', title='Top Products by Profit')
            st.plotly_chart(fig, use_container_width=True)
    
    elif selected == "Customers":
        st.markdown("<h1 class='gradient-text'>👥 Customer Analytics</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Customers", df['customer_id'].nunique())
        with col2:
            st.metric("Avg Order Value", f"${df['sales_amount'].mean():,.0f}")
        
        if 'customer_segment' in df.columns:
            segment_data = df.groupby('customer_segment')['sales_amount'].sum()
            fig = px.pie(values=segment_data.values, names=segment_data.index, title='Revenue by Segment')
            st.plotly_chart(fig, use_container_width=True)
    
    elif selected == "Geography":
        st.markdown("<h1 class='gradient-text'>🌍 Geographic Analysis</h1>", unsafe_allow_html=True)
        
        if 'region' in df.columns:
            region_sales = df.groupby('region')['sales_amount'].sum()
            fig = px.bar(x=region_sales.index, y=region_sales.values, title='Sales by Region')
            st.plotly_chart(fig, use_container_width=True)
        
        if 'city' in df.columns:
            city_sales = df.groupby('city')['sales_amount'].sum().sort_values(ascending=False).head(10)
            fig = px.bar(x=city_sales.index, y=city_sales.values, title='Top 10 Cities')
            st.plotly_chart(fig, use_container_width=True)
    
    elif selected == "Forecast":
        st.markdown("<h1 class='gradient-text'>🔮 Sales Forecast</h1>", unsafe_allow_html=True)
        
        if 'order_date' in df.columns and df['order_date'].notna().any():
            from sklearn.linear_model import LinearRegression
            
            daily_sales = df.groupby(df['order_date'].dt.date)['sales_amount'].sum().reset_index()
            daily_sales['date'] = pd.to_datetime(daily_sales['order_date'])
            daily_sales['day_num'] = (daily_sales['date'] - daily_sales['date'].min()).dt.days
            
            X = daily_sales['day_num'].values.reshape(-1, 1)
            y = daily_sales['sales_amount'].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            future_days = 30
            future_X = np.array(range(X.max() + 1, X.max() + future_days + 1)).reshape(-1, 1)
            future_pred = model.predict(future_X)
            
            future_dates = pd.date_range(start=daily_sales['date'].max() + pd.Timedelta(days=1), periods=future_days)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily_sales['date'], y=daily_sales['sales_amount'], name='Historical'))
            fig.add_trace(go.Scatter(x=future_dates, y=future_pred, name='Forecast', line=dict(dash='dash')))
            st.plotly_chart(fig, use_container_width=True)
    
    elif selected == "Reports":
        st.markdown("<h1 class='gradient-text'>📄 Reports</h1>", unsafe_allow_html=True)
        
        report_type = st.selectbox("Select Report", ["Summary", "Products", "Customers"])
        
        if st.button("Generate Report"):
            if report_type == "Summary":
                report_data = {
                    'Metric': ['Total Revenue', 'Total Profit', 'Total Orders', 'Total Customers'],
                    'Value': [f"${df['sales_amount'].sum():,.0f}", f"${df['profit'].sum():,.0f}", 
                             f"{df['order_id'].nunique():,}", f"{df['customer_id'].nunique():,}"]
                }
            elif report_type == "Products":
                report_data = df.groupby('product_name').agg({'sales_amount': 'sum', 'profit': 'sum'}).reset_index()
            else:
                report_data = df.groupby('customer_id').agg({'sales_amount': 'sum', 'order_id': 'count'}).reset_index()
            
            report_df = pd.DataFrame(report_data)
            st.dataframe(report_df, use_container_width=True)
            
            csv = report_df.to_csv(index=False)
            st.download_button("📥 Download CSV", csv, f"{report_type.lower()}_report.csv", "text/csv")

else:
    st.markdown("<h1 class='gradient-text' style='text-align: center;'>Welcome to E-Commerce Analytics Pro</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; padding: 50px;'>
    <h3>🚀 Get Started</h3>
    <p>Choose a data source from the sidebar</p>
    <ul style='list-style-type: none;'>
    <li>📊 Dashboard with KPIs</li>
    <li>📦 Product analysis</li>
    <li>👥 Customer insights</li>
    <li>🌍 Geographic data</li>
    <li>🔮 Sales forecasting</li>
    <li>📄 Report generation</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>Made with ❤️ using Streamlit</p>", unsafe_allow_html=True)
