#!/usr/bin/python

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

    # Video Server
    h23 = net.addHost( 'h23', mac='00:00:00:00:00:73', ip='10.0.0.73/8', position='70,85,0' )
    

    # Switch
    s11 = net.addSwitch('s11', position='50,70,0') # dpid='0000000100000001'
    
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
    sta11 = net.addStation('sta11',mac='00:00:00:00:00:11', ip='10.0.0.11/8', range='50', position='51,51,0')

    # AP
    ap1 = net.addAccessPoint( 'ap1', ssid= 'ap1-ssid', mode= 'n', channel= '1', position='50,50,0', range=50) # dpid='0000000100000002'

    #ap1 = net.addAccessPoint( 'ap1', ssid= 'ap1-ssid', dpid='0000000100000002', mode= 'g', channel= 0, position='50,50,0', driver='nl80211', range=50, beacon_int=100, config ='ctrl_interface = /var/run/hostapd/, ctrl_interface_group=0')
    
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
    net.addLink(h23, s11)
    net.addLink(s11, ap1)

    
    # Show the network
    #net.plotGraph(max_x=100, max_y=100)
    #net.plotNode(h1, position='30,85,0')
    #net.plotNode(h2, position='70,85,0')
    #net.plotNode(s1, position='50,70,0')


    """Seed"""
    net.seed(1)

    # Mobility (change max_x and max_y to keep sta in range of AP)
    net.startMobility(time=0, model='RandomWayPoint', min_x=10, max_x=70, min_y=10, max_y=70, min_v=0.3, max_v=0.5)


    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start( [c1] )
    s11.start( [c1] )

   
    # ------------------ Capture RSSI vs Association --------------------------------------------------------------

    #sta3.cmd('while sleep 1; do iw dev sta3-wlan0 link | grep 'signal'; >> sta4.txt; done')
    #sta3.cmd('iw dev sta3-wlan0 link | grep 'SSID:\|signal' | awk '{printf "%s ", $2$3}'')
    

    #sta3.cmd('sh ./sta3.sh &')




    # ------------------ Capture Traffic --------------------------------------------------------------------------

    # Method-1: Using Monitor interface on sta1 (Working)
    #ap1.cmd('iw dev ap1-wlan1 interface add mon0 type monitor')
    #ap1.cmd('sudo iw dev mon0 set freq 2412')    
    #ap1.cmd('ifconfig mon0 up')
    #ap1.cmd('sudo wireshark &')
    #ap1.cmd('tcpdump -w final.pcap -s200 -i mon0 -t &')
    
    # Method 1
    sta11.cmd('iw dev sta11-wlan0 interface add mon0 type monitor')
    sta11.cmd('iw dev sta11-wlan0 del')
    sta11.cmd('ifconfig mon0 up')
    sta11.cmd('sudo iw dev mon0 set freq 2412')    
    sta11.cmd('sudo wireshark &')

    # Method 3 (Not Working)
    #sta11.cmd('sudo iw phy phy0 interface add mon0 type monitor')
    #sta11.cmd('sudo iw dev sta11-wlan0 del')
    #sta11.cmd('sudo ifconfig mon0 up')
    #sta11.cmd('sudo iw dev mon0 set freq 2412')
    #sta11.cmd('sudo wireshark &')
    
    
    # ----------------------- iPerf ---------------------------------------------------------------------------

    # iperf applications (client = sender,  server= sink)

    # TCP 
    #sta1.cmd('iperf -s -w 64k &')
    #sta6.cmd('iperf -c 10.0.0.1  -w 64k -t 30 & sleep 3')

    # UDP
    #sta6.cmd('iperf -u -s &')
    #sta1.cmd('iperf -u -c 10.0.0.6 -b 100M  -t 600 &')


