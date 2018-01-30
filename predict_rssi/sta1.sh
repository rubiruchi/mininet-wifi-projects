#!/bin/bash
# Store Parameters of sta1 in a file 'handover_log.csv' in real time.

#while sleep 1; do iw dev sta1-wlan0 link | grep 'signal' >> handover_log1.csv; done


#while sleep 1; iw dev sta1-wlan0 link | grep 'SSID:\|signal' >> handover_log2.csv; done


# Correct
#while sleep 1; do iw dev sta1-wlan0 link | grep 'freq:\|signal' | awk '{printf "%s ", $2, $3}' >> handover_log.csv; done


while sleep 1; do
  iw dev sta1-wlan0 link | awk '/freq/{f=$2};/signal/{s=$2}END{print s","f}'
done >>log1.csv

