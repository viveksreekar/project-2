# tasks.py
import time
from celery import Celery

# --- Celery Configuration ---
# The first argument to Celery is the name of the current module.
# The `broker` argument specifies the URL of our message broker (RabbitMQ).
# The `backend` argument specifies a result backend, used to store task results.
# 'redis://localhost:6379/0' is a common choice for a result backend.
# You'll need to run a Redis server for this: `docker run -d -p 6379:6379 redis`
celery_app = Celery(
    'tasks',
    broker='amqp://guest:guest@localhost:5672//',
    backend='rpc://' # Using RPC backend which sends results back as AMQP messages.
)

# --- Task Definitions ---

@celery_app.task
def send_email(recipient, message):
    """
    A mock task that simulates sending an email.
    In a real application, this would contain the logic to connect to an
    email server (e.g., using smtplib) and send the email.
    """
    print(f"Starting to send email to {recipient}...")
    # Simulate a network delay or a long-running process
    time.sleep(10) # Simulates a 10-second task
    print(f"Email successfully sent to {recipient} with message: '{message}'")
    return f"Email sent to {recipient} successfully."

@celery_app.task
def generate_report(user_id, report_type):
    """
    A mock task that simulates generating a complex report.
    """
    print(f"Starting report generation for user {user_id} (Type: {report_type})...")
    # Simulate heavy computation
    time.sleep(15) # Simulates a 15-second task
    print(f"Report for user {user_id} has been generated.")
    return f"Report for {user_id} is complete."

