import os
import gzip
import xml.etree.ElementTree as ET
import argparse
import yaml
import psycopg2
import geoip2.database

parser = argparse.ArgumentParser(description='Parses masscan output puts it in a database and enriches it with other data.')
parser.add_argument('-path', default='data', 
                   help='directory to read data from')
args = parser.parse_args()
path = args.path

config = yaml.load(file("config.yaml"))
reader = geoip2.database.Reader('data/GeoLite2-City.mmdb')
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
		details = host.getchildren()
		print details[0].items()[1][1]
		print details[1].getchildren()[0].items()[1][1]
		response = reader.city(details[0].items()[1][1])
		print response.city.name