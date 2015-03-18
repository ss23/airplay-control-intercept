#!/usr/bin/env python2
from scapy.all import *

cur_ip = False
def airplay_tcp(pkt):
	if pkt['Raw'].load[0:5] == 'SETUP':
		# Someone is starting to play! Add them to the list yo
		with open('/var/tmp/playing.txt', 'w') as f:
			f.write(pkt[IP].src)
		print "Updated playing.txt to " + pkt[IP].src
	elif pkt['Raw'].load[0:13] == 'SET_PARAMETER':
		#someone is changing state of player (volume, track, etc)
		with open('/var/tmp/playing.txt', 'w') as f:
			f.write(pkt[IP].src)
		print "Updated playing.txt to " + pkt[IP].src
	elif pkt['Raw'].load[0:5] == 'FLUSH':
		#someone is pausing playback
		with open('/var/tmp/playing.txt', 'w') as f:
			f.write(pkt[IP].src)
		print "Updated playing.txt to " + pkt[IP].src
	elif pkt['Raw'].load[0:5] == 'RECOR':
		#someone is starting playback
		with open('/var/tmp/playing.txt', 'w') as f:
			f.write(pkt[IP].src)
		print "Updated playing.txt to " + pkt[IP].src
	elif pkt['Raw'].load[0:5] == 'TEARD':
		# Someone is getting *off* those speakers, yo
		with open('/var/tmp/playing.txt', 'w') as f:
			pass # Rewrite it with nothing
		print "Updated playing.txt to be blank"

def airplay_callback(pkt):
	try:
		if pkt[IP].sprintf('%proto%') == 'tcp':
			#use TCP to id the ip
			airplay_tcp(pkt)
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
