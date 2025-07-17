# Three-Statement-Financial-Model-in-Python
This project implements a basic three-statement financial model in Python that dynamically builds and links the Income Statement, Cash Flow Statement, and Balance Sheet over a multi-year forecast. It also computes key financial ratios by year.
#  Three-Statement Financial Model in Python

This repository contains a basic **three-statement financial model** built in Python. It links together the **Income Statement**, **Cash Flow Statement**, and **Balance Sheet**, and calculates key **financial ratios** by year.

##  Features

- Dynamic multi-year forecasting
- Linked financial statements:
  - Income Statement
  - Cash Flow Statement
  - Balance Sheet
- Supports:
  - Term debt with interest and repayment
  - Revolver facility with interest and minimum cash threshold
  - Accounts payable as a percentage of COGS (current liability)
- Automatic calculation of key financial ratios:
  - Profitability
  - Liquidity
  - Leverage
  - Cash Flow

##  Example Assumptions

```python
assumptions = {
    "revenue_growth": 0.10,
    "cogs_percent": 0.6,
    "opex_percent": 0.20,
    "depreciation": 500,
    "interest_rate": 0.07,
    "revolver_interest_rate": 0.04,
    "tax_rate": 0.25,
    "capex": 1000,
    "change_in_working_cap": 200,
    "debt_repayment": 500,
    "initial_revenue": 10000,
    "initial_debt": 5000,
    "initial_cash": 1000,
    "initial_equity": 5000,
    "initial_assets": 11000,
    "min_cash_balance": 20,
    "revolver_limit": 8000,
    "ap_percent": 0.2
}
```
#  Installation

```python
git clone https://github.com/XChrisAlex/Three-Statement-Financial-Model-in-Python/tree/main
cd Three-Statement-Financial-Model-in-Python
pip install -r requirements.txt

```
# Feedback

Your feedback is appreciated!
If you have suggestions, bug reports, or want to contribute improvements:
*Star this repository

*Submit a pull request

*Open an issue
