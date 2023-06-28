#!/usr/bin/bash
set -ex

#test1
sleep 5
timeout 20 curl http://127.0.0.1:5000
