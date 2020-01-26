#!/usr/bin/python			
			
from	mininet.topo	import	Topo			
from	mininet.net	import	Mininet
from    mininet.node import OVSSwitch, Controller, RemoteController			
from	mininet.util	import	dumpNodeConnections			
from	mininet.log	import	setLogLevel

setLogLevel( 'info' )

# Two local and one "external" controller (which is actually c0)
# Ignore the warning message that the remote isn't (yet) running
c0 = RemoteController( 'c0', ip='127.0.0.1', port=6633 )
c1 = Controller( 'c1', port=6634 )
c2 = Controller( 'c2', port=6633)

cmap = { 'c0': c1&c2 ,'s1': c1, 's2': c2 }

class MultiSwitch( OVSSwitch ):
	  "Custom Switch() subclass that connects to different controllers"
    def start( self, controllers ):
        return OVSSwitch.start( self, [ cmap[ self.name ] ] )

topo = TreeTopo( depth=2, fanout=2 )
net = Mininet( topo=topo, switch=MultiSwitch, build=False )
for c in [ c0, c1 ]:
    net.addController(c)
net.build()

			
class	MyFirstTopo(	Topo	):			
				"Simple	topology	example."			
				def	__init__(	self	):			
								"Create	custom	topo."			
								#	Initialize	topology			
								Topo.__init__(	self	)			
								#	Add	hosts	and	switches			
								h1	=	self.addHost(	'h1'	)			
								h2	=	self.addHost(	'h2'	)			
								h3	=	self.addHost(	'h3'	)			
								h4	=	self.addHost(	'h4'	)			
								leftSwitch	=	self.addSwitch(	's1'	)			
								rightSwitch	=	self.addSwitch(	's2'	)			
								#	Add	links			
								self.addLink(	h1,	leftSwitch	)			
								self.addLink(	h2,	leftSwitch	)			
								self.addLink(	leftSwitch,	rightSwitch	)			
								self.addLink(	rightSwitch,	h3	)			
								self.addLink(	rightSwitch,	h4	)			
			
def	runExperiment():			
				"Create	and	test	a	simple	experiment"			
				topo	=	MyFirstTopo(	)			
				net	=	Mininet(topo)			
				net.start()			
				print	"Dumping	host	connections"			
				dumpNodeConnections(net.hosts)			
				print	"Testing	network	connectivity"			
				net.pingAll()			
				net.stop()			
			
if	__name__	==	'__main__':			
				#	Tell	mininet	to	print	useful	information			
				setLogLevel('info')			
				runExperiment()
				net.start()
CLI( net )
net.stop()
