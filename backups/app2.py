import signal
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import subprocess
import os
import logging
from scheduler import schedule_task, stop_scheduled_task, get_scheduled_tasks, schedule_monthly_task

app = Flask(__name__)

SCRIPTS_DIRECTORY = "/Users/g6-media/Webscrapping-Git/Webscrapping- Webpage/Scrapping Scripts"
stop_execution = False
script_status = {}
script_output = {}

logging.basicConfig(level=logging.DEBUG)


def stop_execution_handler(signum, frame):
    global stop_execution
    stop_execution = True


signal.signal(signal.SIGINT, stop_execution_handler)


def run_script(script_name):
    global stop_execution
    script_path = os.path.join(SCRIPTS_DIRECTORY, script_name)
    script_status[script_name] = 'Running'
    script_stopped = False
    try:
        logging.debug(f"Starting script: {script_name}")
        process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)

        while True:
            if stop_execution:
                logging.debug(f"Stopping script: {script_name}")
                script_status[script_name] = 'Stopping'
                process.terminate()
                script_stopped = True
                break
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                logging.debug(f'Script {script_name} output: {output.strip()}')
                script_output[script_name] = script_output.get(script_name, '') + output

        stdout, stderr = process.communicate()
        script_output[script_name] = script_output.get(script_name, '') + stdout + stderr
        rc = process.poll()

        if not script_stopped:
            script_status[script_name] = 'Completed' if rc == 0 else f'Error: {stderr.strip()}'
        else:
            script_status[script_name] = 'Stopped'

    except Exception as e:
        logging.error(f"Exception running script {script_name}: {e}")
        script_status[script_name] = f'Error: {str(e)}'

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
        global stop_execution
        stop_execution = False
        scripts = request.form.getlist('scripts')
        if not scripts:
            return jsonify({'status': 'No scripts selected.'})
        for script in scripts:
            threading.Thread(target=run_script, args=(script,)).start()
        return jsonify({'status': 'Scripts running...'})
    except Exception as e:
        logging.error(f"Error running scripts: {str(e)}")
        return jsonify({'status': f'Error running scripts: {str(e)}'}), 500


@app.route('/stop_scripts', methods=['POST'])
def stop_scripts():
    try:
        global stop_execution
        stop_execution = True
        return jsonify({'status': 'Stopping scripts...'})
    except Exception as e:
        logging.error(f"Error stopping scripts: {str(e)}")
        return jsonify({'status': f'Error stopping scripts: {str(e)}'}), 500


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

        unique_scripts = list(set(scripts))  # Remove duplicates
        scheduled_scripts = []

        for script in unique_scripts:
            if recurrence_type == 'monthly':
                schedule_monthly_task(script, start_date, start_time, run_script)
            else:
                schedule_task(script, start_date, start_time, run_script)
            scheduled_scripts.append(script)

        if recurrence_type == 'monthly':
            status = f'Scheduled {scheduled_scripts} monthly from {start_date} at {start_time}'
        else:
            status = f'Scheduled {scheduled_scripts} for {start_date} at {start_time}'

        return jsonify({'status': status})
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
        response = stop_scheduled_task()
        return response
    except Exception as e:
        logging.error(f"Error stopping scheduled tasks: {str(e)}")
        return jsonify({'status': f'Error stopping scheduled tasks: {str(e)}'}), 500


@app.route('/get_scheduled_tasks', methods=['GET'])
def get_scheduled_tasks_route():
    try:
        tasks = get_scheduled_tasks()
        return jsonify(tasks)
    except Exception as e:
        logging.error(f"Error getting scheduled tasks: {str(e)}")
        return jsonify({'status': f'Error getting scheduled tasks: {str(e)}'}), 500


@app.route('/styles.css')
def styles():
    return send_from_directory('static', 'styles.css')


if __name__ == '__main__':
    app.run(debug=True)
