import os
import gzip
import xml.etree.ElementTree as ET
import argparse
import yaml
import psycopg2
import geoip2.database
from datetime import datetime
import time
from ipwhois import IPWhois

parser = argparse.ArgumentParser(description='Parses masscan output puts it in a database and enriches it with other data.')
parser.add_argument('-path', default='data', 
                   help='directory to read data from')
args = parser.parse_args()
path = args.path

conn = psycopg2.connect("dbname=massmap user=sam")
cur = conn.cursor()
config = yaml.load(file("config.yaml"))
reader = geoip2.database.Reader('ref-data/GeoLite2-City.mmdb')
for filename in os.listdir(path):
	try:
		f = gzip.open(os.path.join(path,filename), 'rb')
		file_content = f.read()
	except IOError:
		f = open(os.path.join(path,filename), 'rb')
		file_content = f.read()
	f.close()
	root = ET.fromstring(file_content)
	for host in root.findall('host'):
		timestamp = time.strftime("%a, %d %b %Y %H:%M:%S +0000",
                    datetime.fromtimestamp(int(host.items()[0][1])).timetuple()
                    )
		details = host.getchildren()
		ip_address = details[0].items()[1][1]
		port = details[1].getchildren()[0].items()[1][1]
		response = reader.city(details[0].items()[1][1])
		country = response.country.name
		city = response.city.name
		latitude = response.location.latitude
		longitude = response.location.longitude
		cur.execute("INSERT INTO host (ip_address,latitude,longitude,city,country) VALUES (%s,%s,%s,%s,%s) RETURNING id;",(ip_address,latitude,longitude,city,country))
		host_id = cur.fetchone()[0]
		cur.execute("INSERT INTO port (port) VALUES (%s) RETURNING id;",(port,))
		port_id = cur.fetchone()[0]
		cur.execute("INSERT INTO host_port (host_id,port_id) VALUES (%s,%s)",(host_id,port_id))
		cur.execute("INSERT INTO scan (time) VALUES (%s) RETURNING id;",(timestamp,))
		scan_id = cur.fetchone()[0]
		cur.execute("INSERT INTO scan_port (scan_id, port_id) VALUES (%s,%s)",(scan_id,port_id))
conn.commit()
cur.close()
conn.close()