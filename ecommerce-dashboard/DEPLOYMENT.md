# Deployment Guide

This guide covers deploying E-Commerce Analytics Pro to various platforms.

## 🚀 Streamlit Cloud (Recommended)

### Step 1: Prepare Your Repository
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository
4. Choose the branch and file (`app.py`)
5. Click "Deploy"

### Step 3: Configure Secrets (if needed)
Create `.streamlit/secrets.toml`:
```toml
[database]
host = "your_host"
user = "your_user"
password = "your_password"
```

## 🐳 Docker Deployment

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Create .dockerignore
```
venv/
__pycache__/
*.pyc
.git
.gitignore
.env
.DS_Store
```

### Step 3: Build and Run
```bash
# Build image
docker build -t ecommerce-dashboard .

# Run container
docker run -p 8501:8501 ecommerce-dashboard

# Or with volume mount for data
docker run -p 8501:8501 -v $(pwd)/data:/app/data ecommerce-dashboard
```

### Step 4: Deploy to Docker Hub
```bash
# Tag image
docker tag ecommerce-dashboard:latest your_username/ecommerce-dashboard:latest

# Push to Docker Hub
docker push your_username/ecommerce-dashboard:latest
```

## ☁️ Heroku Deployment

### Step 1: Create Procfile
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Step 2: Create runtime.txt
```
python-3.11.0
```

### Step 3: Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

## 🌐 AWS Deployment

### Option 1: AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 ecommerce-dashboard

# Create environment
eb create ecommerce-dashboard-env

# Deploy
eb deploy

# Open in browser
eb open
```

### Option 2: AWS EC2

```bash
# SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Python and dependencies
sudo yum update -y
sudo yum install python3 python3-pip -y

# Clone repository
git clone your-repo-url
cd ecommerce-dashboard

# Install requirements
pip install -r requirements.txt

# Run with Gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:8501 app:app
```

## 🔵 Azure Deployment

### Step 1: Create App Service
```bash
# Login to Azure
az login

# Create resource group
az group create --name myResourceGroup --location eastus

# Create App Service plan
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux

# Create web app
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name ecommerce-dashboard --runtime "PYTHON|3.11"
```

### Step 2: Deploy Code
```bash
# Configure deployment
az webapp deployment source config-zip --resource-group myResourceGroup --name ecommerce-dashboard --src app.zip
```

## 🟢 Google Cloud Run

### Step 1: Create app.yaml
```yaml
runtime: python311

env: standard
entrypoint: streamlit run app.py --server.port 8080 --server.address 0.0.0.0
```

### Step 2: Deploy
```bash
# Login to Google Cloud
gcloud auth login

# Deploy
gcloud run deploy ecommerce-dashboard --source . --platform managed --region us-central1 --allow-unauthenticated
```

## 📦 PythonAnywhere Deployment

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files
3. Create a new web app
4. Configure WSGI file to run Streamlit
5. Reload web app

## 🔒 Security Best Practices

### Environment Variables
```bash
# Create .env file (don't commit!)
DATABASE_URL=your_database_url
API_KEY=your_api_key
SECRET_KEY=your_secret_key
```

### Load in app.py
```python
import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv('DATABASE_URL')
```

### Streamlit Secrets
```python
import streamlit as st

db_url = st.secrets["database"]["url"]
```

## 📊 Performance Optimization for Production

### 1. Enable Caching
```python
@st.cache_data(ttl=3600)
def load_data():
    return pd.read_csv('data.csv')
```

### 2. Use CDN for Static Files
```python
st.image("https://cdn.example.com/image.png")
```

### 3. Optimize Data Loading
```python
# Load only necessary columns
df = pd.read_csv('data.csv', usecols=['col1', 'col2', 'col3'])

# Use chunking for large files
chunks = pd.read_csv('large_file.csv', chunksize=10000)
```

### 4. Database Connection Pooling
```python
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:password@localhost/db', pool_size=10, max_overflow=20)
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest
      - name: Deploy to Streamlit Cloud
        run: |
          streamlit run app.py
```

## 📈 Monitoring and Logging

### Application Monitoring
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Dashboard loaded successfully")
logger.error("Error loading data", exc_info=True)
```

### Error Tracking with Sentry
```python
import sentry_sdk

sentry_sdk.init("your-sentry-dsn")

try:
    # Your code
    pass
except Exception as e:
    sentry_sdk.capture_exception(e)
```

## 🧪 Testing Before Deployment

```bash
# Run tests
pytest tests/

# Check code quality
pylint app.py

# Format code
black app.py

# Type checking
mypy app.py
```

## 📝 Deployment Checklist

- [ ] All dependencies in requirements.txt
- [ ] Environment variables configured
- [ ] Database connections tested
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Security best practices applied
- [ ] Performance optimized
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Backup strategy in place

## 🆘 Troubleshooting Deployment

### App won't start
```bash
# Check logs
streamlit run app.py --logger.level=debug

# Verify dependencies
pip install -r requirements.txt --upgrade
```

### Slow performance
- Enable caching
- Optimize database queries
- Use CDN for static files
- Implement pagination

### Memory issues
- Reduce data size with filters
- Use chunking for large files
- Implement garbage collection

## 📞 Support Resources

- [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-cloud/deploy-your-app)
- [Docker Documentation](https://docs.docker.com/)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [AWS Documentation](https://docs.aws.amazon.com/)

---

**Happy deploying! 🚀**
