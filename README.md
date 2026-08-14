# Capstone Project

## Overview

This repository contains the complete Capstone Project, which is divided into three modules:

- Analytics
- Data Pipeline
- Support Assistant (Retrieval-Augmented Generation)

The project demonstrates the complete data science workflow, including data collection, preprocessing, exploratory data analysis, machine learning, database management, information retrieval, and API development.

---

# Repository Structure

```
CAPSTONE PROJECT/
│
├── analytics/
│   ├── 01_eda.ipynb
│   ├── titanic.csv
│   └── titanic_random_forest_pipeline.pkl
│
├── Data Pipeline/
│   ├── scraper.py
│   ├── books.db
│   ├── books.json
│   └── sql_query_results.json
│
├── support_assistant/
│   ├── app/
│   ├── chroma_db/
│   ├── docs/
│   ├── requirements.txt
│   └── ...
│
└── README.md
```

---

# Module 1: Analytics

## Objective

Perform exploratory data analysis and build machine learning models using the Titanic dataset.

## Features

- Missing value analysis
- Outlier detection using IQR
- Skewness analysis
- Correlation matrix and heatmap
- Univariate, bivariate, and multivariate analysis
- Feature engineering
- Stratified train-test split
- Data preprocessing pipeline
- Standardization
- Model comparison
- Hyperparameter tuning using GridSearchCV
- SMOTE for class imbalance
- Regression analysis
- Pipeline serialization using Joblib

## Machine Learning Models

- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier

## Evaluation Metrics

### Classification

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix

### Regression

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Mean Absolute Percentage Error (MAPE)
- R² Score

---

# Module 2: Data Pipeline

## Objective

Build an automated data pipeline that scrapes book data, cleans it, stores it in a SQLite database, and performs SQL analysis.

## Features

- Web scraping
- Data cleaning
- Currency conversion
- SQLite database creation
- SQL queries
- JOIN operations
- Data analysis using Pandas

## Dataset Fields

- Book Title
- Category
- Price (GBP)
- Price (INR)
- Rating
- Stock Availability

### Currency Conversion

A fixed exchange rate was used throughout the project:

```
1 GBP = 105.50 INR
```

---

# Module 3: Support Assistant

## Objective

Develop a Retrieval-Augmented Generation (RAG) support assistant capable of answering policy-related questions using embedded documentation.

## Technologies

- LangGraph
- ChromaDB
- FastAPI
- Pydantic

## RAG Pipeline

```
User Query
     │
     ▼
Intent Classification
     │
     ├── General Question
     │         │
     │         ▼
     │   Direct Response
     │
     └── Policy Question
               │
               ▼
       ChromaDB Retrieval
               │
               ▼
      Context Generation
               │
               ▼
      Structured JSON Response
```

---

# Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- SQLite
- BeautifulSoup
- Requests
- Joblib
- FastAPI
- LangGraph
- ChromaDB
- Pydantic

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Puffydoik/Capstone-project.git
```

Move into the project directory:

```bash
cd Capstone-project
```

Install the required dependencies:

```bash
pip install -r support_assistant/requirements.txt
```

---

# Running the Project

## Analytics

Open the notebook:

```
analytics/01_eda.ipynb
```

Run all cells sequentially.

---

## Data Pipeline

Execute:

```bash
python "Data Pipeline/scraper.py"
```

This script will:

- Scrape book data
- Generate `books.json`
- Populate `books.db`
- Execute SQL queries

---

## Support Assistant

Navigate to the `support_assistant` directory and start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The application will be available locally.

---

# Project Deliverables

The project includes:

- Complete exploratory data analysis
- Machine learning pipeline
- Saved trained model
- Automated web scraping pipeline
- SQLite database
- SQL query implementation
- Retrieval-Augmented Generation support assistant
- LangGraph workflow
- ChromaDB vector database
- FastAPI application

---

# Future Enhancements

- Deploy the FastAPI application
- Integrate a production LLM
- Improve retrieval accuracy
- Expand the document knowledge base
- Develop a web interface

---

# Author

**Vighnesh K**

Computer Science and Business Systems (CSBS)

Capstone Project
