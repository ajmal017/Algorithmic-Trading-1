import csv
import json

def populate_nasdaq_json():
	companies_dict = {}
	with open('csv Files/Nasdaq_Company_List.csv', newline='') as nasdaq_csvfile:
		reader = csv.DictReader(nasdaq_csvfile)
		for row in reader:
			#If market cap is in the billions
			if 'B' in str(row['MarketCap']):
				companies_dict[row['Symbol']] = {'Name':row['Name'], 'Sector':row['Sector'], 'Industry':row['industry']}
	with open('NASDAQ_Stocks.json', 'w') as nasdaq_json:
		json.dump(companies_dict, nasdaq_json)

def populate_nyse_json():
	companies_dict = {}
	with open('csv Files/NYSE_Company_List.csv', newline='') as nyse_csvfile:
		reader = csv.DictReader(nyse_csvfile)
		for row in reader:
			#If market cap is in the billions
			if 'B' in str(row['MarketCap']):
				companies_dict[row['Symbol']] = {'Name':row['Name'], 'Sector':row['Sector'], 'Industry':row['industry']}
	with open('NYSE_Stocks.json', 'w') as nyse_json:
		json.dump(companies_dict, nyse_json)
			


if __name__ == '__main__':
	populate_nasdaq_json()
	populate_nyse_json()