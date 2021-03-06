from market_data_analysis import market_data_compiler
from market_opperations import alpaca
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json

sched = BlockingScheduler()

def send_mail(stock_data):
	nasdaq_list = stock_data["NASDAQ"]["{}".format(datetime.now().date())]
	nyse_list = stock_data["NYSE"]["{}".format(datetime.now().date())]
	content_html = '<h1><strong>Nasdaq</strong></h1>'
	for stock in nasdaq_list[:10]:
		stock_ticker = stock["ticker"]
		opportunity = stock["opportunity_percentage"]
		pe = stock["forwardPE"]
		pb = stock["priceToBook"]
		dividends = stock["trailingAnnualDividendRate"]
		content_html += "<br><p>Stock: <strong>{}</strong>  Graham valuation: <strong>{}%</strong>  PE: <strong>{}</strong>  PB: <strong>{}</strong>  Dividends: <strong>{}</strong></p>".format(stock_ticker, opportunity, pe, pb, dividends)
	content_html += "<br><h1><strong>NYSE</strong></h1>"
	for stock in nyse_list[:10]:
		stock_ticker = stock["ticker"]
		opportunity = stock["opportunity_percentage"]
		pe = stock["forwardPE"]
		pb = stock["priceToBook"]
		dividends = stock["trailingAnnualDividendRate"]
		content_html += "<br><p>Stock:<strong>{}</strong>  Graham valuation: <strong>{}%</strong>  PE: <strong>{}%</strong>  PB: <strong>{}%</strong>  Dividends: <strong>{}%</strong></p>".format(stock_ticker, opportunity, pe, pb, dividends)
	message = Mail(
    from_email='mamingo@uc.cl',
    to_emails='mamingo@uc.cl',
    subject='Stock opportunities {}'.format(datetime.now().date()),
    html_content=content_html)
	try:
	    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
	    response = sg.send(message)
	    print(response.status_code) 
	    print(response.body)
	    print(response.headers)
	except Exception as e:
		print(e.message)


def get_data():
	with open("market_data_analysis/stock_opportunities.json", 'r') as json_file:
		json_dict = json.load(json_file)
		return(json_dict)

@sched.scheduled_job('cron', day_of_week='mon-sat', hour='14,17,22')
def scheduled_job():
    market_data_compiler.get_stock_data()
    data_dict = get_data()
    send_mail(data_dict)


if __name__ == '__main__':
	market_data_compiler.get_stock_data()
	data_dict = get_data()
	send_mail(data_dict)
	sched.start()