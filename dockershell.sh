#!/bin/bash

# Add logic to modify /etc/hosts
last_line=$(tail -n 1 /etc/hosts)
ip_address=$(echo "$last_line" | awk '{print $1}')
modified_ip_address="${ip_address%.*}.1"
echo "$modified_ip_address      localhost" >> /etc/hosts

cat /etc/hosts

# Start your service or application
exec "$@"