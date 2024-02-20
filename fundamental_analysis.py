import requests
import matplotlib.pyplot as plt

# Function to fetch financial data using Alpha Vantage API
def get_income_statement(symbol):
    API_KEY = 'Your_api_key'
    url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_cashflow_statement(symbol):
    API_KEY = 'Your_api_key'
    url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_balance_sheet(symbol):
    API_KEY = 'Your_api_key'
    url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_earnings(symbol):
    API_KEY = 'Your_api_key'
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_revenue(symbol):
    data = get_income_statement(symbol)
    
    if data:
        yearly_rev = []
        annual_rep = data.get("annualReports") 
        for finance_data in annual_rep:
            yearly_rev.append(float(finance_data.get("totalRevenue"))/1000000.0)

        
        return yearly_rev
        
    else:
        print("data could not be found")
        
def get_gp(symbol):
    data = get_income_statement(symbol)
    yearly_gp = []
    if data:
        annual_rep = data.get("annualReports") 
        for finance_data in annual_rep:
            yearly_gp.append(float(finance_data.get("grossProfit"))/1000000.0)
        return yearly_gp
        
    else:
        print("data could not be found")
        
def get_net_income(symbol):
    data = get_income_statement(symbol)
    yearly_ni = []
    if data:
        annual_rep = data.get("annualReports") 
        for finance_data in annual_rep:
            yearly_ni.append(float(finance_data.get("netIncome"))/1000000.0)
        return yearly_ni
        
    else:
        print("data could not be found")
def get_dates(symbol):
    data = get_income_statement(symbol)
    dates = []
    if data:
        annual_rep = data.get("annualReports") 
        for finance_data in annual_rep:
            dates.append(finance_data.get("fiscalDateEnding"))
        dates.reverse()
        return dates

def get_cogs(symbol):
    data = get_income_statement(symbol)
    yearly_cogs = []
    if data:
        annual_rep = data.get("annualReports")
        for finance_data in annual_rep:
            yearly_cogs.append(float(finance_data.get("costOfRevenue"))/1000000.0)
        return yearly_cogs

def get_sga(symbol):
    data = get_income_statement(symbol)
    yearly_sga = []
    if data:
        annual_rep = data.get("annualReports")
        for finance_data in annual_rep:
            yearly_sga.append(float(finance_data.get("sellingGeneralAndAdministrative"))/1000000.0)
        return yearly_sga

def get_dep_and_amort(symbol):
    data = get_income_statement(symbol)
    yearly_da = []
    if data:
        annual_rep = data.get("annualReports")
        for finance_data in annual_rep:
            yearly_da.append(float(finance_data.get('depreciationAndAmortization'))/1000000.0)
        return yearly_da
    
def get_capex(symbol):
    data = get_cashflow_statement(symbol)
    yearly_capex= []
    if data:
        annual_rep = data.get("annualReports")
        for finance_data in annual_rep:
            yearly_capex.append(float(finance_data.get('capitalExpenditures'))/1000000.0)
        return yearly_capex


def get_change_working_capital(symbol):
    data = get_cashflow_statement(symbol)
    yearly_op_assets= []
    yearly_op_liab = []
    yearly_work_capital = []
    if data:
        annual_rep = data.get("annualReports")
        for finance_data in annual_rep:
            yearly_op_assets.append(float(finance_data.get('changeInOperatingAssets'))/1000000.0)
            yearly_op_liab.append(float(finance_data.get('changeInOperatingLiabilities'))/1000000.0)
        for i in range(len(yearly_op_assets)):
            yearly_work_capital.append(yearly_op_assets[i] - yearly_op_liab[i])
        return yearly_work_capital

def get_eps(symbol):
    data = get_earnings(symbol)
    yearly_eps= []
    if data:
        annual_rep = data.get("annualEarnings")
        for finance_data in annual_rep:
            yearly_eps.append(float(finance_data.get('reportedEPS')))
        return yearly_eps
    
def calc_cagr(lst):
    '''
    Given a list of values, calculate the CAGR

    Parameters
    ----------
    lst : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    t = len(lst)
    cagr = (lst[len(lst)-1]/lst[0])**(1/t) - 1
    return cagr

def graph_financials(revenue, gross_profit, net_income, dates, symbol):
    x = range(len(dates))  # x-axis based on the number of dates
    
    revenue.reverse()
    gross_profit.reverse()
    net_income.reverse()
    
    plt.plot(x, revenue, label='Revenue')
    plt.plot(x, gross_profit, label='Gross Profit')
    plt.plot(x, net_income, label='Net Income')
    
    plt.xlabel('Ending Fiscal Date')
    plt.ylabel('Amount USD (millions)')
    plt.title(f'{symbol} Financials Over Time')
    plt.xticks(x, dates, rotation=45)  # Rotate x-axis labels for readability
    plt.legend()  # Show legend
    
    plt.tight_layout()  # Ensure labels fit into the plot area
    plt.show()

if __name__ == '__main__':
    symbol = input("Stock ticker symbol:\n")
    #symbol2 = input("Stock to compare: ")
    
    yoy_rev = get_revenue(symbol)
    gross_profit = get_gp(symbol)
    net_income = get_net_income(symbol)
    dates = get_dates(symbol)
    
    graph_financials(yoy_rev, gross_profit, net_income, dates, symbol)
    
    rev_cagr = round(calc_cagr(yoy_rev),4)*100
    print(f"The cagr for Revenue over the time frame is {rev_cagr}%")
    
    gp_cagr = round(calc_cagr(gross_profit),4)*100
    print(f"The cagr for Gross Profit over the time frame is {gp_cagr}%")
    
    ni_cagr = (calc_cagr(net_income))*100
    print(f"The cagr for Net Income over the time frame is {ni_cagr}%")
    
    #Calculate Unlevered Free Cash flow using : UCF = Net income + D&A - Change in working capital - Capex
    d_and_a = get_dep_and_amort(symbol)
    capex = get_capex(symbol)
    cwc = get_change_working_capital(symbol)
    
    step_one = [a + b for a, b in zip(net_income, d_and_a)]
    step_two = [a - b for a, b in zip(step_one, cwc)]
    ucf = [a - b for a, b in zip(step_two, capex)]
   
    # Plot UCF over time 
    x = range(len(dates))
    plt.title(f'{symbol} Unlevered Cashflow Over Time')
    plt.plot(x, ucf, label = 'Unlevered Cashflow')
    plt.xticks(x, dates, rotation=45)
    plt.xlabel('Ending Fiscal Date')
    plt.ylabel('Amount USD (millions)')
    plt.legend()
    plt.show()
    
    print(f"The most recent unlevered cashflow for {symbol} was ${ucf[len(ucf)-1]} Million")
    
    yearly_eps = get_eps(symbol)
    
    x = range(len(dates))
    eps_in_frame = yearly_eps[0:len(dates)]
    eps_in_frame = eps_in_frame[::-1]
    plt.title(f'{symbol} Reported EPS Over Time')
    plt.plot(x, eps_in_frame, label = 'EPS')
    plt.xticks(x, dates, rotation=45)
    plt.xlabel('Ending Fiscal Date')
    plt.ylabel('Earnings per share (USD)')
    plt.legend()
    plt.show()
    
    #print(eps_in_frame)
    
    
    
