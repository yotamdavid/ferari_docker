#!/usr/bin/bash
set -ex

sleep 20
# test1
timeout 20 curl -s $EC2_IP_TEST:5000

# <-- שורה מעודכנת -->
echo "Test finished successfully"  # פלט מובנה לפלט של Jenkins
