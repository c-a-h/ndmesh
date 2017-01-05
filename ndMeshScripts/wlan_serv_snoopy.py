#!/usr/bin/env python

import sys
import socket
import MySQLdb

"""
routers = {}
routers['00:15:6D:64:96:57'] = ('Niemier','172.30.100.1')
routers['06:15:6D:64:9A:11'] = ('Stadium','172.30.100.2')
routers['00:15:6D:64:99:8E'] = ('Legends','172.30.100.3')
routers['00:15:6D:64:86:CC'] = ('DBRT','172.30.100.4')
routers['00:15:6D:64:86:F6'] = ('Stinson-Remick','172.30.100.5')
#routers[''] = ('NOT IN SERVICE','172.30.100.6')
routers['00:15:6D:64:86:AA'] = ('Fitz Roof','172.30.100.7')
routers['00:15:6D:64:9A:03'] = ('DPAC','172.30.100.8')
routers['00:15:6D:64:86:E6'] = ('OShag','172.30.100.9')
routers['06:15:6D:64:87:03'] = ('Hayes-Healey','172.30.100.10')
#routers[''] = ('NOT IN SERVICE','172.30.100.11')
routers['00:15:6D:64:86:85'] = ('Curt','172.30.100.12')
routers['00:15:6D:64:86:F0'] = ('Stepan','172.30.100.13')
routers['00:15:6D:64:18:35'] = ('Jordan','172.30.100.14')
routers['00:15:6D:64:86:DE'] = ('Hesburgh','172.30.100.15')
routers['00:15:6D:64:9A:00'] = ('Flanner','172.30.100.16')
"""



def handle_connection(conn):
	"""
	Given a connection object,
	returns a list of tuples of MAC address and strength (as a positive integer)
	"""
	try:
		try:
			msg = ''
			tmp = conn.recv(1024)
			while tmp:
				msg = msg + tmp
				tmp = conn.recv(1024)
		except KeyboardInterrupt:
			pass
	finally:
		conn.close()
	ret = []
	for line in msg.split('\n')[1:]:
		line = line.split()
		if len(line) > 5:
			str = -1 * int(line[5])
			ret.append((line[0].upper(),str))
	return ret



def update_database(source,links):
	db = MySQLdb.connect(user="webadmin",passwd="308WIN",db="meshcam",host="snoopy.cse.nd.edu")
	c = db.cursor()
	#find routernum of first
	count = c.execute("SELECT Router_num FROM ROUTER_INFO WHERE a_rad_addr=%s",(source),)
	if count != 1:
		#not found, or too many found; abort
		print "didn't find",source,"in database. aborting."
		c.close()
		db.close()
		return
	source_num = c.fetchone()[0]
	#clear old entries
	count = c.execute("DELETE FROM CONNECTIONS WHERE source=%s",(source_num,))
	for link in links:
		#find routernum of second
		count = c.execute("SELECT Router_num FROM ROUTER_INFO WHERE a_mac_addr=%s",(link[0],))
		if count != 1:
			#not found, or too many found; abort
			print "didn't find",link[0],"in database. skipping."
			continue
		dest_num = c.fetchone()[0]
		#update connection table
		count = c.execute("INSERT INTO CONNECTIONS (source,destination,strength) VALUES (%s,%s,%s)",(source_num,dest_num,link[1]))
	c.close()
	db.close()
	



if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'please provide a port number'
		sys.exit()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('',int(sys.argv[1])))
	s.listen(1)
	links = {}
	while True:
		print 'waiting...'
		conn,addr = s.accept()
		links[addr[0]] = handle_connection(conn)
		#print links
		"""
		for ip in links:
			from_name = 'UNKNOWN'
			for tmp in routers.keys():
				if ip == routers[tmp][1]:
					from_name = routers[tmp][0]
			for mac,str in links[ip]:
				if mac in routers:
					print from_name,'sees',routers[mac][0],'with strength',str
				else:
					print from_name,'sees UNKNOWN with strength',str
		print
		"""
		if len(links[addr[0]]) > 0:
			print "updating tables"
			update_database(addr[0],links[addr[0]])
