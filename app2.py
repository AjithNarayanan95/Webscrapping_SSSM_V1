import signal
import eventlet
eventlet.monkey_patch()
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import subprocess
import os
import logging
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from scheduler import schedule_task, stop_scheduled_task, get_scheduled_tasks, schedule_monthly_task, scheduled_tasks
from datetime import datetime, timedelta
import uuid



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scheduled_tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)
db = SQLAlchemy(app)

# Global state object
global_state = {
    'run_button_disabled': False,
    'stop_button_disabled': True,
    'schedule_button_disabled': False,
    'stop_schedule_button_disabled': True,
    'scripts_running': False,
    'scheduled_tasks': []
}

state_lock = threading.Lock()

SCRIPTS_DIRECTORY = "/Users/g6-media/Webscrapping-Git/Webscrapping- Webpage/Scrapping Scripts"
stop_execution = False
script_status = {}
script_output = {}

logging.basicConfig(level=logging.DEBUG)

class ScheduledTask(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    script_name = db.Column(db.String(100), nullable=False)
    run_date = db.Column(db.Date, nullable=False)
    run_time = db.Column(db.Time, nullable=False)
    recurrence_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Scheduled')

    def to_dict(self):
        return {
            'id': self.id,
            'script_name': self.script_name,
            'run_date': self.run_date.strftime('%Y-%m-%d'),
            'run_time': self.run_time.strftime('%H:%M'),
            'recurrence_type': self.recurrence_type,
            'status': self.status
        }


# WebSocket changes
@socketio.on('connect')
def handle_connect():
    emit('state_update', global_state)


@socketio.on('run_scripts')
def handle_run_scripts(data):
    scripts = data['scripts']
    if not scripts:
        emit('error', {'message': 'No scripts selected.'})
        return

    with state_lock:
        global_state['run_button_disabled'] = True
        global_state['stop_button_disabled'] = False
        global_state['schedule_button_disabled'] = True
        global_state['stop_schedule_button_disabled'] = True
        global_state['scripts_running'] = True

    global stop_execution
    stop_execution = False

    for script in scripts:
        threading.Thread(target=run_script, args=(script,)).start()
        update_task_status(script, 'Running')

    emit('state_update', global_state, broadcast=True)


@socketio.on('stop_scripts')
def handle_stop_scripts():
    global stop_execution, script_status
    stop_execution = True
    for script_name, status in script_status.items():
        if status == 'Running':
            script_status[script_name] = 'Stopping'

    with state_lock:
        global_state['run_button_disabled'] = False
        global_state['stop_button_disabled'] = True
        global_state['schedule_button_disabled'] = False
        global_state['scripts_running'] = False

    emit('state_update', global_state, broadcast=True)


@socketio.on('schedule_scripts')
def handle_schedule_scripts(data):
    global stop_execution
    stop_execution = False
    scripts = data['scripts']
    start_date = data['start_date']
    start_time = data['start_time']
    recurrence_type = data['recurrence_type']

    unique_scripts = list(set(scripts))
    scheduled_scripts = []

    for script in unique_scripts:
        if recurrence_type == 'monthly':
            schedule_monthly_task(script, start_date, start_time, run_script)
        else:
            schedule_task(script, start_date, start_time, run_script)
        scheduled_scripts.append(script)

    update_and_emit_global_state({
        'run_button_disabled': True,
        'stop_button_disabled': True,
        'schedule_button_disabled': True,
        'stop_schedule_button_disabled': False
    })

    if recurrence_type == 'monthly':
        status = f'Scheduled {scheduled_scripts} monthly from {start_date} at {start_time}'
    else:
        status = f'Scheduled {scheduled_scripts} for {start_date} at {start_time}'

    tasks = get_scheduled_tasks()
    emit('schedule_update', {'status': status, 'tasks': tasks}, broadcast=True)
    emit('state_update', global_state, broadcast=True)


@socketio.on('stop_all')
def handle_stop_all():
    global stop_execution, script_status, scheduled_tasks
    stop_execution = True
    for script_name in script_status:
        script_status[script_name] = 'Stopped'

    stop_scheduled_task()
    scheduled_tasks.clear()

    with state_lock:
        global_state['run_button_disabled'] = False
        global_state['stop_button_disabled'] = True
        global_state['schedule_button_disabled'] = False
        global_state['stop_schedule_button_disabled'] = True
        global_state['scripts_running'] = False
        global_state['scheduled_tasks'] = []

    emit('state_update', global_state, broadcast=True)
    emit('all_stopped', {'status': 'All scheduled tasks and running scripts have been stopped.'}, broadcast=True)
# WebSocket changes
def stop_execution_handler(signum, frame):
    global stop_execution
    stop_execution = True


signal.signal(signal.SIGINT, stop_execution_handler)


def run_script(script_name):
    global stop_execution, script_status, script_output
    script_path = os.path.join(SCRIPTS_DIRECTORY, script_name)
    script_status[script_name] = 'Running'
    url_count = 0
    try:
        logging.debug(f"Starting script: {script_name}")
        process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)

        while True:
            if stop_execution or script_status[script_name] == 'Stopping':
                logging.debug(f"Stopping script: {script_name}")
                process.terminate()
                process.wait(timeout=5)
                if process.poll() is None:
                    process.kill()
                script_status[script_name] = f'Stopped (URLs scraped: {url_count})'
                socketio.emit('script_update', {'script_name': script_name, 'status': script_status[script_name]})
                break
            try:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    logging.debug(f'Script {script_name} output: {output.strip()}')
                    script_output[script_name] = script_output.get(script_name, '') + output
                    if output.strip().startswith('https://'):  # Count URLs
                        url_count += 1
                        script_status[script_name] = f'Running (URLs scraped: {url_count})'
                        socketio.emit('script_update',
                                      {'script_name': script_name, 'status': script_status[script_name]})
            except subprocess.TimeoutExpired:
                continue

        stdout, stderr = process.communicate()
        script_output[script_name] = script_output.get(script_name, '') + stdout + stderr
        rc = process.poll()

        if script_status[script_name] != f'Stopped (URLs scraped: {url_count})':
            script_status[script_name] = f'Completed (URLs scraped: {url_count})' if rc == 0 else f'Error: {stderr.strip()}'
        socketio.emit('script_update', {'script_name': script_name, 'status': script_status[script_name]})

    except Exception as e:
        logging.error(f"Exception running script {script_name}: {e}")
        script_status[script_name] = f'Error: {str(e)}'
        socketio.emit('script_update', {'script_name': script_name, 'status': script_status[script_name]})

    finally:
        if script_name in script_status and 'Running' in script_status[script_name]:
            script_status[script_name] = f'Completed (URLs scraped: {url_count})'

