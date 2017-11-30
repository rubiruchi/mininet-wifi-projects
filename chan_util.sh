#!/bin/sh
 
PATH=/usr/bin:/usr/sbin:/bin:/sbin
export PATH
 
INTERFACE=wlan0
CHANNEL=1
 
do_ () {
    echo "active.value $(iw $INTERFACE survey dump | grep active | head -n $CHANNEL | cut -f 4 | cut -d' ' -f 1)"
    echo "busy.value $(iw $INTERFACE survey dump | grep busy | head -n $CHANNEL | cut -f 4 | cut -d' ' -f 1)"
    echo "receive.value $(iw $INTERFACE survey dump | grep receive | head -n $CHANNEL | cut -f 4 | cut -d' ' -f 1)"
    echo "transmit.value $(iw $INTERFACE survey dump | grep transmit | head -n $CHANNEL | cut -f 4 | cut -d' ' -f 1)"
}
 
do_config () {
    cat <<'EOF'
graph_title WiFi survey
graph_args --base 1000
graph_vlabel channel time
graph_category network
active.label active
active.type COUNTER
busy.label busy
busy.type COUNTER                 
receive.label receive
receive.type COUNTER
transmit.label transmit
transmit.type COUNTER
EOF     
}                                                                               
                                                                                 
do_autoconf () {                                                                
    echo yes                                                                   
    exit 0
}
               
case $1 in    
        ''|config|autoconf)
                eval do_$1;;
esac
