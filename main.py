import pandas as pd

class ThreeStatementModel:
    def __init__(self, assumptions, years=5):
        self.assumptions = assumptions
        self.years = years
        self.data = {
            "Income Statement": [],
            "Cash Flow Statement": [],
            "Balance Sheet": []
        }
        self.debt = assumptions["initial_debt"]
        self.equity = assumptions["initial_equity"]
        self.fixed_assets = assumptions["initial_assets"] - assumptions["initial_cash"]
        self.cash = assumptions["initial_cash"]
        self.revolver = 0
        self.min_cash_balance = assumptions.get("min_cash_balance", 0)
        self.revolver_limit = assumptions.get("revolver_limit", 5000)

    def income_statement(self, revenue):
        a = self.assumptions
        cogs = revenue * a["cogs_percent"]
        opex = revenue * a["opex_percent"]
        depreciation = a["depreciation"]
        gross_profit = revenue - cogs
        ebit = gross_profit - opex - depreciation
        term_interest = a["interest_rate"] * self.debt
        revolver_interest = a["revolver_interest_rate"] * self.revolver
        interest = term_interest + revolver_interest
        ebt = ebit - interest
        taxes = ebt * a["tax_rate"]
        net_income = ebt - taxes
        return {
            "Revenue": revenue,
            "COGS": cogs,
            "OPEX": opex,
            "Depreciation": depreciation,
            "EBIT": ebit,
            "Interest": interest,
            "Term Interest": term_interest,
            "Revolver Interest": revolver_interest,
            "EBT": ebt,
            "Taxes": taxes,
            "Net Income": net_income
        }

    def cash_flow_statement(self, income):
        a = self.assumptions
        depreciation = income["Depreciation"]
        net_income = income["Net Income"]
        cfo = net_income + depreciation - a["change_in_working_cap"]
        cfi = -a["capex"]
        interest = income["Interest"]
        debt_repayment = a.get("debt_repayment", 0)
        cff = -interest - debt_repayment
        net_cash_flow = cfo + cfi + cff
        return {
            "CFO": cfo,
            "CFI": cfi,
            "CFF": cff,
            "Net Cash Flow": net_cash_flow
        }

    def balance_sheet(self, cash_flow, net_income, cogs):
        a = self.assumptions
        self.fixed_assets += a["capex"] - a["depreciation"]
        projected_cash = self.cash + cash_flow["Net Cash Flow"]

        if projected_cash < self.min_cash_balance:
            draw_needed = self.min_cash_balance - projected_cash
            draw = min(draw_needed, self.revolver_limit - self.revolver)
            self.revolver += draw
            self.cash = projected_cash + draw
        else:
            excess_cash = projected_cash - self.min_cash_balance
            repay = min(excess_cash, self.revolver)
            self.revolver -= repay
            self.cash = projected_cash - repay

        self.debt -= a.get("debt_repayment", 0)
        self.equity += net_income

        # New: Accounts Payable
        ap = cogs * a.get("ap_percent", 0)
        current_liabilities = self.revolver + ap
        non_current_liabilities = self.debt
        total_liabilities = current_liabilities + non_current_liabilities
        total_assets = self.cash + self.fixed_assets
        liabilities_and_equity = total_liabilities + self.equity

        return {
            "Cash": self.cash,
            "Fixed Assets": self.fixed_assets,
            "Assets": total_assets,
            "Revolver (Current Liab.)": self.revolver,
            "Accounts Payable": ap,
            "Debt (Non-Current)": self.debt,
            "Total Liabilities": total_liabilities,
            "Equity": self.equity,
            "Liabilities + Equity": liabilities_and_equity
        }

    def run(self):
        a = self.assumptions
        revenue = a["initial_revenue"]
        for year in range(1, self.years + 1):
            revenue *= (1 + a["revenue_growth"])
            income = self.income_statement(revenue)
            cash_flow = self.cash_flow_statement(income)
            balance = self.balance_sheet(cash_flow, income["Net Income"], income["COGS"])
            self.data["Income Statement"].append(income)
            self.data["Cash Flow Statement"].append(cash_flow)
            self.data["Balance Sheet"].append(balance)
        return self.data

# Updated assumptions including AP
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

# Run model
model = ThreeStatementModel(assumptions)
results = model.run()

# Convert results to DataFrames
years = [f"Year {i+1}" for i in range(model.years)]
income_df = pd.DataFrame(results["Income Statement"], index=years)
cashflow_df = pd.DataFrame(results["Cash Flow Statement"], index=years)
balance_df = pd.DataFrame(results["Balance Sheet"], index=years)

print("Income Statement:\n", income_df)
print("\nCash Flow Statement:\n", cashflow_df)
print("\nBalance Sheet:\n", balance_df)

# Calculate key financial ratios categorized by nature, indexed by year

# Profitability Ratios
profitability = pd.DataFrame(index=income_df.index)
profitability["Gross Margin"] = (income_df["Revenue"] - income_df["COGS"]) / income_df["Revenue"]
profitability["EBIT Margin"] = income_df["EBIT"] / income_df["Revenue"]
profitability["Net Profit Margin"] = income_df["Net Income"] / income_df["Revenue"]
profitability["Return on Assets (ROA)"] = income_df["Net Income"] / balance_df["Assets"]
profitability["Return on Equity (ROE)"] = income_df["Net Income"] / balance_df["Equity"]

# Liquidity Ratios
liquidity = pd.DataFrame(index=income_df.index)
liquidity["Quick Ratio (Cash/CL)"] = balance_df["Cash"] / (
    balance_df["Revolver (Current Liab.)"] + balance_df["Accounts Payable"]
)

# Leverage Ratios
leverage = pd.DataFrame(index=income_df.index)
leverage["Debt to Equity"] = balance_df["Total Liabilities"] / balance_df["Equity"]
leverage["Debt to Assets"] = balance_df["Total Liabilities"] / balance_df["Assets"]
leverage["Interest Coverage (EBIT/Interest)"] = income_df["EBIT"] / income_df["Interest"]

# Cash Flow Ratios
cashflow_ratios = pd.DataFrame(index=income_df.index)
cashflow_ratios["CFO to Total Debt"] = cashflow_df["CFO"] / (
    balance_df["Revolver (Current Liab.)"] + balance_df["Debt (Non-Current)"]
)
cashflow_ratios["CFO to CapEx"] = cashflow_df["CFO"] / -cashflow_df["CFI"]

# Display all grouped ratios
print("\n=== Profitability Ratios ===\n", profitability)
print("\n=== Liquidity Ratios ===\n", liquidity)
print("\n=== Leverage Ratios ===\n", leverage)
print("\n=== Cash Flow Ratios ===\n", cashflow_ratios)