UNWANTED_SCRIPTS = ['module_package.py']
@app.route('/')

def index():
    try:
        scripts = [f for f in os.listdir(SCRIPTS_DIRECTORY) if f.endswith('.py') and f not in UNWANTED_SCRIPTS]
        return render_template('index.html', scripts=scripts)
    except Exception as e:
        logging.error(f"Error loading scripts: {str(e)}")
        return jsonify({'status': f'Error loading scripts: {str(e)}'}), 500


@app.route('/run_scripts', methods=['POST'])
def run_scripts():
    try:
        global global_state, stop_execution  # Add stop_execution to the global declaration
        print("Run scripts route called")
        with state_lock:
            global_state['run_button_disabled'] = True
            global_state['stop_button_disabled'] = False
            global_state['schedule_button_disabled'] = True
            global_state['stop_schedule_button_disabled'] = True
            global_state['scripts_running'] = True

        stop_execution = False  # Reset the stop_execution flag

        scripts = request.form.getlist('scripts')
        if not scripts:
            return jsonify({'status': 'No scripts selected.', **global_state})

        for script in scripts:
            threading.Thread(target=run_script, args=(script,)).start()
            update_task_status(script, 'Running')

        return jsonify({'status': 'Scripts running...', **global_state})
    except Exception as e:
        logging.error(f"Error running scripts: {str(e)}")
        return jsonify({'status': f'Error running scripts: {str(e)}', **global_state}), 500

def update_task_status(script_name, status):
    for task in scheduled_tasks:
        if task['script_name'] == script_name:
            task['status'] = status
            break

