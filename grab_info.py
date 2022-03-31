import pandas_datareader
import yfinance as yf
import pandas as pd

ticker_input = "MSFT"
get_data = yf.Ticker(ticker_input)

is_unorg = get_data.financials
bs_unorg = get_data.balance_sheet

bs_unorg_current = bs_unorg.iloc[:,0]/1000000
bs_unorg_past_year = bs_unorg.iloc[:,1]/1000000
bs_unorg_two_past_year = bs_unorg.iloc[:,2]/1000000
bs_reindex_list = [
    "Cash", "Short Term Investments", "Net Receivables", "Inventory", "Other Current Assets", "Total Current Assets",
    "Property Plant Equipment", "Long Term Investments", "Net Tangible Assets", "Other Assets", "Total Assets",
    "Accounts Payable", "Short Long Term Debt", "Other Current Liab", "Total Current Liabilities",
    "Long Term Debt", "Other Liab", "Total Liab",
    "Common Stock", "Treasury Stock", "Retained Earnings", "Other Stockholder Equity", "Total Stockholder Equity"
    ]


bs_org_current = bs_unorg_current.reindex(bs_reindex_list)
bs_org_past_year = bs_unorg_past_year.reindex(bs_reindex_list)
bs_org_two_past_year = bs_unorg_two_past_year.reindex(bs_reindex_list)

is_unorg_current = is_unorg.iloc[:,0]/1000000
is_unorg_past_year = is_unorg.iloc[:,1]/1000000
is_unorg_two_past_year = is_unorg.iloc[:,2]/1000000
is_reindex_list = [
    "Total Revenue", "Cost Of Revenue", "Gross Profit",
    "Selling General Administrative", "Research Development", "Other Operating Expenses",
    "Operating Income", "Non Recurring", "Other Items", "Reconciled Depreciation",
    "Ebit", 
    "Interest Expense", "Minority Interest", "Income Before Tax", 
    "Income Tax Expense", "Total Other Income Expense Net",
    "Net Income"
    ]

is_org_current = is_unorg_current.reindex(is_reindex_list)
is_org_past_year = is_unorg_past_year.reindex(is_reindex_list)
is_org_two_past_year = is_unorg_two_past_year.reindex(is_reindex_list)

org_current_col = [
    is_org_current["Total Revenue"], 
    is_org_current["Cost Of Revenue"],
    is_org_current["Gross Profit"], 
    is_org_current["Selling General Administrative"],
    is_org_current["Research Development"],
    is_org_current["Other Operating Expenses"],
    is_org_current["Operating Income"],
    is_org_current["Non Recurring"],
    is_org_current["Other Items"],
    is_org_current['Reconciled Depreciation'],
    is_org_current["Ebit"],
    is_org_current["Income Tax Expense"]/is_org_current["Income Before Tax"],
    is_org_current["Ebit"]*(1-(is_org_current["Income Tax Expense"]/is_org_current["Income Before Tax"])),
    "Depreciation",
    "ATOCF",
    "  ",
    "AR",
    "Inventory",
    "AP",
    "Net Working Capital",
    "∆NWC", 
    "  ",
    "Factory",
    "Equipment",
    "CAPEX",
    "  ",
    "Disposal Proceeds",
    "Tax Impact of Disposal",
    "  ",
    "Free Cash Flow",
    "Cumulative Cash Flow"
    ]

ICF_dataframe = pd.DataFrame(
    index=[
        "Net Sales", 
        "COGS", 
        "Gross Profit", 
        "SG&A", "R&D", "Other Operating",
        "Operating Income",
        "Non Reccuring", "Other Items",
        "EBIT",
        "Effective Tax Rate",
        "NOPAT",
        "Add: Depreciation",
        "ATOCF",
        "  ",
        "AR",
        "Inventory",
        "AP",
        "Net Working Capital",
        "∆NWC", 
        "  ",
        "Factory",
        "Equipment",
        "CAPEX",
        "  ",
        "Disposal Proceeds",
        "Tax Impact of Disposal",
        "  ",
        "Free Cash Flow",
        "Cumulative Cash Flow"
        ],
    columns=["2019", "2020", "2021", "2022", "2023", "2024"]
)

ICF_dataframe = ICF_dataframe.replace({"2022": org_current_col})

is_org_current
