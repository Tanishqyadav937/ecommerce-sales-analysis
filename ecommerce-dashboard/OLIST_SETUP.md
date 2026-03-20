# Olist Dataset Setup Guide

## 📊 Using Your Olist Dataset

Your Olist customers dataset has been detected! Here's how to use it with the dashboard.

### ✅ What's Detected

- ✅ `olist_customers_dataset.csv` (8.6MB) - **LOADED**

### 📥 To Use Full Olist Dataset

Download the complete Olist dataset from Kaggle and place these files in the `ecommerce-dashboard` folder:

```
ecommerce-dashboard/
├── olist_customers_dataset.csv          ✅ (Already uploaded)
├── olist_orders_dataset.csv             (Download from Kaggle)
├── olist_order_items_dataset.csv        (Download from Kaggle)
├── olist_products_dataset.csv           (Download from Kaggle)
├── olist_order_payments_dataset.csv     (Download from Kaggle)
└── olist_order_reviews_dataset.csv      (Download from Kaggle)
```

### 🚀 Running the Updated Dashboard

#### Option 1: Use the New Olist-Optimized App (Recommended)

```bash
# Run the new app optimized for Olist data
streamlit run app_olist.py
```

#### Option 2: Use the Original App

```bash
# Run the original app
streamlit run app.py
```

### 🎯 Features with Olist Data

#### With Customers Dataset Only
- ✅ Customer location analysis
- ✅ Geographic insights
- ✅ Customer count metrics
- ⚠️ Limited sales/revenue data

#### With Full Olist Dataset
- ✅ Complete sales analysis
- ✅ Order history
- ✅ Product performance
- ✅ Payment methods
- ✅ Customer reviews & ratings
- ✅ Delivery time analysis
- ✅ Full forecasting

### 📋 Olist Dataset Columns

#### Customers Dataset (Currently Available)
```
customer_id              - Unique customer ID
customer_unique_id       - Unique customer identifier
customer_zip_code_prefix - Zip code
customer_city            - City name
customer_state           - State code
```

#### Orders Dataset (To Download)
```
order_id                 - Unique order ID
customer_id              - Customer reference
order_status             - Order status
order_purchase_timestamp - Purchase date/time
order_approved_at        - Approval date
order_delivered_carrier_date - Carrier delivery date
order_delivered_customer_date - Customer delivery date
order_estimated_delivery_date - Estimated delivery date
```

#### Order Items Dataset (To Download)
```
order_id                 - Order reference
order_item_id            - Item ID
product_id               - Product reference
seller_id                - Seller reference
shipping_limit_date      - Shipping deadline
price                    - Item price
freight_value            - Freight cost
```

#### Products Dataset (To Download)
```
product_id               - Unique product ID
product_category_name    - Product category
product_name_lenght      - Product name length
product_description_lenght - Description length
product_photos_qty       - Number of photos
product_weight_g         - Weight in grams
product_length_cm        - Length in cm
product_height_cm        - Height in cm
product_width_cm         - Width in cm
```

#### Payments Dataset (To Download)
```
order_id                 - Order reference
payment_sequential       - Payment sequence
payment_type             - Payment method
payment_installments     - Number of installments
payment_value            - Payment amount
```

#### Reviews Dataset (To Download)
```
review_id                - Unique review ID
order_id                 - Order reference
review_score             - Rating (1-5)
review_comment_title     - Review title
review_comment_message   - Review message
review_creation_date     - Review date
review_answer_timestamp  - Answer timestamp
```

### 🔄 How the App Handles Missing Files

The updated `app_olist.py` intelligently handles missing files:

1. **Customers Only** → Shows customer locations and basic metrics
2. **Customers + Orders** → Shows sales and order data
3. **All Files** → Full analytics with all features

### 📥 Download Olist Dataset

1. Go to [Kaggle Olist Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
2. Download all CSV files
3. Extract to `ecommerce-dashboard` folder
4. Run `streamlit run app_olist.py`

### 🎯 Quick Start with Current Data

```bash
# 1. Navigate to project
cd ecommerce-dashboard

# 2. Run the Olist-optimized app
streamlit run app_olist.py

# 3. Click "Load Olist Data" in sidebar
# 4. Explore customer data
```

### 📊 What You Can Do Now

With your current customers dataset:

✅ **Geographic Analysis**
- View customer distribution by state
- Analyze customers by city
- Regional customer counts

✅ **Customer Insights**
- Total customer count
- Customer location mapping
- State-wise distribution

✅ **Dashboard**
- Customer metrics
- Location-based analytics
- City rankings

### 🚀 Next Steps

1. **Download Full Dataset** from Kaggle
2. **Place Files** in ecommerce-dashboard folder
3. **Run App** with `streamlit run app_olist.py`
4. **Explore** all 6 dashboard sections

### 🆘 Troubleshooting

**Issue**: "Customers dataset not found"
- **Solution**: Ensure `olist_customers_dataset.csv` is in the ecommerce-dashboard folder

**Issue**: "Orders dataset not found"
- **Solution**: Download from Kaggle and place in the folder (optional - app works with customers only)

**Issue**: App runs but shows limited data
- **Solution**: Download the complete Olist dataset from Kaggle for full features

### 📞 Support

- Check `QUICKSTART.md` for general help
- See `CONFIG.md` for customization
- Review `README.md` for full documentation

---

**Version**: 2.0.0 with Olist Support  
**Status**: ✅ Ready to Use  
**Date**: March 20, 2024
