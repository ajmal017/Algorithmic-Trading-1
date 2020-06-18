from market_data_analysis import market_data_compiler
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    pmarket_data_compiler.get_stock_data()


if __name__ == '__main__':
	sched.start()