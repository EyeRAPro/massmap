from flask import Flask
import psycopg2
import json
from flask import request

app = Flask(__name__)
conn = psycopg2.connect("dbname=massmap user=sam")
cur = conn.cursor()

@app.route("/")
def index():
	return app.send_static_file('index.html')

@app.route("/ports")
def port_list():
	cur.execute("select DISTINCT port from port;")
	return json.dumps(cur.fetchall())

@app.route("/scans")
def scan_for_ports():
	ports = map(int,request.args.getlist('ports'))
	cur.execute("""SELECT host.ip_address, port.port, host.latitude, host.longitude, host.city, host.country from port 
		left join scan_port on scan_port.port_id = port.id 
		join scan on scan.id = scan_port.scan_id 
		join host_port on port.id = host_port.port_id
		join host on host_port.host_id = host.id 
		where port.port = any (%s)""",(ports,))
	return json.dumps(cur.fetchall())
if __name__ == "__main__":
    app.run(debug=True)