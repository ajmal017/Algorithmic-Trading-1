from market_data_analysis import market_data_compiler
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

sched = BlockingScheduler()
"""
def send_mail(stock_data):
	nasdaq_list = stock_data["NASDAQ"]["{}".format(datetime.date(datetime.now()))]
	nyse_list = stock_data["NYSE"]["{}".format(datetime.date(datetime.now()))]
	content_list = []
	content_list.append("NASDAQ")
	for stock in nasdaq_list[:10]:
		stock_ticker = stock["ticker"]
		opportunity = stock["opportunity_percentage"]
		pe = stock["forwardPE"]
		pb = stock["priceToBook"]
		dividends = stock["trailingAnnualDividendRate"]
		content_list.append("Stock: {}  Graham %: {}  PE: {}  PB: {}  Dividends: {}".format(stock_ticker, opportunity, pe, pb, dividends))
	content_list.append("NYSE")
	for stock in nyse_list[:10]:
		stock_ticker = stock["ticker"]
		opportunity = stock["opportunity_percentage"]
		pe = stock["forwardPE"]
		pb = stock["priceToBook"]
		dividends = stock["trailingAnnualDividendRate"]
		content_list.append("Stock: {}  Graham %: {}  PE: {}  PB: {}  Dividends: {}".format(stock_ticker, opportunity, pe, pb, dividends))
	complete_content = ""
	for content in content_list:
		complete_content.join("{} \n".format(content))
    SERVER = ""
    FROM = "mamingo@uc.cl"
    TO = ["mamingo@uc.cl"]
    SUBJECT = "Stock opportunities {}".format(datetime.datetime.now().date())
    message = ""From: {}\r\nTo: {}\r\nSubject: {}\r\n
    {}
    ".format(FROM, ",".join(TO), SUBJECT, complete_content)
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)
"""
def get_data():
	with open("market_data_analysis/stock_opportunities", 'r') as json_file:
		json_dict = json.load(json_file)
		return(json_dict)

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    pmarket_data_compiler.get_stock_data()


if __name__ == '__main__':
	pmarket_data_compiler.get_stock_data()
	sched.start()