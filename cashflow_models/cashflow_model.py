import numpy as np
import pandas as pd

# Added a new comment here - 02

def calculate_cashflow(initial_investment, cashflows, discount_rate):
    net_present_value = -initial_investment
    for t, cashflow in enumerate(cashflows, start=1):
        discounted_cashflow = cashflow / ((1 + discount_rate) ** t)
        net_present_value += discounted_cashflow
    return net_present_value

# Example usage
initial_investment = 1000
cashflows = [200, 300, 400, 500]
discount_rate = 0.05

npv = calculate_cashflow(initial_investment, cashflows, discount_rate)
print(f"Net Present Value: {npv}")
