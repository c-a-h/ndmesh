#!/usr/bin/env python

"""
-for playing with generating map
-prints straight html/javascript

-currently prints very little info about gatewayss
"""

import sys
import MySQLdb


class Router:
	def __init__(self,num,name,type,lat,long,ip,has_cam=0,pref_gw=None):
		self.number = num
		self.name = name
		self.type = type
		self.latitude = lat
		self.longitude = long
		self.ip_addr = ip
		self.has_camera = has_cam
		self.gw_ip = pref_gw




db = MySQLdb.connect(user="webuser",passwd="webpassword",db="meshcam",host="snoopy.cse.nd.edu")
c = db.cursor()


num_routers = c.execute("SELECT Router_num,Name,Type,latitude,longitude,a_rad_addr,has_camera,pref_gw FROM ROUTER_INFO")

routers = {}
#routers = []
for i in range(num_routers):
	data = c.fetchone()
	#print data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]
	routers[data[0]] = Router(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
	#routers.append(Router(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]))



num_connections = c.execute('SELECT source,destination,strength FROM CONNECTIONS')
conns = {}
for i in range(num_connections):
	(src,dest,str) = c.fetchone()
	#add
	if src not in conns:
		conns[src] = {dest:str}
	else:
		conns[src][dest] = str
	#make match
	#if dest in conns:
	#	if src in conns[dest]:
			#use < for optimistic
			#or > for pessimistic
	#		if str < conns[dest][src]:
	#			conns[dest][src] = str
	#		else:
	#			conns[src][dest] = conns[dest][src]


print 'Content-type: text/html\n\n'

print """
<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript">
  function initialize() {
"""
for r in routers:
	print '    var router%d = new google.maps.LatLng(%f,%f);' % (routers[r].number,routers[r].latitude,routers[r].longitude)
#can do average center if desired: add lat and long in the above loop, then divide by number of routers
#or, find outer hull and the center of that!
#or, just screw it and hard-code a value
print """
    var centerpoint = new google.maps.LatLng(41.700475,-86.234019);
    var myOptions = {
      zoom: 16,
      center: centerpoint,
      mapTypeId: google.maps.MapTypeId.HYBRID,
      mapTypeControlOptions: {
        mapTypeIds: [google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.SATELLITE, google.maps.MapTypeId.HYBRID]
      }
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
"""
for r in routers:
	#infowindow
	print '    var infowindow%d = new google.maps.InfoWindow({' % routers[r].number
	print "      content: '<b>%s</b><br/>Type: %s'" % (routers[r].name,routers[r].type)
	if routers[r].has_camera:
		print '      + \'<br/><a href="/ndMeshScripts/genCamControl.cgi?gwaddress=%s&ngwaddress=%s&page=9&camname=%s" target="_top"><img width=192 height=144 alt="no image available" src=/cgi-bin/ndMeshScripts/snapshot.cgi?resolution=1&gwaddress=%s&ngwaddress=%s></a>\'' % (routers[r].gw_ip,routers[r].ip_addr,routers[r].name,routers[r].gw_ip,routers[r].ip_addr)
	print "      + '<br/>'"
	print '    });'
	#marker
	print '    var marker%d = new google.maps.Marker({' % routers[r].number
	print '      position: router%d,' % routers[r].number
	print '      map: map,'
	print '      title: "%s",' % routers[r].name
	if routers[r].type == 'NGW':
		print "      icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=N|FF3333|000000'"
		#print "      icon: '/ndmesh/images/camera_icon.png'"
	else:
		print "      icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=G|33FFFF|000000'"
		#print "      icon: '/ndmesh/images/gw_icon.png'"
	print '    });'
	#listener
	print '    google.maps.event.addListener(marker%d,\'click\',function() {' % routers[r].number
	print '      infowindow%d.open(map,marker%d)' % (routers[r].number,routers[r].number)
	print '    });'
#do connections here
for src in conns:
	for dest in conns[src]:
		print '    var link%dto%d = [router%d, router%d];' % (src,dest,src,dest)
		print '    var path%dto%d = new google.maps.Polyline( {' % (src,dest)
		print '      path: link%dto%d,' % (src,dest)
		if conns[src][dest] < 65:
			print '      strokeColor: "#00FF00",'
		elif conns[src][dest] < 75:
			print '      strokeColor: "#FFFF00",'
		else:
			print '      strokeColor: "#FF0000",'
		print '      strokeOpacity: 0.5,'
		print '      strokeWeight: 4'
		print '    });'
		print '    path%dto%d.setMap(map);' % (src,dest)

print """
  }
</script>

<style type="text/css">
  h3 {color:#FDD017}
</style>

</head>
<body onload="initialize()" >
  <div id="map_canvas" style="width: 470px; height: 710px" align=center></div>
</body>
</html>
"""
