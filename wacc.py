import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression


ticker = "AAPL"

class WACC_data():

    def __init__(self, ticker):
        print("Initializing...")
        self.ticker = ticker

        self.ticker_data = yf.Ticker(self.ticker)

        #Calc Risk Free Rate
        get_risk_free_rate = yf.Ticker("^TNX").history(period="1d", interval="1d")
        self.risk_free_rate = get_risk_free_rate["Close"][0]

        #Calc Expected Market Return
        spy_10y_historical_data = yf.Ticker("SPY").history(period="120mo", interval="1mo").dropna()
        expected_market_return = (spy_10y_historical_data["Close"][-1]/spy_10y_historical_data["Close"][0])**(1/10)-1
        self.expected_market_return = expected_market_return

        #Get Balance Sheet Data
        self.balance_sheet_data = yf.Ticker(self.ticker).balance_sheet

        #Get Income Statement Data
        self.income_statement_data = yf.Ticker(self.ticker).financials

    def get_capm(self):
        print("Calculating Cost of Equity...")
        #Calculate Beta
        stock_history = self.ticker_data.history(period="60mo", interval="1mo")
        spy_history = yf.Ticker("SPY").history(period="60mo", interval="1mo")

        stock_history = stock_history.dropna()
        spy_history = spy_history.dropna()

        stock_history["Continuous Return"] = np.log(stock_history["Close"] / stock_history["Close"].shift(1))
        spy_history["Continuous Return"] = np.log(spy_history["Close"] / spy_history["Close"].shift(1))

        y = np.array(stock_history["Continuous Return"][1:]).reshape(-1, 1)
        x = np.array(spy_history["Continuous Return"][1:]).reshape(-1, 1)


        model = LinearRegression().fit(x, y)
        beta = float(model.coef_)

        #Calculate CAPM
        self.risk_free_rate = self.risk_free_rate/100
        capm = self.risk_free_rate + beta * (self.expected_market_return - self.risk_free_rate)
        return capm

    def get_debt_value(self):
        print("Calculating Value of Debt")
        short_long_term_debt = float(self.balance_sheet_data[12:13].iloc[:, 0])
        long_term_debt = float(self.balance_sheet_data[20:21].iloc[:, 0])
        total_debt = short_long_term_debt + long_term_debt

        return total_debt

    def get_market_cap(self):
        print("Calculating Value of Equity")
        ticker_info = self.ticker_data.info
        market_cap = ticker_info['marketCap']

        return market_cap

    def get_tax_rate(self):
        print("Calculating Tax Rate")
        income_tax_expense = self.income_statement_data.iloc[14, 0]
        earnings_before_tax = self.income_statement_data.iloc[2, 0]
        tax_rate = income_tax_expense/earnings_before_tax

        return tax_rate

    def get_cost_of_debt(self):
        print("Calculating Cost of Debt")
        interest_expense = -self.income_statement_data.iloc[10, 0]

        total_debt = self.get_debt_value()
        effective_tax_rate = self.get_tax_rate()

        cost_of_debt = (interest_expense * (1 - effective_tax_rate)) / total_debt

        return cost_of_debt


def get_WACC(ticker):

    #Retrieving Data from WACC_data class
    WACC_data_instance = WACC_data(ticker)

    equity_value = WACC_data_instance.get_market_cap()
    debt_value = WACC_data_instance.get_debt_value()
    cost_of_equity = WACC_data_instance.get_capm()
    cost_of_debt = WACC_data_instance.get_cost_of_debt()
    tax_rate = WACC_data_instance.get_tax_rate()

    #Intermediate Calculations
    total_value = equity_value + debt_value
    percent_equity = equity_value/total_value
    percent_debt = debt_value/total_value

    #WACC Calculation
    wacc = (percent_equity * cost_of_equity) + (percent_debt * cost_of_debt * (1 - tax_rate))
    return wacc

if __name__ == 'main':
    get_WACC(ticker)