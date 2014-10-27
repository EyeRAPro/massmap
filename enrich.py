import os
import gzip
import xml.etree.ElementTree as ET
import argparse

parser = argparse.ArgumentParser(description='Parses masscan output puts it in a database and enriches it with other data.')
parser.add_argument('-path', default='data', 
                   help='directory to read data from')
args = parser.parse_args()
path = args.path
for filename in os.listdir(path):
	try:
		f = gzip.open(os.path.join(path,filename), 'rb')
		file_content = f.read()
	except IOError:
		f = open(os.path.join(path,filename), 'rb')
		file_content = f.read()
	f.close()
	root = ET.fromstring(file_content)
	for country in root.iter('host'):
		print country.get('addr')
		print country.get('port')