from flask import Flask
import psycopg2
import json
from flask import request

app = Flask(__name__)
conn = psycopg2.connect("dbname=massmap user=sam")
cur = conn.cursor()

@app.route("/")
def hello():
	cur.execute("select * from host;")
	return json.dumps(cur.fetchall())

@app.route("/ports")
def port_list():
	cur.execute("select DISTINCT port from port;")
	return json.dumps(cur.fetchall())

@app.route("/scans")
def scan_for_ports():
	ports = map(int,request.args.getlist('ports'))
	cur.execute("SELECT id from port where port = any (%s)",(ports,))
	return json.dumps(cur.fetchall())
if __name__ == "__main__":
    app.run(debug=True)