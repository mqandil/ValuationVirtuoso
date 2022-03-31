import yfinance as yf
import pandas as pd
from datetime import date
from wacc import get_WACC as gw
from npv import npv


#Create Date Headings
current_date = date.today()
current_year = current_date.year

year_columns_list = [
    current_year - 2,
    current_year - 1,
    current_year,
    current_year + 1,
    current_year + 2,
    current_year + 3,
    current_year + 4
]

#Download Financial Statements
ticker = "MSFT"

cashflow_statement_info = yf.Ticker(ticker).cashflow
income_statement_info = yf.Ticker(ticker).financials
balance_sheet_info = yf.Ticker(ticker).balance_sheet
company_info = yf.Ticker(ticker).info

#Get ICF Info
current_depreciation = cashflow_statement_info.iloc[11, 0]
past_depreciation = cashflow_statement_info.iloc[11, 1]

current_revenue = income_statement_info.iloc[15, 0]
past_revenue = income_statement_info.iloc[15, 1]

current_cost_of_goods_sold = income_statement_info.iloc[17, 0]
past_cost_of_goods_sold = income_statement_info.iloc[17, 1]

current_gross_profit = income_statement_info.iloc[6, 0]
past_gross_profit = income_statement_info.iloc[6, 1]

current_sga_expense = income_statement_info.iloc[5, 0]
past_sga_expense = income_statement_info.iloc[5, 1]

current_rd_expense = income_statement_info.iloc[0, 0]
past_rd_expense = income_statement_info.iloc[0, 1]

current_ebit = income_statement_info.iloc[7, 0]
past_ebit = income_statement_info.iloc[7, 1]

current_income_tax_expense = income_statement_info.iloc[14, 0]
current_earnings_before_tax = income_statement_info.iloc[2, 0]
current_tax_rate = current_income_tax_expense/current_earnings_before_tax

past_income_tax_expense = income_statement_info.iloc[14, 1]
past_earnings_before_tax = income_statement_info.iloc[2, 1]
past_tax_rate = past_income_tax_expense/past_earnings_before_tax


#Net Working Capital
current_total_current_assets = balance_sheet_info.iloc[19, 0]
past_total_current_assets = balance_sheet_info.iloc[19, 1]

current_total_current_liabilities = balance_sheet_info.iloc[15, 0]
past_total_current_liabilities = balance_sheet_info.iloc[15, 1]

current_net_working_capital = current_total_current_assets - current_total_current_liabilities
past_net_working_capital = past_total_current_assets - past_total_current_liabilities

current_change_in_net_working_capital = current_net_working_capital - past_net_working_capital
past_change_in_net_working_capital = 0


#Capital Expenditures
current_net_tangible_assets = balance_sheet_info.iloc[20, 0]
past_net_tangible_assets = balance_sheet_info.iloc[20, 1]

current_capital_expenditures = current_net_tangible_assets - past_net_tangible_assets
past_capital_expenditures = 0


#Free Cash Flows
current_free_cash_flow = (current_ebit*(1 - current_tax_rate)+current_depreciation)-current_change_in_net_working_capital-current_capital_expenditures
past_free_cash_flow = 0


#OCF Projections

revenue_growth = [
    (income_statement_info.iloc[15, 0]-income_statement_info.iloc[15, 1])/income_statement_info.iloc[15, 1],
    (income_statement_info.iloc[15, 1]-income_statement_info.iloc[15, 2])/income_statement_info.iloc[15, 2],
    (income_statement_info.iloc[15, 2]-income_statement_info.iloc[15, 3])/income_statement_info.iloc[15, 3]
]
average_revenue_growth = sum(revenue_growth)/len(revenue_growth)
projected_revenues = [current_revenue]
for value in range(5):
    projected_revenues.append(projected_revenues[-1]*(1+average_revenue_growth))


cogs_to_sales = [
    (income_statement_info.iloc[17, 0])/income_statement_info.iloc[15, 0],
    (income_statement_info.iloc[17, 1])/income_statement_info.iloc[15, 1],
    (income_statement_info.iloc[17, 2])/income_statement_info.iloc[15, 2]
]
average_cogs_to_sales = sum(cogs_to_sales)/len(cogs_to_sales)
projected_cogs = [current_cost_of_goods_sold]
i=1
for value in range(5):
    projected_cogs.append(projected_revenues[i]*average_cogs_to_sales)
    i+=1

projected_gross_profit = [current_gross_profit]
i=1
for value in range(5):
    projected_gross_profit.append(projected_revenues[i]-projected_cogs[i])
    i+=1


