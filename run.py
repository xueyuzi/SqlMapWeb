import flask
import sqlite3
import requests
from sqlmap_api_test import AutoSqli
from flask import request, jsonify, redirect, render_template
from flask import abort


app = flask.Flask(__name__)
DATABASE = './database.db'
SQLMAPServer = 'http://192.168.1.82:8775'

@app.route('/')
def index():
	return redirect("/create")

@app.route('/create')
def main():
	return render_template('index.html')

@app.route('/task/create', methods=['POST'])
def create():
	target = str(request.form.get('target')).strip(r"'")
	cookie = str(request.form.get('cookie')).strip(r"'")
	if len(target) == 0:
		return abort(404)
	task = AutoSqli(SQLMAPServer, target, cookie=cookie)
	task.task_new()
	task.option_set()
	task.scan_start()

	conn = sqlite3.connect(DATABASE)
	cur = conn.cursor()
	cur.execute("insert into asset(task_id, target) values('%s', '%s')"
			%(task.taskid, target))
	conn.commit()
	conn.close()
	return redirect('/list')

@app.route('/list')
def list():
	tasks=[]
	conn = sqlite3.connect(DATABASE)
	cur = conn.cursor()
	cur.execute("select task_id, target from asset order by create_time desc")
	for row in cur:
		task={}
		task["task_id"] = row[0]
		task["target"] = row[1]
		tasks.append(task)
	conn.close()
	return render_template('tasks.html', tasks=tasks)

@app.route('/task/report', methods=['POST'])
def status():
	taskid = str(request.form.get('taskid')).strip(r"'")
	conn = sqlite3.connect(DATABASE)
	cur = conn.cursor()
	cur.execute("select * from asset where task_id = '%s'" % (taskid))
	if len(cur.fetchall()) == 0:
		abort(404)
	task = AutoSqli(SQLMAPServer)
	# status = requests.get(SQLMAPServer + '/scan/' + taskid + '/status').json()
	task.taskid = taskid
	status = task.scan_status()
	conn = sqlite3.connect(DATABASE)
	cur = conn.cursor()
	cur.execute("update asset set status = '%s' where task_id = '%s'" % (status, taskid))
	conn.commit()
	conn.close()
	if status == "terminated":
		return jsonify(task.get_report())
	return render_template('info.html', status=status)
	# return jsonify(status)
		# return jsonify(status)
@app.route('/revoke/<taskid>')
def revoke(task_id):
	return task_id
if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
