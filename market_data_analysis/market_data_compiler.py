import json
import yfinance as yf
from datetime import datetime



def open_json_file(file_path):
	with open(file_path, 'r') as json_file:
		json_dict = json.load(json_file)
		return(json_dict)

def get_stock_data():
	nasdaq_dict = open_json_file('market_data_analysis/nasdaq_stocks.json')
	nasdaq_list = []
	for nasdaq_stock in nasdaq_dict.keys():
		try:
			stock_dict = get_specific_stock_data(nasdaq_stock)
		except:
			continue
		if stock_dict == None:
			continue
		if stock_dict['opportunity_percentage'] > 0:
			nasdaq_list.append(stock_dict)
	new_nasdaq_list = sorted(nasdaq_list, key=lambda k: k['opportunity_percentage']) 
	nyse_dict = open_json_file('market_data_analysis/nyse_stocks.json')
	nyse_list = []
	for nyse_stock in nyse_dict.keys():
		try:
			stock_dict = get_specific_stock_data(nyse_stock)	
		except:
			continue
		if stock_dict == None:
			continue
		if stock_dict['opportunity_percentage'] > 0:
			nyse_list.append(stock_dict)
	new_nyse_list = sorted(nyse_list, key=lambda k: k['opportunity_percentage']) 
	write_opportunity_json(new_nasdaq_list, new_nyse_list)


def write_opportunity_json(nasdaq_list, nyse_list):
	with open('market_data_analysis/stock_opportunities.json', 'r') as json_file:
		current_dict = json.load(json_file)
	with open('market_data_analysis/stock_opportunities.json', 'w') as json_file1:
		current_dict['NASDAQ'][str(datetime.now())] = nasdaq_list
		current_dict['NYSE'][str(datetime.now())] = nyse_list
		json.dump(current_dict, json_file1)

def get_specific_stock_data(ticker):
	"""yf_stock.info: ['zip', 'sector', 'fullTimeEmployees', 'longBusinessSummary', 
	'city', 'phone', 'state', 'country', 'companyOfficers', 'website', 'maxAge', 
	'address1', 'industry', 'previousClose', 'regularMarketOpen', 'twoHundredDayAverage', 
	'trailingAnnualDividendYield', 'payoutRatio', 'volume24Hr', 'regularMarketDayHigh', 
	'navPrice', 'averageDailyVolume10Day', 'totalAssets', 'regularMarketPreviousClose', 
	'fiftyDayAverage', 'trailingAnnualDividendRate', 'open', 'toCurrency', 'averageVolume10days', 
	'expireDate', 'yield', 'algorithm', 'dividendRate', 'exDividendDate', 'beta', 'circulatingSupply',
	 'startDate', 'regularMarketDayLow', 'priceHint', 'currency', 'trailingPE', 'regularMarketVolume', 
	 'lastMarket', 'maxSupply', 'openInterest', 'marketCap', 'volumeAllCurrencies', 'strikePrice',
	  'averageVolume', 'priceToSalesTrailing12Months', 'dayLow', 'ask', 'ytdReturn', 'askSize',
	   'volume', 'fiftyTwoWeekHigh', 'forwardPE', 'fromCurrency', 'fiveYearAvgDividendYield', 'fiftyTwoWeekLow', 'bid', 
	'tradeable', 'dividendYield', 'bidSize', 'dayHigh', 'exchange', 'shortName', 'longName', 
	'exchangeTimezoneName', 'exchangeTimezoneShortName', 'isEsgPopulated', 'gmtOffSetMilliseconds', 
	'quoteType', 'symbol', 'messageBoardId', 'market', 'annualHoldingsTurnover', 'enterpriseToRevenue', 
	'beta3Year', 'profitMargins', 'enterpriseToEbitda', '52WeekChange', 'morningStarRiskRating', 'forwardEps',
	 'revenueQuarterlyGrowth', 'sharesOutstanding', 'fundInceptionDate', 'annualReportExpenseRatio', 
	 'bookValue', 'sharesShort', 'sharesPercentSharesOut', 'fundFamily', 'lastFiscalYearEnd',
	  'heldPercentInstitutions', 'netIncomeToCommon', 'trailingEps', 'lastDividendValue', 
	  'SandP52WeekChange', 'priceToBook', 'heldPercentInsiders', 'nextFiscalYearEnd', 
	  'mostRecentQuarter', 'shortRatio', 'sharesShortPreviousMonthDate', 'floatShares', 'enterpriseValue', 
	  'threeYearAverageReturn', 'lastSplitDate', 'lastSplitFactor', 'legalType', 'morningStarOverallRating', 
	  'earningsQuarterlyGrowth', 'dateShortInterest', 'pegRatio', 'lastCapGain', 'shortPercentOfFloat', 
	  'sharesShortPriorMonth', 'category', 'fiveYearAverageReturn', 'regularMarketPrice', 'logo_url']"""
	yf_stock = yf.Ticker(ticker)
	info_dict = yf_stock.info
	if 'priceToBook' in info_dict.keys():
		priceToBook = info_dict['priceToBook']
	else:
		return None
	if 'forwardPE' in info_dict.keys():
		forwardPE = info_dict['forwardPE']
	else:
		return None
	if 'sharesOutstanding' in info_dict.keys():
		sharesOutstanding = info_dict['sharesOutstanding']
	else:
		return None
	if 'trailingAnnualDividendRate' in info_dict.keys():
		trailingAnnualDividendRate = info_dict['trailingAnnualDividendRate']
	else:
		return None
	response = strategy_1(forwardPE, priceToBook, trailingAnnualDividendRate)
	print("{} Company:{} PB:{} PE:{} Nº Shares:{} Dividend:{}".format(response, ticker, priceToBook, forwardPE, sharesOutstanding, trailingAnnualDividendRate))
	if response:
		data = yf_stock.history(start="2019-06-16", end="2020-06-16")
		last_quote = (data.tail(1)['Close'].iloc[0])
		trailingEps = info_dict['trailingEps']
		growth = get_growth_rate(data)
		graham_value = graham_value_formula(trailingEps, growth)
		percetange_diference_value = ((graham_value - last_quote)/last_quote)*100
		return {'ticker': ticker, 'opportunity_percentage': percetange_diference_value, 'priceToBook': priceToBook, 'forwardPE': forwardPE, 'sharesOutstanding': sharesOutstanding, 'trailingAnnualDividendRate': trailingAnnualDividendRate}

	else:
		return None
	#print(graham_value_formula(float(trailingEps), ))
	#print('totalAssets:{} \n priceHint:{} \n dividendRate:{} \n trailingAnnualDividendRate:{} \n trailingEps:{} \n marketCap :{} \n profitMargins:{} \n enterpriseValue:{} \n fiveYearAverageReturn:{}'.format(total_assets, price_hint, dividend_rate, trailingAnnualDividendRate, trailingEps, market_capitalization, profit_margins, enterprise_value, five_year_average_return))

def strategy_1(pe,pb,dividend_rate):
	if pe < 9:
		if pb < 1.2:
			if dividend_rate > 1:
				return True
			else:
				return False
		else:
			return False
	else:
		return False


def get_growth_rate(data):
	first_quote = data.tail(-1)['Close'].iloc[0]
	last_quote = data.tail(1)['Close'].iloc[0]
	growth = ((last_quote - first_quote)/first_quote)*100
	return growth


def graham_value_formula(EPS, g):
	valuation = (EPS*(7 + 1*g)*4.4)/3.7
	return valuation




	