sga_to_sales = [
    (income_statement_info.iloc[5, 0])/income_statement_info.iloc[15, 0],
    (income_statement_info.iloc[5, 1])/income_statement_info.iloc[15, 1],
    (income_statement_info.iloc[5, 2])/income_statement_info.iloc[15, 2]
]
average_sga_to_sales = sum(sga_to_sales)/len(sga_to_sales)
projected_sga_expenses = [current_sga_expense]
i=1
for value in range(5):
    projected_sga_expenses.append(projected_revenues[i]*average_sga_to_sales)
    i+=1


rd_to_sales = [
    (income_statement_info.iloc[0, 0])/income_statement_info.iloc[15, 0],
    (income_statement_info.iloc[0, 1])/income_statement_info.iloc[15, 1],
    (income_statement_info.iloc[0, 2])/income_statement_info.iloc[15, 2]
]
average_rd_to_sales = sum(rd_to_sales)/len(rd_to_sales)
projected_rd_expenses = [current_rd_expense]
i=1
for value in range(5):
    projected_rd_expenses.append(projected_revenues[i]*average_rd_to_sales)
    i+=1


projected_ebit = [current_ebit]
i=1
for value in range(5):
    projected_ebit.append(projected_gross_profit[i]-projected_sga_expenses[i]-projected_rd_expenses[i])
    i+=1


average_tax_rate = (current_tax_rate + past_tax_rate)/2
proj_ebit_tax_shield = [current_ebit*(1 - current_tax_rate)]
i=1
for value in range(5):
    proj_ebit_tax_shield.append(projected_ebit[i]*(1-average_tax_rate))
    i+=1


depreciation_to_sales = [
    (cashflow_statement_info.iloc[11, 0])/income_statement_info.iloc[15, 0],
    (cashflow_statement_info.iloc[11, 1])/income_statement_info.iloc[15, 1],
    (cashflow_statement_info.iloc[11, 2])/income_statement_info.iloc[15, 2]
]
average_depreciation_to_sales = sum(depreciation_to_sales)/len(depreciation_to_sales)
projected_depreciation = [current_depreciation]
i=1
for value in range(5):
    projected_depreciation.append(projected_revenues[i]*average_depreciation_to_sales)
    i+=1


projected_ocf = [proj_ebit_tax_shield[0]+current_depreciation]
i=1
for value in range(5):
    projected_ocf.append(proj_ebit_tax_shield[i]+projected_depreciation[i])
    i+=1



#NWC Projections
tca_to_sales = [
    (balance_sheet_info.iloc[19, 0])/income_statement_info.iloc[15, 0],
    (balance_sheet_info.iloc[19, 1])/income_statement_info.iloc[15, 1],
    (balance_sheet_info.iloc[19, 2])/income_statement_info.iloc[15, 2]
]
average_tca_to_sales = sum(tca_to_sales)/len(tca_to_sales)
projected_total_current_assets = [current_total_current_assets]
i=1
for value in range(5):
    projected_total_current_assets.append(projected_revenues[i]*average_tca_to_sales)
    i+=1


tcl_to_sales = [
    (balance_sheet_info.iloc[15, 0])/income_statement_info.iloc[15, 0],
    (balance_sheet_info.iloc[15, 1])/income_statement_info.iloc[15, 1],
    (balance_sheet_info.iloc[15, 2])/income_statement_info.iloc[15, 2]
]
average_tcl_to_sales = sum(tcl_to_sales)/len(tcl_to_sales)
projected_total_current_liabilities = [current_total_current_liabilities]
i=1
for value in range(5):
    projected_total_current_liabilities.append(projected_revenues[i]*average_tcl_to_sales)
    i+=1


projected_net_working_capital = [current_net_working_capital]
i=1
for value in range(5):
    projected_net_working_capital.append(projected_total_current_assets[i]-projected_total_current_liabilities[i])
    i+=1


projected_change_in_net_working_capital = [current_change_in_net_working_capital]
i=1
for value in range(5):
    projected_change_in_net_working_capital.append(projected_net_working_capital[i]-projected_net_working_capital[i-1])
    i+=1


