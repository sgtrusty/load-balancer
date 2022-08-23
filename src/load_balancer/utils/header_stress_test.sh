#!/usr/bin/env bash

C=${1:-1000}

echo -e "Stress test Load Balancer "

PID_LIST=""

echo -e "Started"
START=$(date +%s)
for i in $(seq $C); do
  echo "0001STRESS TEST" | nc 172.25.0.10 5000 > /dev/null 2>&1 &
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
