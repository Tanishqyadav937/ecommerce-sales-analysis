# Configuration Guide

This guide explains how to customize the E-Commerce Analytics Pro dashboard.

## 🎨 Customizing Colors

Edit the CSS section in `app.py` to change the color scheme:

```python
# Current gradient colors
background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
```

### Popular Color Schemes

**Blue & Purple (Current)**
```css
background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
```

**Green & Teal**
```css
background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
```

**Orange & Red**
```css
background: linear-gradient(90deg, #ff6b6b 0%, #ee5a6f 100%);
```

**Pink & Purple**
```css
background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
```

## 📊 Modifying Sample Data

Edit the `load_sample_data()` function to customize:

### Change Number of Records
```python
for order_id in range(1, 5001):  # Change 5001 to desired number
```

### Add/Remove Products
```python
categories = {
    'Electronics': ['Smartphones', 'Laptops', 'Tablets'],
    'Fashion': ['Men\'s Clothing', 'Women\'s Clothing'],
    # Add more categories here
}
```

### Adjust Price Ranges
```python
base_price = np.random.uniform(20, 1000) * multiplier  # Change 20-1000 range
```

### Modify Date Range
```python
start_date = pd.Timestamp('2023-01-01')
end_date = pd.Timestamp('2023-12-31')
```

### Change Seasonality
```python
if date.month in [11, 12]:
    multiplier = 2.5  # Increase for higher seasonality
elif date.month in [6, 7]:
    multiplier = 1.5
```

## 🔧 Adding Custom Metrics

### Add a New KPI Card

In the Dashboard section, add:

```python
with col5:
    custom_metric = df['your_column'].sum()
    st.markdown(f"""
    <div class='metric-card fade-in'>
    <h3 style='color: #666; font-size: 14px;'>YOUR METRIC</h3>
    <h2 style='color: #2c3e50; font-size: 28px;'>{custom_metric:,.0f}</h2>
    <p style='color: #3498db;'>Your description</p>
    </div>
    """, unsafe_allow_html=True)
```

### Add a New Chart

```python
with col1:
    colored_header(label="📊 Your Chart Title", description="Description", color_name="blue-70")
    
    # Your data processing
    chart_data = df.groupby('column').agg({'metric': 'sum'})
    
    # Create chart
    fig = px.bar(chart_data, title="Your Chart Title")
    st.plotly_chart(fig, use_container_width=True)
```

## 📈 Configuring Forecasting

### Change Forecast Period
```python
future_days = 30  # Change to desired number of days
```

### Use Different Forecasting Model

Replace LinearRegression with:

```python
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)
```

Or use Prophet for better time series:

```python
from prophet import Prophet

# Prepare data for Prophet
prophet_df = daily_sales.rename(columns={'date': 'ds', 'sales': 'y'})
model = Prophet()
model.fit(prophet_df)
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)
```

## 🎯 Customizing Filters

### Add New Filter in Sidebar

```python
with st.sidebar:
    # Add after existing filters
    selected_payment = st.multiselect(
        "Payment Method",
        options=df['payment_method'].unique(),
        default=df['payment_method'].unique()
    )
    
    # Apply filter
    df = df[df['payment_method'].isin(selected_payment)]
```

### Add Filter to Products Analysis

```python
with col4:
    min_rating = st.slider("Minimum Rating", min_value=1, max_value=5, value=3)

filtered_products = filtered_products[filtered_products['customer_rating'] >= min_rating]
```

## 🌐 Integrating Real Data

### Connect to Database

```python
import sqlite3

@st.cache_data
def load_from_database():
    conn = sqlite3.connect('your_database.db')
    df = pd.read_sql_query("SELECT * FROM orders", conn)
    conn.close()
    return df
```

### Connect to API

```python
import requests

@st.cache_data
def load_from_api():
    response = requests.get('https://api.example.com/orders')
    data = response.json()
    df = pd.DataFrame(data)
    return df
```

### Connect to Google Sheets

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

@st.cache_data
def load_from_sheets():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Your Sheet Name').sheet1
    df = pd.DataFrame(sheet.get_all_records())
    return df
```

## 🔐 Adding Authentication

```python
import streamlit_authenticator as stauth

names = ["John Smith", "Jane Doe"]
usernames = ["jsmith", "jdoe"]
passwords = ["password1", "password2"]

authenticator = stauth.Authenticate(names, usernames, passwords, "dashboard", "abcdef", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    # Show dashboard
    pass
elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
```

## 📱 Responsive Design

The dashboard is already responsive, but you can customize breakpoints:

```python
# For mobile optimization
if st.session_state.get('is_mobile', False):
    col1, col2 = st.columns(1)  # Single column on mobile
else:
    col1, col2 = st.columns(2)  # Two columns on desktop
```

## 🚀 Performance Optimization

### Enable Caching for Custom Functions

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def expensive_calculation(df):
    # Your calculation here
    return result
```

### Lazy Load Charts

```python
if st.checkbox("Show Advanced Charts"):
    # Charts only load when checkbox is checked
    fig = px.scatter(df, x='x', y='y')
    st.plotly_chart(fig)
```

### Reduce Data Size

```python
# Sample data for faster processing
df_sample = df.sample(n=min(10000, len(df)))
```

## 📝 Adding Custom Sections

### Create New Tab

```python
tab1, tab2, tab3 = st.tabs(["Overview", "Details", "Export"])

with tab1:
    st.write("Overview content")

with tab2:
    st.write("Details content")

with tab3:
    st.write("Export content")
```

### Add Expandable Sections

```python
with st.expander("Advanced Options"):
    option1 = st.slider("Option 1", 0, 100)
    option2 = st.selectbox("Option 2", ["A", "B", "C"])
```

## 🔄 Updating Dependencies

To update all packages to latest versions:

```bash
pip install -r requirements.txt --upgrade
```

To check for outdated packages:

```bash
pip list --outdated
```

---

For more help, see README.md or QUICKSTART.md
