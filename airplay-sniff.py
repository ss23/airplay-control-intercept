#!/usr/bin/env python2
from scapy.all import *

cur_ip = False

def airplay_callback(pkt):
	try:
		if pkt[IP].sprintf('%proto%') == 'tcp':
			# This could be anything! Parse further
			if pkt['Raw'].load[0:5] == 'TEARD':
				# Anyone can teardown, only remove the IP if it's the currently playing person
				global cur_ip
				if cur_ip == pkt[IP].src:
					# Someone is getting *off* those speakers, yo
					with open('/tmp/playing.txt', 'w') as f:
						pass # Rewrite it with nothing
					print "Updated playing.txt to be blank"
		else:
			# Should be UDP
			if cur_ip != pkt[IP].src:
				# A new person!
				with open('/tmp/playing.txt', 'w') as f:
					f.write(pkt[IP].src)
				cur_ip = pkt[IP].src
				print "Updated playing.txt to " + pkt[IP].src
	except:
		pass # meh
sniff(filter="port 5000 or port 6001", store=0, prn=airplay_callback);
