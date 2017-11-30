#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller,OVSKernelAP #,OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import time as time
from time import sleep

currentTime = time.time()

def topology():
    
    "Create a network."
    net = Mininet( controller=Controller, link=TCLink, accessPoint=OVSKernelAP, enable_wmediumd=True, enable_interference=True ) #switch=OVSKernelSwitch

    print "*** Creating nodes"

    # File Server
    h1 = net.addHost( 'h1', mac='00:00:00:00:00:77', ip='10.0.0.77/8' )

    # Video Server
    #h2 = net.addHost( 'h2', mac='00:00:00:00:00:78', ip='10.0.0.78/8' )

    # Switch
    #s1 = net.addSwitch('s1')
    
    # Wi-Fi Stations
    sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/8',  antennaHeight='1', antennaGain='0.8') #, position='45,45,0') # range=36
    sta2 = net.addStation( 'sta2', mac='00:00:00:00:00:02', ip='10.0.0.2/8',  antennaHeight='1', antennaGain='0.8' ) # range=42
    sta3 = net.addStation( 'sta3', mac='00:00:00:00:00:03', ip='10.0.0.3/8',  antennaHeight='1', antennaGain='0.8' ) # range=49
    sta4 = net.addStation( 'sta4', mac='00:00:00:00:00:04', ip='10.0.0.4/8',  antennaHeight='1', antennaGain='0.8' ) # range=58
    sta5 = net.addStation( 'sta5', mac='00:00:00:00:00:05', ip='10.0.0.5/8',  antennaHeight='1', antennaGain='0.8' ) # range=67
    sta6 = net.addStation( 'sta6', mac='00:00:00:00:00:06', ip='10.0.0.6/8',  antennaHeight='1', antennaGain='0.8' ) # range=36
    sta7 = net.addStation( 'sta7', mac='00:00:00:00:00:07', ip='10.0.0.7/8',  antennaHeight='1', antennaGain='0.8' ) # range=42
    sta8 = net.addStation( 'sta8', mac='00:00:00:00:00:08', ip='10.0.0.8/8',  antennaHeight='1', antennaGain='0.8' ) # range=49
    sta9 = net.addStation( 'sta9', mac='00:00:00:00:00:09', ip='10.0.0.9/8',  antennaHeight='1', antennaGain='0.8' ) # range=58
    sta10 = net.addStation('sta10',mac='00:00:00:00:00:10', ip='10.0.0.10/8', antennaHeight='1', antennaGain='0.8' ) # range=42

    # AP
    ap1 = net.addAccessPoint( 'ap1', ssid= 'ap1-ssid', equipmentModel='DI524', range='40', mode='g', channel='10', position='50,50,0', beacon_int='100') # range=334

    #ap1 = net.addAccessPoint( 'ap1', config='ctrl_interface=/var/run/hostapd/,ctrl_interface_group=0')
    
    # Controller
    c1 = net.addController( 'c1', controller=Controller )


    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    # Association based on strongest signal
    print "*** Enabling Association Control (AP)"
    net.associationControl('ssf')
    net.propagationModel("logDistancePropagationLossModel", exp=4)

    print "*** Associating and Creating links"
    #net.addLink(s1, h1)
    #net.addLink(s1, h2)
    #net.addLink(s1, ap1)
    net.addLink(h1, ap1)

    
    # Show the network
    net.plotGraph(max_x=100, max_y=100)
    net.plotNode(h1, position='20,80,0')


    """Seed"""
    net.seed(1)

    # Mobility (change max_x and max_y to keep sta in range of AP)
    net.startMobility(time=0, model='RandomWayPoint', min_x=10, max_x=70, min_y=10, max_y=70, min_v=0.1, max_v=0.3)


    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start( [c1] )

    # Show Flow tables
    # sh ovs-ofctl dump-flows s1
    
    # Configuring flow tables in AP
    # sh ovs-ofctl add-flow ap1 in_port=1,actions=output:2
    # sh ovs-ofctl add-flow ap1 in_port=2,actions=output:1

    # Delete flows
    # sh ovs-ofctl del-flows ap1


   
    
    # ------------------ Capture Traffic --------------------------------------------------------------------------

    # Method-1: Using Monitor interface on sta1 (Working)
    ap1.cmd('iw dev ap1-wlan1 interface add mon0 type monitor')
    ap1.cmd('sudo iw dev mon0 set freq 2457')    
    ap1.cmd('ifconfig mon0 up')
    ap1.cmd('sudo wireshark &')

    
    
    
    # Method-2: Not Working
    #sta1.cmd('sudo iw sta1-wlan0 interface add mon0 type monitor')
    #sta1.cmd('sudo ifconfig mon0 up')
    #sta1.cmd('sudo iw dev mon0 set freq 2457')  
    #sta1.cmd('sudo wireshark &')  
    #sta1.cmd('sudo tcpdump -i mon0 -n -w wireless.cap')
    

    # Method-3: Using hwsim0 interface
    #c1.cmd('sudo wireshark &')
    #c1.cmd('sh ifconfig hwsim0 up')
    #c1.cmd('sudo iw dev mon0 set freq 2412')
    
    # ----------------------- Applications ---------------------------------------------------------------------------

    # iperf applications (client = sender,  server= sink)

    # TCP Servers (Default Port 5001)

    #sta1.cmd('iperf -s -w 64k &') # set
    #sta2.cmd('iperf -s -w 64k &') # set
    #sta3.cmd('iperf -s -w 64k &')
    #sta4.cmd('iperf -s -w 64k &')
    #sta5.cmd('iperf -s -w 64k &')

    # UDP Servers
    #sta6.cmd('iperf -u -s &')
    #sta7.cmd('iperf -u -s &')
    #sta8.cmd('iperf -u -s &') # set
    #sta9.cmd('iperf -u -s &') # set
    #sta10.cmd('iperf -u -s &')

    # TCP Clients
    #sta6.cmd('iperf -c 10.0.0.1  -w 64k -t 30 & sleep 3')  # set # (-P 2) two parallel streams, (-d) simultaneous upload and downlaod
    #time.sleep(100)
    #sta7.cmd('iperf -c 10.0.0.2  -w 64KB -t 500 & sleep 2') # set
    #sta8.cmd('iperf -c 10.0.0.3  -w 64KB -t 300 &')
    #sta9.cmd('iperf -c 10.0.0.4  -w 64KB -t 200 & ')
    #sta10.cmd('iperf -c 10.0.0.5 -w 64KB -t 100 & ')

    

    # UDP Clients
    #sta1.cmd('iperf -u -c 10.0.0.6 -b 100M  -t 600 &')
    #sta2.cmd('iperf -u -c 10.0.0.7 -b 100M  -t 400 & ')

    #sta3.cmd('iperf -u -c 10.0.0.8  -t 100 & sleep 1') # set
    #sta4.cmd('iperf -u -c 10.0.0.9  -t 300 & sleep 2') # set

    #sta5.cmd('iperf -u -c 10.0.0.10 -t 600 & sleep 3')


    # HTTP Server (Sender i.e. website host)
    #h1.cmd('python -m SimpleHTTPServer 80 &')

    # HTTP Clients (Sink)
    #sta1.cmd('wget -O- h1')
    #sta2.cmd('wget -O- h1')
    #sta3.cmd('wget -O- h1')
    #sta4.cmd('wget -O- h1')
    #sta5.cmd('wget -O- h1')
    #sta6.cmd('wget -O- h1')
    #sta7.cmd('wget -O- h1')
    #sta8.cmd('wget -O- h1')
    #sta9.cmd('wget -O- h1')
    #sta10.cmd('wget -O- h1')

    #h1.cmd('kill %python')                  

    # Download a PDF file from server
    h1.cmd('cd /home/khan/projects/server-h1')
    #h1.cmd('python -m SimpleHTTPServer 8000 &')

    #sta1.cmd('cd /home/khan/projects/clients/sta1 &')

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

    
    
    #sta1.cmd('wget http://10.0.0.77:80/1.pdf')
    #sta2.cmd('wget http://10.0.0.77:81/1.pdf')
    #sta3.cmd('wget http://10.0.0.77:81/1.pdf &')
    #sta4.cmd('wget http://10.0.0.77:81/1.pdf &')
    #sta5.cmd('wget http://10.0.0.77:81/1.pdf &')
    #sta6.cmd('wget http://10.0.0.77:81/1.pdf &')
    #sta7.cmd('wget http://10.0.0.77:81/1.pdf &')
    #sta8.cmd('wget http://10.0.0.77:81/1.pdf &')
    #sta9.cmd('wget http://10.0.0.77:81/1.pdf &')
    #sta10.cmd('wget http://10.0.0.77:81/1.pdf &')

    #h1.cmd('kill %python')
    


    #ap1.cmd('tcpdump -w ap1.pcap -s 96 -i ap1-wlan1 -t &')
    #sta1.cmd('tcpdump -w sta1.pcap -s 96 -i sta1-wlan0 -t &')
    #sta2.cmd('tcpdump -w sta2.pcap -s 96 -i sta2-wlan0 -t &')
    #sta2.cmd('iperf -s &')
    #sta1.cmd('iperf -c 10.0.0.2 -t 20 &')


    # Streaming Server
    #h1.cmd('cd /home/khan/projects/h1-server')
    #h1.cmdPrint("cvlc -vvv clip.mp4 --sout '#duplicate{dst=rtp{dst=10.0.0.5,port=5004,mux=ts},dst=display}' :sout-keep &")
    #h1.cmdPrint("echo $!") # PID of latest bg process

    # Streaming Client
    #sta5.cmd('cd /home/khan/projects/client-sta5')
    #sta5.cmdPrint("cvlc rtsp://10.0.0.5:5004/clip.mp4 &") # Unicast Stream
    #sta5.cmdPrint("echo $!")



    # Stream video from h1 to sta1
    #sta1.cmd('cvlc rtp://@:5004 --sout \
    #    "#transcode{vcodec=h264,acodec=mpga,ab=128,channels=2,samplerate=44100}:std{access=file,mux=mp4,dst=output.mp4}" \
    #    --run-time 40 vlc://quit &')

    #h1.cmd('cvlc -vvv clip360.mp4 --sout \
    #    "#transcode{vcodec=h264,acodec=mpga,ab=128,channels=2,samplerate=44100}:duplicate{dst=rtp{dst=10.0.0.1,port=5004,mux=ts}}" \
    #    --run-time 40 vlc://quit ') #test.mp4


    # Streaming youtube
    #sta5.cmd('cvlc --preferred-resolution 240 https://www.youtube.com/watch?v=m2Oo4kBHBNU')


    # Multicast Streaming
    # Transcode the input stream, display the transcoded stream and send it to a multicast IP address with the associated SAP announce:
#    h1.cmd('vlc -vvv input_stream --sout
#'#transcode{vcodec=mp4v,acodec=mpga,vb=800,ab=128,deinterlace}:
#duplicate{dst=display,dst=rtp{mux=ts,dst=239.255.12.42,sdp=sap,name="TestStream"}}'  ')

    # To receive the input stream that is being multicasted above on a client: 
    # sta1.cmd('vlc rtp://239.255.12.42')

    # ------------------------------------------------------------ Run Simulation ---------------------------------------
    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