# -------------------- File Download -------------------------------------------


    # Create and Change Work Directories
    h21.cmd('cd /home/khan/projects/server-h21')
    h22.cmd('cd /home/khan/projects/server-h22')
    h23.cmd('cd /home/khan/projects/server-h23')
    sta1.cmd('mkdir -p /home/khan/projects/clients/sta1 && cd "$_"')
    sta2.cmd('mkdir -p /home/khan/projects/clients/sta2 && cd "$_"')
    sta3.cmd('mkdir -p /home/khan/projects/clients/sta3 && cd "$_"')
    sta4.cmd('mkdir -p /home/khan/projects/clients/sta4 && cd "$_"')
    sta5.cmd('mkdir -p /home/khan/projects/clients/sta5 && cd "$_"')
    sta6.cmd('mkdir -p /home/khan/projects/clients/sta6 && cd "$_"')
    sta7.cmd('mkdir -p /home/khan/projects/clients/sta7 && cd "$_"')
    sta8.cmd('mkdir -p /home/khan/projects/clients/sta8 && cd "$_"')
    sta9.cmd('mkdir -p /home/khan/projects/clients/sta9 && cd "$_"')
    sta10.cmd('mkdir -p /home/khan/projects/clients/sta10 && cd "$_"')


    # wget [options] {link}
    # -c: restart incomplete download
    # -b: download in the background
    # --tries=75
    # -i url_list.txt
    # --limit-rate=200k
    # wget --limit-rate=200k -c -b --tries=3 -i /home/khan/projects/server-h1/doclist1.txt &
    #h21.cmd('python -m SimpleHTTPServer 80 &')
    #h22.cmd('python -m SimpleHTTPServer 80 &')

    h23.cmd('python -m SimpleHTTPServer 81 &')
    h23.cmd('python -m SimpleHTTPServer 82 &')
    h23.cmd('python -m SimpleHTTPServer 83 &')
    h23.cmd('python -m SimpleHTTPServer 84 &')
    h23.cmd('python -m SimpleHTTPServer 85 &')
    h23.cmd('python -m SimpleHTTPServer 86 &')
    h23.cmd('python -m SimpleHTTPServer 87 &')
    h23.cmd('python -m SimpleHTTPServer 88 &')
    h23.cmd('python -m SimpleHTTPServer 89 &')
    h23.cmd('python -m SimpleHTTPServer 90 &')

    
    #sta1.cmd('ping -i 0.2 -s 56 -c 9999999 h1  &')

    sta1.cmd('wget --limit-rate=200k -c -b --tries=75 http://10.0.0.73:81/movie2.mp4')
    sta2.cmd('wget --limit-rate=200k -c -b --tries=75 http://10.0.0.73:82/movie2.mp4')
    sta3.cmd('wget --limit-rate=200k -c -b --tries=75 http://10.0.0.73:83/movie2.mp4')
    sta4.cmd('wget --limit-rate=200k -c -b --tries=75 http://10.0.0.73:84/movie2.mp4')
    sta5.cmd('wget --limit-rate=200k -c -b --tries=75 http://10.0.0.73:85/movie2.mp4')
    sta6.cmd('wget --limit-rate=200k -c -b --tries=75 http://10.0.0.73:86/movie2.mp4')
    sta7.cmd('wget --limit-rate=200k -c -b --tries=75 http://10.0.0.73:87/movie2.mp4')
    sta8.cmd('wget --limit-rate=200k -c -b --tries=75 http://10.0.0.73:88/movie2.mp4')
    sta9.cmd('wget --limit-rate=200k -c -b --tries=75 http://10.0.0.73:89/movie2.mp4')
    sta10.cmd('wget --limit-rate=200k -c -b --tries=75 http://10.0.0.73:90/movie2.mp4')

    #sta3.cmd('wget --limit-rate=200k -c -b --tries=75 --wait=10 http://10.0.0.71:80/{1..10}.pdf &')
    #sta4.cmd('wget --limit-rate=200k -c -b --tries=75 --wait=15 http://10.0.0.71:80/{1,3,5,7,9}.pdf &')
    #sta5.cmd('wget --limit-rate=200k -c -b --tries=75 --wait=20 http://10.0.0.71:80/{2,4,6,8,10}.pdf &')
    #sta6.cmd('wget --limit-rate=200k -c -b --tries=75 --wait=10 http://10.0.0.71:80/{1..10}.pdf &')
    #sta7.cmd('wget --limit-rate=200k -c -b --tries=75 --wait=50 http://10.0.0.71:80/{1,3,5,7,9}.pdf &')
    #sta8.cmd('wget --limit-rate=200k -c -b --tries=75 --wait=20 http://10.0.0.71:80/{2,4,6,8,10}.pdf &')
    
    #h1.cmd('kill %python')
    #h2.cmd('kill %python')
    


    


    # Video Streaming  ---------- h2 >> sta2 --------------------------------------------------------

    #sta1.cmd('cvlc rtp://@:5004 --sout \
    #    "#transcode{vcodec=h264,acodec=mpga,ab=128,channels=2,samplerate=44100}:std{access=file,mux=mp4,dst=output.mp4}" \
    #    --run-time 40 vlc://quit &')

    #h1.cmd('cvlc -vvv clip360.mp4 --sout \
    #    "#transcode{vcodec=h264,acodec=mpga,ab=128,channels=2,samplerate=44100}:duplicate{dst=rtp{dst=10.0.0.1,port=5004,mux=ts}}" \
    #    --run-time 40 vlc://quit ') #test.mp4


    # Video Streaming --------- Youtube >> Sta2 ------------------------------------------------------------

    #sta5.cmd('cvlc --preferred-resolution 240 https://www.youtube.com/watch?v=m2Oo4kBHBNU')


    # Video Streaming --------- h2 >> sta2 multicast -----------------------------------------------------

    # Transcode the input stream, display the transcoded stream and send it to a multicast IP address with the associated SAP announce:
#    h2.cmd('vlc -vvv input_stream --sout
#'#transcode{vcodec=mp4v,acodec=mpga,vb=800,ab=128,deinterlace}:
#duplicate{dst=display,dst=rtp{mux=ts,dst=239.255.12.42,sdp=sap,name="TestStream"}}'  ')

    # To receive the input stream that is being multicasted above on a client: 
    # sta2.cmd('vlc rtp://239.255.12.42')

    # ------------------------------------------------------------ Run Simulation ---------------------------------------
    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
