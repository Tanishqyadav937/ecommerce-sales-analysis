# E-Commerce Sales & Profit Analysis Dashboard

A professional, interactive analytics dashboard built with Streamlit for analyzing e-commerce sales data, identifying profit trends, and providing actionable business insights.

## Features

✨ **Modern UI with Animations**
- Gradient backgrounds and smooth transitions
- Animated metric cards with hover effects
- Professional color scheme (purple/blue gradients)
- Responsive design

📊 **Comprehensive Analytics**
- Real-time KPI metrics (Revenue, Profit, Orders, Customers)
- Revenue and profit trend analysis
- Top products by revenue and profit
- Sales distribution by category and region
- Customer lifetime value (LTV) calculations
- Repeat customer rate analysis

🎯 **Interactive Filters**
- Date range selection
- Category filtering
- Region filtering
- Multi-select options with clear all functionality

📈 **Visualizations**
- Line charts for trends
- Bar charts for product performance
- Pie charts for distribution analysis
- Interactive Plotly charts with hover details

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

1. Navigate to the project directory:
```bash
cd ecommerce-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

### Using Sample Data

By default, the dashboard generates realistic synthetic e-commerce data with:
- 1000+ transactions
- 8 different products
- 2 categories (Electronics, Accessories)
- 4 regions (North, South, East, West)
- Date range: Jan 2023 - Mar 2024

### Upload Your Own Data

1. Click "Upload CSV" in the sidebar
2. Select your CSV file with columns:
   - `Date` (YYYY-MM-DD format)
   - `Product` (product name)
   - `Category` (product category)
   - `Quantity` (order quantity)
   - `Unit_Price` (price per unit)
   - `Revenue` (total revenue)
   - `Cost` (cost of goods)
   - `Profit` (revenue - cost)
   - `Customer_ID` (unique customer identifier)
   - `Region` (geographic region)

## Dashboard Sections

### 1. KPI Cards
Quick overview of key metrics:
- Total Revenue
- Total Profit
- Total Orders
- Unique Customers

### 2. Trends
- Daily revenue trend line chart
- Daily profit trend line chart

### 3. Product Performance
- Top 8 products by revenue
- Top 8 products by profit

### 4. Distribution Analysis
- Revenue by category (pie chart)
- Revenue by region (pie chart)

### 5. Advanced Metrics
- Average Order Value (AOV)
- Profit Margin %
- Repeat Customer Rate
- Average Customer Lifetime Value (LTV)

### 6. Transaction Details
- Recent 20 transactions table
- Sortable and filterable data

## Customization

### Modify Colors
Edit the CSS in `app.py` to change the gradient colors:
```python
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Adjust Sample Data
Modify the `generate_sample_data()` function to:
- Change number of records
- Add/remove products
- Adjust price ranges
- Modify date ranges

### Add More Metrics
Extend the `calculate_metrics()` function to compute additional KPIs

## Performance Tips

- For large datasets (>100k rows), consider:
  - Filtering data before visualization
  - Using date range filters
  - Aggregating data by day/week instead of individual transactions

- Use `@st.cache_data` decorator for expensive computations

## Dependencies

- **streamlit**: Web app framework
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **plotly**: Interactive visualizations
- **scikit-learn**: ML capabilities (optional)

## File Structure

```
ecommerce-dashboard/
├── app.py              # Main dashboard application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Troubleshooting

**Issue**: Dashboard won't start
- Solution: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Charts not displaying
- Solution: Check that your data has the required columns

**Issue**: Slow performance
- Solution: Use date range filters to reduce data size

## Future Enhancements

- [ ] Forecasting with ARIMA/Prophet
- [ ] Customer segmentation analysis
- [ ] Inventory management tracking
- [ ] Dark mode toggle
- [ ] Export reports to PDF
- [ ] Real-time data integration
- [ ] Multi-page navigation
- [ ] Advanced filtering with SQL queries

## License

MIT License - Feel free to use and modify for your projects

## Support

For issues or questions, please refer to:
- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
