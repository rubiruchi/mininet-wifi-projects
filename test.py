#!/usr/bin/python

### This is the script attached to the email...

from mininet.net import Mininet
from mininet.node import Controller,OVSKernelAP,OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import time as time

currentTime = time.time()

def topology():
    
    "Create a network."
    net = Mininet( controller=Controller, link=TCLink, accessPoint=OVSKernelAP, switch=OVSKernelSwitch, enable_wmediumd=True, enable_interference=True )

    print "*** Creating nodes"

    # File Server
    h21 = net.addHost( 'h21', mac='00:00:00:00:00:71', ip='10.0.0.71/8', position='30,85,0')
    h22 = net.addHost( 'h22', mac='00:00:00:00:00:72', ip='10.0.0.72/8', position='70,85,0' ) 

    # Switch
    s11 = net.addSwitch('s11', position='50,70,0')
    
    # Wi-Fi Stations
    sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/8',  range='20', position='70,50,0',)
    sta2 = net.addStation( 'sta2', mac='00:00:00:00:00:02', ip='10.0.0.2/8',  range='20', position='30,50,0',)
    sta3 = net.addStation( 'sta3', mac='00:00:00:00:00:03', ip='10.0.0.3/8',  range='30', position='51,51,0',)
    
    # AP
    ap1 = net.addAccessPoint( 'ap1', ssid= 'ap1-ssid', mode= 'g', channel= '1', position='50,50,0', range=30)

    
    # Controller
    c1 = net.addController( 'c1', controller=Controller )


    # Association based on strongest signal
    print "*** Enabling Association Control (AP)"
    net.associationControl('ssf')
    net.propagationModel("logDistancePropagationLossModel", exp=4)


    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Associating and Creating links"
    net.addLink(h21, s11)
    net.addLink(h22, s11)
    net.addLink(s11, ap1)

    
    # Show the network
    net.plotGraph(max_x=100, max_y=100)
    net.plotNode(h21, position='30,85,0')
    net.plotNode(h22, position='70,85,0')
    net.plotNode(s11, position='50,70,0')


    """Seed"""
    net.seed(1)

    # Mobility (change max_x and max_y to keep sta in range of AP)
    #net.startMobility(time=0, model='RandomWayPoint', min_x=10, max_x=70, min_y=10, max_y=70, min_v=0.3, max_v=0.5)


    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start( [c1] )
    s11.start( [c1] )

  

    # ------------------ Capture Traffic --------------------------------------------------------------------------

    # Method-1:
    # Can capture all frames but not showing RSSI for packets from wired nodes -> Wifi stations
    #ap1.cmd('iw dev ap1-wlan1 interface add mon0 type monitor')
    #ap1.cmd('sudo iw dev mon0 set freq 2412')    
    #ap1.cmd('ifconfig mon0 up')
    #ap1.cmd('sudo wireshark &')
    
    # Method 2
    # mon0 is enabled and up, but not capturing anything
    #sta3.cmd('iw dev sta3-wlan0 interface add mon0 type monitor')
    #sta3.cmd('iw dev sta3-wlan0 del')
    #sta3.cmd('ifconfig mon0 up')
    #sta3.cmd('sudo iw dev mon0 set freq 2412')    
    #sta3.cmd('sudo wireshark &')

    # Method 3
    #sta3.cmd('iw dev sta3-wlan0 interface add mon0 type monitor')
    #sta3.cmd('sudo iw dev mon0 set freq 2412')    
    #sta3.cmd('ifconfig mon0 up')
    #sta3.cmd('sudo wireshark &')
    
    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
