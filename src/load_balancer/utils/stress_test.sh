#!/usr/bin/env bash

C=${1:-1000}

echo -e "Stress test Load Balancer "

PID_LIST=""

START=$(date +%s)
echo $START
for i in $(seq $C); do
  echo "0001STRESS TEST" | nc 172.25.0.10 5000 > /dev/null 2>&1 &
  PID=$!
  PID_LIST="$PID_LIST $PID"
  echo -e "Requests $i"
done
END=$(date +%s)
echo $END

FAIL=0
for PID in $PID_LIST; 
do
  echo -e "Wait for $PID..."    
  wait $PID || let "FAIL+=1" 
done

if [ "$FAIL" == "0" ]; then 
  echo "YAY!"
  TIME=$(echo "($END - $START)" | bc -l)
  if [ "$TIME" == "0" ]; then
    TIME=1
  fi
  RPS=$(echo "$C / $TIME" | bc)
  echo -e "Requests Per Second = $RPS. Elapsed = $TIME."
else 
  echo "FAIL! ($FAIL)" 
fi

# for i in $(seq $C)
# do
#   curl -s "http://localhost:8080/[$MIN-$MAX]" > /dev/null 2>&1 & 
# done
