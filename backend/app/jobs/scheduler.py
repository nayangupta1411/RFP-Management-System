from apscheduler.schedulers.blocking  import BlockingScheduler
from database.connection import get_db
from ..jobs.vendor_response_job import process_vendor_responses_job

def start_scheduler(app):
    
    scheduler = BlockingScheduler()
    
    def job():
        with app.app_context():
            db = get_db()
            process_vendor_responses_job(db)
  
    scheduler.add_job(
        job,
        trigger="interval",
        minutes=5,
        id="vendor_response_job",
        replace_existing=True,
        max_instances=1
    )
    
    print("✔ Scheduler started successfully")
    print(type(scheduler))
    scheduler.start()