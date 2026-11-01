# Customer Churn Prediction

An analysis of telecom customer data to find why customers leave and which groups are most at risk, so a business can act early to retain them.

## Problem Statement
Customer churn costs telecom companies revenue, and keeping an existing customer is usually cheaper than winning a new one. This project explores customer demographics, services, contracts and billing to find what drives churn and how much revenue is at risk.

## Dataset
- Telco Customer Churn dataset (customer demographics, services subscribed, contract, billing and satisfaction information)
- Size: 7,043 customers x 50 columns
- Target: `Churn` (Yes / No), created from the churn category column (1,869 churned, 5,174 retained)

## Tech Stack
Python, Pandas, NumPy, Matplotlib, Seaborn, SciPy, Streamlit

## Approach
1. **Data cleaning:** checked for missing values; filled `InternetType`, `ChurnCategory` and `ChurnReason` where blank; dropped the `Offer` column (about 55% missing)
2. **Feature creation:** built a binary `Churn` target and tenure groups (0-12, 13-24, 25-48, 49-60, 60+ months)
3. **Exploratory analysis:** churn rate, churn by tenure group, churn by contract type, monthly charges vs churn, churn heatmap (tenure x contract)
4. **Statistical analysis:** correlation of tenure and monthly charge with churn, and a chi-square test between contract type and churn
5. **Revenue at risk:** estimated monthly and annual revenue linked to churned customers

## Key Insights
- **Overall churn rate is 26.5%** (1,869 of 7,043 customers).
- **Tenure is the strongest signal.** Churn falls from 47.4% in the first year to 28.7% (13-24 months), 20.4% (25-48), 14.4% (49-60) and 6.6% after 60 months. Tenure has a correlation of -0.35 with churn.
- **Higher bills go with higher churn.** Churned customers pay about $74.44 a month on average, against $61.27 for retained customers (correlation of 0.19).
- **Contract type matters.** The chi-square test shows contract type is significantly associated with churn (p-value effectively 0).

## Project Structure
```
├── app.py                  # App for predictions
├── churn_analysis.ipynb    # Cleaning, EDA and statistical analysis
├── TelcoCustomerChurn.csv  # Dataset
├── requirements.txt
└── README.md
```

## How to Run
```
git clone https://github.com/Sanjana28-Shetty/Customer-Churn-Prediction.git
cd Customer-Churn-Prediction
pip install -r requirements.txt
jupyter notebook churn_analysis.ipynb
```

## Author
Sanjana S Shetty
[LinkedIn](https://www.linkedin.com/in/sanjana-s-shetty-803153299) | [GitHub](https://github.com/Sanjana28-Shetty)
