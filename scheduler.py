
from threading import Timer
from flask import jsonify
import logging
from datetime import datetime, timedelta
from flask_socketio import SocketIO

logging.basicConfig(level=logging.DEBUG)
scheduled_tasks = []

# This should be set from your main Flask app
socketio = None

def set_socketio(socket):
    global socketio
    socketio = socket

def schedule_task(script_name, start_date, start_time, run_script):
    try:
        run_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        delay = (run_datetime - datetime.now()).total_seconds()

        if delay < 0:
            logging.error(f"Scheduled time {start_date} {start_time} is in the past.")
            return jsonify({'status': f'Error: Scheduled time {start_date} {start_time} is in the past'}), 400

        def scheduled_run():
            run_script(script_name)
            update_task_status(script_name, 'Completed')

        t = Timer(delay, scheduled_run)
        t.start()

        task = {
            'script_name': script_name,
            'run_date': start_date,
            'run_time': start_time,
            'thread': t,
            'status': 'Scheduled'
        }

        scheduled_tasks.append(task)
        logging.info(f'Script {script_name} scheduled for {start_date} at {start_time}.')
        emit_task_update()
        return task
    except Exception as e:
        logging.error(f"Error scheduling script {script_name}: {str(e)}")
        return None

def stop_scheduled_task(script_name=None):
    global scheduled_tasks
    logging.info(f"Attempting to stop tasks. Current tasks: {len(scheduled_tasks)}")
    tasks_to_remove = []
    if script_name:
        tasks_to_remove = [task for task in scheduled_tasks if task['script_name'] == script_name]
    else:
        tasks_to_remove = scheduled_tasks.copy()

    for task in tasks_to_remove:
        logging.info(f"Cancelling task: {task['script_name']}")
        task['thread'].cancel()
        scheduled_tasks.remove(task)

    if script_name:
        logging.info(f'Scheduled task for {script_name} cancelled.')
    else:
        logging.info('All scheduled tasks stopped.')
        scheduled_tasks = []

    # We don't need to emit here as it's now done in the route handler

def schedule_monthly_task(script_name, start_date, start_time, run_script):
    try:
        start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        current_datetime = start_datetime
        task = None

        def schedule_next_run():
            nonlocal current_datetime
            delay = (current_datetime - datetime.now()).total_seconds()

            if delay < 0:
                current_datetime = current_datetime.replace(day=1, month=current_datetime.month % 12 + 1, year=current_datetime.year + (current_datetime.month // 12))
                schedule_next_run()
                return

            t = Timer(delay, run_and_reschedule)
            t.start()

            task = {
                'script_name': script_name,
                'run_date': current_datetime.strftime("%Y-%m-%d"),
                'run_time': start_time,
                'thread': t,
                'status': 'Scheduled'
            }

            scheduled_tasks.append(task)
            logging.info(f'Script {script_name} scheduled for {current_datetime.strftime("%Y-%m-%d")} at {start_time}.')
            emit_task_update()

        def run_and_reschedule():
            run_script(script_name)
            update_task_status(script_name, 'Completed')
            nonlocal current_datetime
            current_datetime = current_datetime.replace(day=1, month=current_datetime.month % 12 + 1, year=current_datetime.year + (current_datetime.month // 12))
            schedule_next_run()

        schedule_next_run()
        return task
    except Exception as e:
        logging.error(f"Error scheduling script {script_name}: {str(e)}")
        return None

def get_scheduled_tasks():
    return [{
        'script_name': task['script_name'],
        'run_date': task['run_date'],
        'run_time': task['run_time'],
        'status': task['status']
    } for task in scheduled_tasks]

def update_task_status(script_name, status):
    for task in scheduled_tasks:
        if task['script_name'] == script_name:
            task['status'] = status
            break
    emit_task_update()

def emit_task_update():
    if socketio:
        tasks = get_scheduled_tasks()
        socketio.emit('tasks_updated', {'tasks': tasks})
        socketio.emit('request_state_update')