#!/bin/sh

LOAD_BALANCER_IP=$(ip addr show eth0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1)
echo "Running load balancer with '-i=$LOAD_BALANCER_IP' from 'eth0' interface"
python load_balancer.py -i=${LOAD_BALANCER_IP}