@app.route('/update_state', methods=['POST'])
def update_state():
    global global_state
    try:
        new_state = request.json
        if new_state is None:
            raise ValueError("No JSON data received")
        app.logger.info(f"Received state update: {new_state}")
        with state_lock:
            global_state.update(new_state)
        app.logger.info(f"Updated global state: {global_state}")
        return jsonify(global_state)
    except Exception as e:
        app.logger.error(f"Error updating state: {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.route('/stop_scripts', methods=['POST'])
def stop_scripts():
    try:
        global global_state
        with state_lock:
            global_state['run_button_disabled'] = False
            global_state['stop_button_disabled'] = True
            global_state['schedule_button_disabled'] = False
            global_state['scripts_running'] = False

        global stop_execution, script_status
        stop_execution = True
        for script_name, status in script_status.items():
            if status == 'Running':
                script_status[script_name] = 'Stopping'
        socketio.emit('state_update', global_state)
        return jsonify({'status': 'Stopping all running scripts...'})
    except Exception as e:
        logging.error(f"Error stopping scripts: {str(e)}")
        return jsonify({'status': f'Error stopping scripts: {str(e)}'}), 500

@socketio.on('stop_scripts')
def handle_stop_scripts():
    global stop_execution, script_status
    stop_execution = True
    for script_name, status in script_status.items():
        if status == 'Running':
            script_status[script_name] = 'Stopping'

    with state_lock:
        global_state['run_button_disabled'] = False
        global_state['stop_button_disabled'] = True
        global_state['schedule_button_disabled'] = False
        global_state['scripts_running'] = False

    emit('state_update', global_state, broadcast=True)

@app.route('/status', methods=['GET'])
def status():
    try:
        return jsonify(script_status)
    except Exception as e:
        logging.error(f"Error getting status: {str(e)}")
        return jsonify({'status': f'Error getting status: {str(e)}'}), 500


@app.route('/schedule_scripts', methods=['POST'])
def schedule_scripts():
    try:
        scripts = request.form.getlist('scripts')
        start_date = request.form.get('start-date')
        start_time = request.form.get('start-time')
        recurrence_type = request.form.get('recurrence-type')

        run_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        run_time = datetime.strptime(start_time, '%H:%M').time()

        scheduled_scripts = []
        for script in scripts:
            new_task = ScheduledTask(
                id=str(uuid.uuid4()),
                script_name=script,
                run_date=run_date,
                run_time=run_time,
                recurrence_type=recurrence_type,
                status='Scheduled'
            )
            db.session.add(new_task)
            scheduled_scripts.append(script)

            # Schedule the task
            if recurrence_type == 'monthly':
                task = schedule_monthly_task(script, start_date, start_time, run_script)
            else:
                task = schedule_task(script, start_date, start_time, run_script)

            if task is None:
                return jsonify({'status': f'Error scheduling script: {script}'}), 500

        db.session.commit()

        status = f'Scheduled {scheduled_scripts} for {start_date} at {start_time}'
        if recurrence_type == 'monthly':
            status = f'Scheduled {scheduled_scripts} monthly from {start_date} at {start_time}'

        tasks = ScheduledTask.query.all()
        # Emit WebSocket event to all clients immediately
        # socketio.emit('tasks_updated', {'tasks': [task.to_dict() for task in tasks]}, broadcast=True)
        socketio.emit('tasks_updated', {'tasks': [task.to_dict() for task in tasks]})
        return jsonify({
            'status': f'Scheduled {scripts} for {start_date} at {start_time}',
            'tasks': [task.to_dict() for task in tasks]
        })
    except Exception as e:
        logging.error(f"Error scheduling script: {str(e)}")
        return jsonify({'status': f'Error scheduling script: {str(e)}'}), 500

@app.route('/stop_scheduled_scripts', methods=['POST'])
# def stop_scheduled_scripts():
#     try:
#         script_name = request.form.get('script_name')
#         if not script_name:
#             return jsonify({'status': 'No script name provided.'}), 400
#         response = stop_scheduled_task(script_name)
#         return response
#     except Exception as e:
#         logging.error(f"Error stopping scheduled task: {str(e)}")
#         return jsonify({'status': f'Error stopping scheduled task: {str(e)}'}), 500

@app.route('/stop_scheduled_scripts', methods=['POST'])
def stop_scheduled_scripts():
    try:
        script_name = request.form.get('script_name')
        if script_name:
            # Delete the specific task from the database
            ScheduledTask.query.filter_by(script_name=script_name).delete()
        else:
            # Delete all tasks from the database
            ScheduledTask.query.delete()

        db.session.commit()

        # Clear in-memory tasks
        stop_scheduled_task(script_name)

        # Fetch updated tasks from the database
        updated_tasks = ScheduledTask.query.all()

        # Emit WebSocket event to all clients
        socketio.emit('tasks_updated', {'tasks': [task.to_dict() for task in updated_tasks]}, broadcast=True)


        return jsonify({'status': 'Scheduled tasks cleared successfully.'})
    except Exception as e:
        logging.error(f"Error stopping scheduled tasks: {str(e)}")
        db.session.rollback()
        return jsonify({'status': f'Error stopping scheduled tasks: {str(e)}'}), 500

@app.route('/reset_state', methods=['POST'])
def reset_state():
    global stop_execution, script_status, script_output
    stop_execution = False
    script_status = {}
    script_output = {}
    return jsonify({'status': 'State reset successfully'})

def update_and_emit_global_state(new_state=None):
    global global_state
    with state_lock:
        if new_state:
            app.logger.info(f"Updating global state with: {new_state}")
            global_state.update(new_state)
        app.logger.info(f"Emitting global state: {global_state}")
        socketio.emit('state_update', global_state, broadcast=True)

@socketio.on('request_state_update')
def handle_state_update_request():
    update_and_emit_global_state()



@app.route('/stop_all', methods=['POST'])
def stop_all():
    global stop_execution, script_status, scheduled_tasks
    try:
        global global_state
        update_and_emit_global_state({
            'run_button_disabled': False,
            'stop_button_disabled': True,
            'schedule_button_disabled': False,
            'stop_schedule_button_disabled': True,
            'scripts_running': False,
            'scheduled_tasks': []
        })

        emit('state_update', global_state, broadcast=True)

        # Stop all running scripts
        stop_execution = True
        for script_name in script_status:
            script_status[script_name] = 'Stopped'

        # Stop all scheduled tasks
        stop_scheduled_task()

        # Clear scheduled tasks
        scheduled_tasks.clear()

        return jsonify({'status': 'All scheduled tasks and running scripts have been stopped.'})
    except Exception as e:
        return jsonify({'status': f'Error stopping all tasks and scripts: {str(e)}'}), 500


@app.route('/get_state', methods=['GET'])
def get_state():
    global global_state
    with state_lock:
        return jsonify(global_state)

@app.route('/get_scheduling_status', methods=['GET'])
def get_scheduling_status():
    tasks = get_scheduled_tasks()
    any_scheduled = len(tasks) > 0
    any_running = any(task.get('status') == 'Running' for task in tasks)
    return jsonify({
        'status': 'Scheduled' if any_scheduled else 'Not Scheduled',
        'tasks': [{'script_name': task['script_name'], 'run_date': task['run_date'], 'run_time': task['run_time'],
                   'status': task.get('status', 'Scheduled')} for task in tasks],
        'any_scheduled': any_scheduled,
        'any_running': any_running
    })

@app.route('/check_running_scripts', methods=['GET'])
def check_running_scripts():
    any_running = any(status == 'Running' for status in script_status.values())
    return jsonify({'any_running': any_running})

@app.route('/get_scheduled_tasks', methods=['GET'])
def get_scheduled_tasks_route():
    try:
        tasks = ScheduledTask.query.all()
        return jsonify([task.to_dict() for task in tasks])
    except Exception as e:
        logging.error(f"Error getting scheduled tasks: {str(e)}")
        return jsonify({'status': f'Error getting scheduled tasks: {str(e)}'}), 500


@app.route('/styles.css')
def styles():
    return send_from_directory('static', 'styles.css')

@app.route('/settings')
def settings():
    return render_template('settings.html')


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

    socketio = SocketIO(app)
    socketio.run(app, host='192.168.0.161', port=5000, debug=True)

