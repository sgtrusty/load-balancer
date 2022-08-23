#!/usr/bin/env bash

'''
 # SpinachSocket - a metric load balancer with multi-threading
 # Copyright (C) 2022  Santiago González <https://github.com/sgtrusty>
 #             ~ Assembled through trust in coffee. ~
 #
 # This program is free software; you can redistribute it and/or modify
 # it under the terms of the CC BY-NC-ND 4.0 as published by
 # the Creative Commons; either version 2 of the License, or
 # (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # CC BY-NC-ND 4.0 for more details.
 #
 # You should have received a copy of the CC BY-NC-ND 4.0 along
 # with this program; if not, write to the  Creative Commons Corp.,
 # PO Box 1866, Mountain View, CA 94042.
 #
'''

C=${1:-1000}

echo -e "Stress test Load Balancer "

PID_LIST=""

echo -e "Started"
START=$(date +%s)
for i in $(seq $C); do
  echo -e "STRESS TEST" | nc 172.25.0.10 5000 > /dev/null 2>&1 &
  PID=$!
  PID_LIST="$PID_LIST $PID"
  #echo -e "Requests $i" ## bottleneck
done
END_REQUEST=$(date +%s)

echo -e "Waiting"
FAIL=0
for PID in $PID_LIST; 
do
  #echo -e "Wait for $PID..." ## bottleneck
  wait $PID || let "FAIL+=1" 
done
END_RECEIVE=$(date +%s)

if [ "$FAIL" == "0" ]; then 
  echo "FAIL! ($FAIL)" 
fi

TIME_REQ=$(echo "($END_REQUEST - $START)" | bc -l)
if [ "$TIME_REQ" == "0" ]; then
  TIME_REQ=1
fi
TIME_REC=$(echo "($END_RECEIVE - $START)" | bc -l)
if [ "$TIME_REC" == "0" ]; then
  TIME_REC=1
fi
RPS_REQ=$(echo "$C / $TIME_REQ" | bc)
RPS_REC=$(echo "$C / $TIME_REC" | bc)
echo -e "Requests Made Per Second = $RPS_REQ op/sec. Elapsed = $TIME_REQ."
echo -e "Requests Received Per Second = $RPS_REC op/sec. Elapsed = $TIME_REC."

# for i in $(seq $C)
# do
#   curl -s "http://localhost:8080/[$MIN-$MAX]" > /dev/null 2>&1 & 
# done
