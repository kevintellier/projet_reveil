from flask import Flask, render_template, request, redirect, url_for, flash
import sys

app = Flask(__name__)

@app.route("/")	
def index():
	return render_template('index.html',wake_up_time="Pas de Réveil")

@app.route("/", methods=['POST'])
def change_alarm():
	time = request.form["time"]
	print(time, file=sys.stderr)
	return render_template('index.html', wake_up_time=time)

@app.route("/wakeup", methods=['POST'])
def alarm():
	main.py
	return render_template('index.html', wake_up_time=time)

if __name__ == '__main__':
	app.run(debug=True)