#!/bin/bash
# Store Parameters of sta1 in a file 'handover_log.csv' in real time.

#while sleep 1; do iw dev sta1-wlan0 link | grep 'signal' >> handover_log1.csv; done

# SSID
# freq
# RX
# TX
# signal
# tx bitrate
# bss flags
# dtime period
# beacon int

#while sleep 1; iw dev sta1-wlan0 link | grep 'SSID:\|signal' >> handover_log2.csv; done

while sleep 1; do
  iw dev sta2-wlan0 link | awk '/freq/{f=$2};/signal/{s=$2}END{print s","f}'
done >>log2.csv

