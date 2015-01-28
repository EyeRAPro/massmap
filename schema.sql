CREATE SEQUENCE host_id_seq;
CREATE SEQUENCE port_id_seq;
CREATE SEQUENCE scan_id_seq;

CREATE TABLE host (
	id INT4 DEFAULT nextval('host_id_seq') PRIMARY KEY,
	ip_address INET,
	latitude REAL,
	longitude REAL,
	city VARCHAR(50),
	country VARCHAR(20)
);

CREATE TABLE port (
	id INT4 DEFAULT nextval('port_id_seq') PRIMARY KEY,
	port INT
);

CREATE TABLE scan (
	id INT4 DEFAULT nextval('host_id_seq') PRIMARY KEY,
	time TIMESTAMP NOT NULL
);

CREATE TABLE host_port (
	host_id INT4 DEFAULT nextval('host_id_seq'),
	port_id INT4 DEFAULT nextval('port_id_seq')
);

CREATE TABLE scan_port (
	scan_id INT4 DEFAULT nextval('scan_id_seq'),
	port_id INT4 DEFAULT nextval('port_id_seq')
);