#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, UserAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import time as time
import os

currentTime = time.time()

def topology():
    
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, accessPoint=UserAP, enable_wmediumd=True, enable_interference=True)

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', range=20)
    sta2 = net.addStation('sta2', range=20)
    ap1 = net.addAccessPoint('ap1', ssid='handover', mode='g', channel='1', passwd='123456789a', 		encrypt='wpa2', position='30,50,0', range=30)
    ap2 = net.addAccessPoint('ap2', ssid='handover', mode='g', channel='6', passwd='123456789a', 		encrypt='wpa2', position='70,50,0', range=30)
    c1 = net.addController('c1', controller=Controller)
   
    print "*** Enabling Association Control (AP)"
    net.associationControl('ssf')
    net.propagationModel("logDistancePropagationLossModel", exp=3)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links"
    net.addLink(ap1, ap2)

    print "*** Setting bgscan"
    net.setBgscan(signal=-50, s_inverval=1, l_interval=3600)
    
    """plotting graph"""
    net.plotGraph(min_x=-30, max_x=120, min_y=-30, max_y=120)
    
    """Seed"""
    net.seed(20)

    "*** Available models: RandomWalk, TruncatedLevyWalk, RandomDirection, RandomWayPoint, GaussMarkov,  	  ReferencePoint, TimeVariantCommunity ***"

    net.startMobility(time=0, model='RandomDirection', min_x=20, max_x=80, min_y=20, max_y=70, min_v=0.3, max_v=0.5)


    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start( [c1] )
    ap2.start([c1])
    

   
    # Capture RSSI vs Association

    #sta1.cmd('while sleep 1; do iw dev sta1-wlan0 link | grep 'signal'; >> handover_log.txt; done')
    #sta1.cmd('iw dev sta1-wlan0 link | grep 'SSID:\|signal' | awk '{printf "%s ", $2$3}'')
    #sta1.cmd('sta1 iw dev sta1-wlan0 link | grep -i 'freq:\|signal' | awk -F',' '{printf "%s ", $2, $3}'')

    #sta1.cmd('sh ./sta1.sh &')
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