#CAPEX Projections
gross_tangible_assets_to_sales = [
    (balance_sheet_info.iloc[20, 0])/income_statement_info.iloc[15, 0],
    (balance_sheet_info.iloc[20, 1])/income_statement_info.iloc[15, 1],
    (balance_sheet_info.iloc[20, 2])/income_statement_info.iloc[15, 2]
]
average_gross_tangible_assets_to_sales = sum(gross_tangible_assets_to_sales)/len(gross_tangible_assets_to_sales)
projected_gross_tangible_assets = [current_net_tangible_assets]
i=1
for value in range(5):
    projected_gross_tangible_assets.append(projected_revenues[i]*average_gross_tangible_assets_to_sales)
    i+=1

projected_capital_expenditures = [current_capital_expenditures]
i=1
for value in range(5):
    projected_capital_expenditures.append(projected_gross_tangible_assets[i]-projected_gross_tangible_assets[i-1])
    i+=1


#FCF Projections
projected_free_cash_flow = [current_free_cash_flow]
i=1
for value in range(5):
    projected_free_cash_flow.append(projected_ocf[i]-projected_change_in_net_working_capital[i]-projected_capital_expenditures[i])
    i+=1







#OCF Data
current_year_fcf_data = [current_revenue, current_cost_of_goods_sold, 
    current_gross_profit, current_sga_expense, current_rd_expense, 
    current_ebit, current_ebit*(1 - current_tax_rate), current_depreciation, 
    current_ebit*(1 - current_tax_rate)+current_depreciation, 
    current_total_current_assets, current_total_current_liabilities,
    current_net_working_capital, current_change_in_net_working_capital, 
    current_capital_expenditures, current_free_cash_flow
]

past_year_fcf_data = [past_revenue, past_cost_of_goods_sold, 
    past_gross_profit, past_sga_expense, past_rd_expense, 
    past_ebit, past_ebit*(1 - past_tax_rate), past_depreciation, 
    past_ebit*(1 - past_tax_rate)+past_depreciation,
    past_total_current_assets, past_total_current_liabilities,
    past_net_working_capital, past_change_in_net_working_capital, 
    past_capital_expenditures, past_free_cash_flow
]

projections = []
i = 1
for value in range(5):
    projections.append([
        projected_revenues[i],
        projected_cogs[i],
        projected_gross_profit[i],
        projected_sga_expenses[i],
        projected_rd_expenses[i],
        projected_ebit[i],
        proj_ebit_tax_shield[i],
        projected_depreciation[i],
        projected_ocf[i],
        projected_total_current_assets[i],
        projected_total_current_liabilities[i],
        projected_net_working_capital[i],
        projected_change_in_net_working_capital[i],
        projected_capital_expenditures[i],
        projected_free_cash_flow[i]
    ])
    i+=1

#Long-Term Value
long_term_growth_rate = 0.012
wacc = gw(ticker)
y5_fcf = projections[4][14]

terminal_fcf = (y5_fcf*(1+long_term_growth_rate))/(wacc - long_term_growth_rate)
projections[4][14] += terminal_fcf


indexes = ["Revenue", "COGS", "Gross Profit", "SG&A Expense", 
    "R&D Expense", "EBIT", "EBIT * (1 - Tc)", "Depreciation", 
    "Operating Cash Flow", "Total Current Assets", "Total Current Liabilities",
    "Net Working Capital", "Change in Net Working Capital", "Capital Expenditures",
    "Free Cash Flow"
]

fcf_df = pd.DataFrame({
    year_columns_list[0]: past_year_fcf_data,
    year_columns_list[1]: current_year_fcf_data,
    year_columns_list[2]: projections[0],
    year_columns_list[3]: projections[1],
    year_columns_list[4]: projections[2],
    year_columns_list[5]: projections[3],
    year_columns_list[6]: projections[4]
    },
    indexes
)

fcf_projections = list(fcf_df.iloc[14, 2:7])

net_present_value = npv(wacc, fcf_projections)


#Share Price
value_of_operations = net_present_value + balance_sheet_info.iloc[10, 0]

short_long_term_debt = float(balance_sheet_info[12:13].iloc[:, 0])
long_term_debt = float(balance_sheet_info[20:21].iloc[:, 0])
total_debt = short_long_term_debt + long_term_debt

value_of_equity = value_of_operations - total_debt

shares_outstanding = company_info["sharesOutstanding"]
share_price = value_of_equity / shares_outstanding


share_price_data = pd.DataFrame(
    [net_present_value,
    value_of_operations, 
    total_debt,
    value_of_equity,
    shares_outstanding,
    share_price
    ],
    index=[
        'NPV',
        'Value of Ops',
        'Total Debt',
        'Equity Value',
        'Shares Outstanding',
        'Share Price'
    ]
)


print(share_price)