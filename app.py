import schedule
import time
from threading import Thread
from flask import Flask, render_template
from database import init_db, get_opportunities
from feed_parser import update_opportunities
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

def start_scheduler():
    init_db()
    logger.info("Scheduler initialized")
    schedule.every().day.at("10:15").do(update_opportunities)
    while True:
        schedule.run_pending()
        logger.info("Scheduler checked for pending tasks")
        time.sleep(60)

scheduler_thread = Thread(target=start_scheduler, daemon=True)
scheduler_thread.start()

@app.route('/')
def index():
    opportunities = get_opportunities()
    opportunities.sort(key=lambda x: (-x['fully_funded'], x['date']))
    logger.info(f"Retrieved {len(opportunities)} opportunities")
    return render_template('index.html', opportunities=opportunities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)