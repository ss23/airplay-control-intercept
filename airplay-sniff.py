#!/usr/bin/env python2
from scapy.all import *

def airplay_callback(pkt):
	try:
		if pkt['Raw'].load[0:5] == 'SETUP':
			# Someone is starting to play! Add them to the list yo
			with open('/tmp/playing.txt', 'w') as f:
				f.write(pkt[IP].src)
			print "Updated playing.txt to " + pkt[IP].src
		elif pkt['Raw'].load[0:5] == 'TEARD':
			# Someone is getting *off* those speakers, yo
			with open('/tmp/playing.txt', 'w') as f:
				pass # Rewrite it with nothing
			print "Updated playing.txt to be blank"
	except:
		pass # meh
sniff(filter="tcp and port 5000", store=0, prn=airplay_callback);
