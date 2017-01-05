#!/usr/bin/env python

import cgi
import cgitb
#cgitb.enable()

import socket


HOST = '129.74.152.233'
PORT = 8081

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#s.send('172.30.100.41 /nphControlCamera?Direction=PanScan')
s.send('172.30.100.41 /SnapshotJPEG?Resolution=192x144')
#s.send('172.30.100.41 /nphMotionJpeg?Resolution=192x144')




#get initial string
data = s.recv(2048)

if '200 OK' in data:
	#pull content-type out, buffer the rest
	while 'Content-type' not in data:
		#clear first time here
		if '200 OK' in data:
			data = s.recv(2048)
		else:
			data = data + s.recv(2048)
	#print content-type
	for line in data.split('\n'):
		if 'Content-type' in line:
			print line
	#print rest
	for line in data.split('\n'):
		if 'Content-type' not in line:
			print line
	print
	while data:
		data = None
		data = s.recv(2048)
		print data,
"""
if '200 OK' in data:
	while data:
		data = None
		data = s.recv(2048).replace('\n\n\n','')
		print data
"""

"""
data = s.recv(2048)
while data:
	data = None
	data = s.recv(2048)
	print data.rstrip('\n')
"""
#print 'done'

s.close()
