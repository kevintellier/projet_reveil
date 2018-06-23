from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

@app.route("/")	
def index():
	return render_template('index.html')

@app.route("/validate", methods=['POST'])
def change_alarm():
	time = request.form["time"]
	print(time, file=sys.stderr)
	return render_template('settings.html')

if __name__ == '__main__':
	app.run(debug=True)