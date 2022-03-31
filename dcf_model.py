import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st
%matplotlib inline

years = ['2020A', '2021B', '2022P', '2023P', '2024P', '2025P']
sales = pd.Series(index=years)
sales['2020A'] = 31.0

growth_rate = 0.1

for year in range(1, 6):
    sales[year] = sales[year-1]*(1+growth_rate)

ebitda_margin = 0.14
depr_percent = 0.032
ebitda = sales*ebitda_margin
depreciation = sales*depr_percent
ebit = ebitda-depreciation
nwc_percent = 0.24
nwc = sales*nwc_percent
change_in_nwc = nwc.shift(1)-nwc
capex_percent = depr_percent
capex = -(sales*capex_percent)
tax_rate = 0.25
tax_payment = -ebit*tax_rate
tax_payment = tax_payment.apply(lambda x: min(x, 0))
free_cash_flow = ebit+depreciation+tax_payment+capex+change_in_nwc

free_cash_flow

cost_of_capital = 0.12
terminal_growth_rate = 0.02

terminal_value = (free_cash_flow[-1]*(1+terminal_growth_rate))/(cost_of_capital-terminal_growth_rate)

discount_factors = [(1/(1+cost_of_capital)) ** i for i in range(1, 6)]

dcf_value = (sum(free_cash_flow[1:] * discount_factors) + terminal_value*discount_factors[-1])

output = pd.DataFrame([sales, ebit, free_cash_flow],
    index=['Sales', 'EBIT', 'Free Cash Flow']).round(2)

iterations = 10000

def run_mcs():

    #Create probability distributions

    sales_growth_dist = np.random.normal(loc=0.1, scale=0.01, size=iterations)
    ebitda_margin_dist = np.random.normal(loc=0.14, scale=0.02, size=iterations)
    nwc_percent_dist = np.random.normal(loc=0.24, scale=0.01, size=iterations)

    #Calculate DCF value for each set of random inputs
    output_distribution = []
    for i in range(iterations):
        for year in range(1, 6):
            sales[year] = sales[year-1]*(1+sales_growth_dist[0])
        ebitda = sales*ebitda_margin_dist[i]
        depreciation=sales*depr_percent
        ebit=ebitda-depreciation
        nwc=sales*ebitda_margin_dist[i]
        change_in_nwc=nwc.shift(1)-nwc
        capex=-(sales*capex_percent)
        tax_payment=-ebit*tax_rate
        tax_payment=tax_payment.apply(lambda x: min(x, 0))
        free_cash_flow = ebit+depreciation+tax_payment+capex+change_in_nwc

        #DCF Valuation
        terminal_value = (free_cash_flow[-1] * 1.02) / (cost_of_capital - 0.02)
        free_cash_flow[-1] += terminal_value
        discount_factors = [(1 / (1 + cost_of_capital)) ** i for i in range (1,6)]
        dcf_value=sum(free_cash_flow[1:]*discount_factors)
        output_distribution.append(dcf_value)

    return output_distribution

mcs_npv_lst = run_mcs()

plt.hist(mcs_npv_lst, density=True, bins=30)
mn, mx = plt.xlim()
plt.xlim(mn, mx)
kde_xs = np.linspace(mn, mx, 300)
kde = st.gaussian_kde(mcs_npv_lst)
plt.plot(kde_xs, kde.pdf(kde_xs), label="PDF", color="purple")
plt.legend(loc="upper left")

plt.ylabel('Probability')
plt.xlabel('NPV')
plt.title("Monte Carlo Simulation of NPV from DCF Model")