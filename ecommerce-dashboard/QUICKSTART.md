# E-Commerce Analytics Pro - Quick Start Guide

Welcome to E-Commerce Analytics Pro! This guide will get you up and running in minutes.

## 🚀 Installation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Dashboard
```bash
streamlit run app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## 📊 Getting Started

### First Time Setup

1. **Choose Your Data Source** (in the sidebar):
   - **Sample Data** (Recommended for first-time users)
     - Pre-loaded with 5,000 realistic e-commerce transactions
     - Includes multiple product categories and customer segments
     - Perfect for exploring all features
   
   - **Upload Your Own**
     - Import your CSV file with e-commerce data
     - Required columns: order_id, order_date, customer_id, sales_amount, profit, etc.
   
   - **Kaggle (Olist)**
     - For advanced users with Olist dataset
     - Download from Kaggle and place files in the project directory

2. **Set Date Range** (optional)
   - Use the date filter in the sidebar to focus on specific periods
   - Default shows all available data

## 🎯 Dashboard Features

### 1. **Executive Dashboard** (Default View)
   - **KPI Cards**: Quick overview of key metrics
     - Total Revenue
     - Total Profit & Profit Margin
     - Total Orders & Average Order Value
     - Customer Count & Repeat Rate
   
   - **Revenue Trend**: Monthly revenue and profit visualization
   - **Category Distribution**: Revenue breakdown by product category
   - **Top Products**: Best performers by profit
   - **Improvement Areas**: Products with negative profit

### 2. **Products Analysis**
   - Filter by category and profit margin
   - Sort products by Profit, Revenue, Quantity, or Margin
   - Interactive product performance matrix
   - Scatter plot showing relationship between units sold and profit

### 3. **Customer Insights**
   - Customer segment distribution (Premium, Regular, Occasional, New)
   - Revenue and profit by segment
   - Customer Lifetime Value (CLV) analysis
   - Repeat customer rate and VIP customer count

### 4. **Geographic Analysis**
   - Regional performance comparison
   - Top 10 cities by revenue
   - Regional revenue and profit breakdown

### 5. **Forecasting**
   - 30-day sales forecast using linear regression
   - Historical vs. predicted trends
   - Expected growth rate calculation
   - Forecasted revenue metrics

### 6. **Reports**
   - **Executive Summary**: Key metrics snapshot
   - **Product Performance**: Category-level analysis
   - **Customer Analysis**: Segment breakdown
   - **Financial Report**: Monthly revenue and profit
   - Download reports as CSV

## 💡 Tips & Tricks

### Optimizing Performance
- Use date filters for large datasets (>100k rows)
- Filter by specific categories to reduce data size
- The dashboard caches data automatically for faster loading

### Understanding the Data
- **Profit Margin**: (Profit / Revenue) × 100
- **Average Order Value**: Total Revenue / Total Orders
- **Repeat Rate**: Percentage of customers with multiple orders
- **Customer Segments**: Based on purchase frequency and order value

### Customizing the Dashboard
- Edit colors in the CSS section of `app.py`
- Modify the sample data generation in `load_sample_data()`
- Add new metrics in the KPI section
- Create custom filters in the sidebar

## 📁 File Structure

```
ecommerce-dashboard/
├── app.py                 # Main dashboard application
├── requirements.txt       # Python dependencies
├── README.md             # Full documentation
├── QUICKSTART.md         # This file
└── sample_data.csv       # Sample dataset (optional)
```

## 🔧 Troubleshooting

### Dashboard won't start
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt --upgrade

# Try running with verbose output
streamlit run app.py --logger.level=debug
```

### Charts not displaying
- Check that your data has the required columns
- Ensure date columns are in YYYY-MM-DD format
- Verify numeric columns contain valid numbers

### Slow performance
- Use date range filters to reduce data size
- Filter by specific categories
- Reduce the number of rows displayed in tables

### Data not loading
- For CSV uploads, ensure the file has required columns
- Check file encoding (UTF-8 recommended)
- Verify column names match expected format

## 📚 Sample Data Schema

If uploading your own data, ensure these columns:

| Column | Type | Description |
|--------|------|-------------|
| order_id | string | Unique order identifier |
| order_date | date | Order date (YYYY-MM-DD) |
| customer_id | string | Unique customer identifier |
| customer_segment | string | Customer type (Premium/Regular/Occasional/New) |
| region | string | Geographic region |
| city | string | City name |
| product_category | string | Product category |
| product_name | string | Product name |
| quantity | int | Units ordered |
| unit_price | float | Price per unit |
| sales_amount | float | Total revenue |
| profit | float | Total profit |
| profit_margin | float | Profit margin % |
| customer_rating | int | Customer rating (1-5) |

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Charts](https://plotly.com/python/)
- [Pandas Guide](https://pandas.pydata.org/docs/)
- [E-Commerce Analytics Best Practices](https://www.shopify.com/blog/ecommerce-analytics)

## 🚀 Next Steps

1. **Explore Sample Data**: Start with the default sample data to understand all features
2. **Upload Your Data**: Import your own e-commerce data for real insights
3. **Customize**: Modify colors, metrics, and filters to match your needs
4. **Share**: Export reports and share insights with your team

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the full README.md for detailed documentation
3. Check Streamlit and Plotly documentation for framework-specific issues

---

**Happy analyzing! 📊**
