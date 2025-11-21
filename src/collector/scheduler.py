from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from collector.nasdaq_scraper import fetch_and_store_data

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store_data, 'interval', hours=1)
    scheduler.start()
    print(f"Scheduler started at {datetime.now()}")

if __name__ == "__main__":
    start_scheduler()