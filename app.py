import schedule
import time
from threading import Thread
from flask import Flask, render_template
from database import init_db, get_opportunities
from feed_parser import update_opportunities

app = Flask(__name__)

# Initialize database and start scheduler
def start_scheduler():
    init_db()
    schedule.every().day.at("00:00").do(update_opportunities)  # Update daily at midnight
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

# Run scheduler in a separate thread
scheduler_thread = Thread(target=start_scheduler, daemon=True)
scheduler_thread.start()

@app.route('/')
def index():
    opportunities = get_opportunities()
    # Sort by fully_funded (descending) and then date
    opportunities.sort(key=lambda x: (-x['fully_funded'], x['date']))
    return render_template('index.html', opportunities=opportunities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)