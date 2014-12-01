CREATE SEQUENCE host_id_seq;
CREATE SEQUENCE port_id_seq;

CREATE TABLE host (
	id INT4 DEFAULT nextval('host_id_seq') PRIMARY KEY,
	ip_address INET
);

CREATE TABLE port (
	id INT4 DEFAULT nextval('port_id_seq') PRIMARY KEY,
	port INT
);

CREATE TABLE host_port (
	host_id INT4 DEFAULT nextval('host_id_seq'),
	port_id INT4 DEFAULT nextval('port_id_seq')
);