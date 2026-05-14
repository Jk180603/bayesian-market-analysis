# Bayesian Marketing Analytics & Campaign Optimization

A production-ready Bayesian analytics system for marketing campaign performance analysis using PyMC, PostgreSQL, and Streamlit.

The project processes marketing campaign data, performs SQL-based analytics, estimates campaign effectiveness using Bayesian inference, and visualizes uncertainty-aware business insights through an interactive dashboard.

---

# Features

- Marketing campaign ETL pipeline
- PostgreSQL data warehouse integration
- SQL analytics layer
- Bayesian statistical modeling with PyMC
- Probabilistic campaign effectiveness estimation
- Uncertainty interval analysis
- Interactive Streamlit dashboard
- Reproducible modular project structure

---

# Tech Stack

- Python
- PyMC
- PostgreSQL
- SQLAlchemy
- Pandas
- NumPy
- ArviZ
- Streamlit
- Matplotlib

---

# Project Architecture

```text
CSV Data
   ↓
ETL Pipeline
   ↓
PostgreSQL Database
   ↓
SQL Analytics Layer
   ↓
Bayesian Modeling (PyMC)
   ↓
Reports & Insights
   ↓
Streamlit Dashboard
```

---

# Bayesian Modeling

The project uses Bayesian inference to estimate marketing channel effectiveness while quantifying uncertainty through posterior probability distributions and HDI intervals.

Unlike traditional deterministic ML models, this approach provides probabilistic estimates for campaign performance and supports uncertainty-aware decision making.

---

# Dashboard Features

- Channel effectiveness comparison
- Bayesian uncertainty intervals
- Campaign performance analytics
- SQL-driven business insights

---

# Setup

## Clone repository

```bash
git clone https://github.com/Jk180603/bayesian-marketing-analytics.git
cd bayesian-marketing-analytics
```

## Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run ETL Pipeline

```bash
python src/generate_data.py
python src/load_to_postgres.py
```

---

# Run Bayesian Model

```bash
python src/bayesian_model.py
```

---

# Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

# Example Insights

- Marketing channels compared using posterior effectiveness distributions
- Uncertainty-aware ROI estimation
- Probabilistic campaign performance evaluation

---

# Future Improvements

- Docker deployment
- Automated retraining workflows
- API integration
- Real-time campaign monitoring
- Cloud deployment
- Multi-touch attribution modeling