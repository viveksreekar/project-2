# app.py
from flask import Flask, request, render_template, jsonify, url_for
from tasks import send_email, generate_report
from celery.result import AsyncResult

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main page to submit tasks.
    Handles both displaying the form and processing form submissions.
    """
    if request.method == 'POST':
        task_type = request.form.get('task_type')
        task = None
        if task_type == 'email':
            recipient = request.form.get('recipient')
            message = request.form.get('message')
            # Send the task to the message queue
            task = send_email.delay(recipient, message)
        elif task_type == 'report':
            user_id = request.form.get('user_id')
            report_type = request.form.get('report_type')
            # Send the task to the message queue
            task = generate_report.delay(user_id, report_type)
        
        if task:
            # Return the task ID to the client so it can check the status
            return jsonify({"taskId": task.id}), 202
            
    return render_template('index.html')

@app.route('/task_status/<task_id>')
def task_status(task_id):
    """
    Endpoint for the client to poll for task status.
    """
    task = AsyncResult(task_id)
    
    response_data = {
        'state': task.state,
        'result': task.result if task.state == 'SUCCESS' else str(task.info)
    }
    return jsonify(response_data)


# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
