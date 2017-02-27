import optparse
import os
from socket import *
from threading import *

screenLock = Semaphore(value = 1)

def parseTarget(tgtHost):
	octets = tgtHost.split(".")
	firstOct = []
	secondOct = []
	thirdOct = []
	fourthOct = []
	if "-" in octets[0]:
		rnge = octets[0].split("-")
		firstOct = range(int(rnge[0]) , int(rnge[1]) + 1)
	else:
		firstOct.append(int(octets[0]))
		
	if "-" in octets[1]:
		rnge = octets[1].split("-")
		secondOct = range(int(rnge[0]) , int(rnge[1]) + 1)
	else:
		secondOct.append(int(octets[1]))
		
	if "-" in octets[2]:
		rnge = octets[2].split("-")
		thirdOct = range(int(rnge[0]) , int(rnge[1]) + 1)
	else:
		thirdOct.append(int(octets[2]))
		
	if "-" in octets[3]:
		rnge = octets[3].split("-")
		fourthOct = range(int(rnge[0]) , int(rnge[1]) + 1)
	else:
		fourthOct.append(int(octets[3]))
		
	#now put those ranges into every combination possible
	
	tgtHosts = []
	
	for i in firstOct:
		for j in secondOct:
			for k in thirdOct:
				for l in fourthOct:
					tgtHosts.append(str(i) + "." + str(j) + "." + str(k) + "." + str(l))
	return tgtHosts

def checkUp(tgtHosts, verb):
	goodHosts = []
	for host in tgtHosts:
		response = os.system("ping -n 1 -w 500 " + host + " > nul")
		if response == 0:
			goodHosts.append(host)
			print host + " is up"
		elif verb:
			print host + " is down"
	print "Discovered " + str(len(goodHosts)) + " Hosts up"
	return goodHosts
	
def connScan(tgtHost, tgtPort, verb):
	try:
		connSkt = socket(AF_INET, SOCK_STREAM)
		connSkt.connect((tgtHost, tgtPort))
		connSkt.send('Hello\r\n')
		
		results = connSkt.recv(100)
		screenLock.acquire()
		print "[+] " + str(tgtPort) + "/tcp open"
	except:
		if (verb):
			screenLock.acquire()
			print "[-] " + str(tgtPort) + "/tcp closed"
	finally:
		screenLock.release()
		connSkt.close()
		
def portScan(tgtHost, tgtPorts, verb):
	try:
		tgtIP = gethostbyname(tgtHost)
	except:
		print "[-] Cannot resolve " + tgtHost + ": unknown host"
		return
	
	try:
		tgtName = gethostbyaddr(tgtIP)
		print "\n[+] Scan results for: " + tgtName[0] + " (" + tgtIP + ")"
	except:
		print "\n[+] Scan results for: " + tgtIP
	
	setdefaulttimeout(1)
	i=0
	while (i in range(0, len(tgtPorts))):
		try:
			t = Thread(target = connScan, args  = (tgtHost, int(tgtPorts[i]), verb))
			t.start()
			i += 1
		except:
			pass
		
def Main():
	parser = optparse.OptionParser("Usage %prog -H <target host> -p <target port> -v/-q (verbose/quiet)")
	parser.add_option("-H", dest = "tgtHost", type = "string", help = "Specify target host")
	parser.add_option("-p", dest = "tgtPort", type = "string", help = "Specify target port")
	parser.add_option("-v", action="store_true", dest="verbose")
	parser.add_option("-q", action="store_false", dest="verbose")
	
	(options, args) = parser.parse_args()
	if (options.tgtHost == None):
		print parser.usage
		exit(0)

	else:
		tgtHosts = checkUp(parseTarget(options.tgtHost), options.verbose)
		
		if (options.tgtPort == None):
			ports = "0-65535"
		else:
			ports = str(options.tgtPort)
		if ('-' in ports):
			ranges = ports.split('-')
			intPorts = range(int(ranges[0]), int(ranges[1]) + 1)
			tgtPorts = map(str, intPorts)
		else:
			tgtPorts = ports.split(',')
		
	for tgtHost in tgtHosts:
		portScan(tgtHost, tgtPorts, options.verbose)
	
if __name__ == '__main__':
	Main()
		