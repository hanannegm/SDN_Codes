#!/usr/bin/python


from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def multiControllerNet():
    "Create a network from semi-scratch with multiple controllers."

    net = Mininet( controller=Controller, switch=OVSSwitch )

    info( "*** Creating (reference) controllers\n" )
    c1 = net.addController( 'c1', port=6633 )
    c2 = net.addController( 'c2', port=6634 )

    info( "*** Creating switches\n" )
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )

    info( "*** Creating hosts\n" )
    hosts1 = [ net.addHost( 'h%d' % n ) for n in ( 1, 2 ) ]
    hosts2 = [ net.addHost( 'h%d' % n ) for n in ( 3, 4 ) ]
   

    info( "*** Creating links\n" )
    for h in hosts1:
        net.addLink( s1, h )
    for h in hosts2:
        net.addLink( s2, h )
    net.addLink( s1, s2 )
    
    info( "*** Starting network\n" )
    net.build()
    c1.start()
    c2.start()
    s1.start( [ c1 ] )
    s2.start( [ c2 ] )

    info( "***Dumping host connections\n")
    dumpNodeConnections(net.hosts)

    info( "*** Testing network\n" )
    net.pingAll()

    info( "*** Testing bandwidth between h1 and h4\n")
    h1, h4 = net.get( 'h1', 'h4' )
    net.iperf( (h1, h4) )

    info( "*** Running CLI\n" )
    CLI( net )

    info( "*** Stopping network\n" )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )  # for CLI output
    multiControllerNet()