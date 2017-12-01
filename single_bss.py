#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller,OVSKernelAP,OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import time as time


def topology():
    
    "Create a network."
    net = Mininet( controller=Controller, link=TCLink, accessPoint=OVSKernelAP, switch=OVSKernelSwitch, enable_wmediumd=True, enable_interference=True )

    print "*** Creating nodes"


    # Wi-Fi Stations
    sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/8',  range='20')
    sta2 = net.addStation( 'sta2', mac='00:00:00:00:00:02', ip='10.0.0.2/8',  range='20')
    sta3 = net.addStation( 'sta3', mac='00:00:00:00:00:03', ip='10.0.0.3/8',  range='20')
    sta4 = net.addStation( 'sta4', mac='00:00:00:00:00:04', ip='10.0.0.4/8',  range='20')
    sta5 = net.addStation( 'sta5', mac='00:00:00:00:00:05', ip='10.0.0.5/8',  range='20') 
    sta6 = net.addStation( 'sta6', mac='00:00:00:00:00:06', ip='10.0.0.6/8',  range='20')
    sta7 = net.addStation( 'sta7', mac='00:00:00:00:00:07', ip='10.0.0.7/8',  range='20')
    sta8 = net.addStation( 'sta8', mac='00:00:00:00:00:08', ip='10.0.0.8/8',  range='20')
    sta9 = net.addStation( 'sta9', mac='00:00:00:00:00:09', ip='10.0.0.9/8',  range='20')
    sta10 = net.addStation('sta10',mac='00:00:00:00:00:10', ip='10.0.0.10/8', range='20')
    sta11 = net.addStation('sta11',mac='00:00:00:00:00:11', ip='10.0.0.11/8', range='20', position='30,50,0')
    sta12 = net.addStation('sta12',mac='00:00:00:00:00:12', ip='10.0.0.12/8', range='20', position='70,50,0')

    # AP
    ap1 = net.addAccessPoint( 'ap1', ssid= 'ap1-ssid', mode= 'g', channel= '1', position='50,50,0', range=50) # dpid='0000000100000002'
    
    # Controller
    c1 = net.addController( 'c1', controller=Controller )


    # Association based on strongest signal
    print "*** Enabling Association Control (AP)"
    net.associationControl('ssf')
    net.propagationModel("logDistancePropagationLossModel", exp=4)


    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    
    # Show the network
    net.plotGraph(max_x=100, max_y=100)


    """Seed"""
    net.seed(1)

    # Mobility (change max_x and max_y to keep sta in range of AP)
    net.startMobility(time=0, model='RandomWayPoint', min_x=10, max_x=90, min_y=10, max_y=90, min_v=0.5, max_v=1)


    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start( [c1] )

 

    # ------------------ Capture Traffic --------------------------------------------------------------------------

    # Method-1: Using Monitor interface on sta1 (Working)
    ap1.cmd('iw dev ap1-wlan1 interface add mon0 type monitor')
    #ap1.cmd('sudo iw dev mon0 set freq 2412')    
    ap1.cmd('ifconfig mon0 up')
    #ap1.cmd('sudo wireshark &')
    ap1.cmd( 'mkdir -p /home/khan/projects-dir/dumps && cd "$_"')
    ap1.cmd('tcpdump -i mon0 -C 300 -s 200 -w single_bss.pcap &')
    
   
    
  

# -------------------- File Download -------------------------------------------


    # Create and Change Work Directories
    sta1.cmd('cd /home/khan/projects-dir/server-h23')
    sta3.cmd('cd /home/khan/projects-dir/server-h23')
    sta5.cmd('cd /home/khan/projects-dir/server-h23')
    sta7.cmd('cd /home/khan/projects-dir/server-h23')
    sta9.cmd('cd /home/khan/projects-dir/server-h23')
    
    sta2.cmd( 'mkdir -p /home/khan/projects-dir/clients/sta2 && cd "$_"')
    sta4.cmd( 'mkdir -p /home/khan/projects-dir/clients/sta4 && cd "$_"')
    sta6.cmd( 'mkdir -p /home/khan/projects-dir/clients/sta6 && cd "$_"')
    sta8.cmd( 'mkdir -p /home/khan/projects-dir/clients/sta8 && cd "$_"')
    sta10.cmd('mkdir -p /home/khan/projects-dir/clients/sta10 && cd "$_"')


    # wget [options] {link}
    # -c: restart incomplete download
    # -b: download in the background
    # --tries=75
    # -i url_list.txt
    # --limit-rate=200k
    # wget --limit-rate=200k -c -b --tries=3 -i /home/khan/projects/server-h1/doclist1.txt &
    

    sta1.cmd('python -m SimpleHTTPServer 81 &')
    sta3.cmd('python -m SimpleHTTPServer 83 &')
    sta5.cmd('python -m SimpleHTTPServer 85 &')
    sta7.cmd('python -m SimpleHTTPServer 87 &')
    sta9.cmd('python -m SimpleHTTPServer 89 &')
    

    
    #sta11.cmd('ping -i 0.2 -s 56 -c 9999999 sta12  &')

    
    #sta2.cmd( 'wget -c -b --tries=75 http://10.0.0.1:81/movie2.mp4')
    #sta4.cmd( 'wget -c -b --tries=75 http://10.0.0.3:83/movie2.mp4')
    #sta6.cmd( 'wget -c -b --tries=75 http://10.0.0.5:85/movie2.mp4')
    #sta8.cmd( 'wget -c -b --tries=75 http://10.0.0.7:87/movie2.mp4')
    #sta10.cmd('wget -c -b --tries=75 http://10.0.0.9:89/movie2.mp4')

    #sta3.cmd('wget --limit-rate=200k -c -b --tries=75 --wait=10 http://10.0.0.71:80/{1..10}.pdf &')
    #sta4.cmd('wget --limit-rate=200k -c -b --tries=75 --wait=15 http://10.0.0.71:80/{1,3,5,7,9}.pdf &')
    #sta5.cmd('wget --limit-rate=200k -c -b --tries=75 --wait=20 http://10.0.0.71:80/{2,4,6,8,10}.pdf &')
    #sta6.cmd('wget --limit-rate=200k -c -b --tries=75 --wait=10 http://10.0.0.71:80/{1..10}.pdf &')
    #sta7.cmd('wget --limit-rate=200k -c -b --tries=75 --wait=50 http://10.0.0.71:80/{1,3,5,7,9}.pdf &')
    #sta8.cmd('wget --limit-rate=200k -c -b --tries=75 --wait=20 http://10.0.0.71:80/{2,4,6,8,10}.pdf &')
    
    #h1.cmd('kill %python')
    #h2.cmd('kill %python')
    


    # ------------------------------------------------------------ Run Simulation ---------------------------------------
    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
