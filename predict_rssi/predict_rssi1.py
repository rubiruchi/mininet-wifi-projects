#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import time as time
import os


def topology():
    
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, accessPoint=OVSKernelAP, enable_wmediumd=True, enable_interference=True)

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8')
   
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='50,50,0')
   
    c1 = net.addController('c1', controller=Controller)
   
    print "*** Enabling Association Control (AP)"
    net.associationControl('ssf')
    net.propagationModel("logDistancePropagationLossModel", exp=3)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()
    
    """plotting graph"""
    net.plotGraph(min_x=0, max_x=200, min_y=0, max_y=200)
    
    """Seed"""
    net.seed(20)

    "*** Available models: RandomWalk, TruncatedLevyWalk, RandomDirection, RandomWayPoint, GaussMarkov,  	  ReferencePoint, TimeVariantCommunity ***"

    #net.startMobility(time=0, repetitions=1, reverse=False)
    #sta1.coord = ['50.0,20.0,0.0', '80.0,50.0,0.0', '50.0,80.0,0.0', '50.0,20.0,0.0', '50.0,20.0,0.0']
    
    #net.mobility(sta1, 'start', time=1)
    #net.mobility(sta1, 'stop',  time=22)
    #net.stopMobility(time=23)


    
    net.startMobility(time=0, model='RandomDirection', min_x=10, max_x=190, min_y=10, max_y=190, min_v=0.5, max_v=0.8)



    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start( [c1] )

    # Capture RSSI vs Association
    sta1.cmd('sh ./sta1.sh &')
    #sta2.cmd('sh ./sta2.sh &')


    # Capture Traffic 
    #ap1.cmd('iw dev ap1-wlan1 interface add mon0 type monitor')
    #ap1.cmd('ifconfig mon0 up')
    #ap1.cmd('sudo wireshark &')
    #ap1.cmd('tcpdump -w final.pcap -s0 -i mon0 -t &')


    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
