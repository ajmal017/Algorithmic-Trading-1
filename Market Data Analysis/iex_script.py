"""Data provided by IEX Cloud https://iexcloud.io."""
from iexfinance import Stock
from pylivetrader import *

def initialize(context):
    # These are the sectors we're interested in trading.
    # They can be individually commented out if you wish to avoid one sector
    # or another.
    context.sectors = [
        'Basic Materials',
        'Consumer Cyclical',
        'Financial Services',
        'Real Estate',
        'Consumer Defensive',
        'Healthcare',
        'Utilities',
        'Communication Services',
        'Energy',
        'Industrials',
        'Technology'
    ]

    context.months_until_rebalance = 1
    schedule_function(try_rebalance,
                      date_rule=date_rules.month_start(),
                      time_rule=time_rules.market_open())

stock_batch = Stock(['AAPL', 'TSLA', 'MSFT'])
stock_batch.get_financials()

def try_rebalance(context, data):
    # See if it's time to rebalance every month.
    # We'll reevaluate our positions once every three months.
    if context.months_until_rebalance == 1:
        update_target_securities(context)
        rebalance(context)
        context.months_until_rebalance = 3
    else:
        context.months_until_rebalance -= 1