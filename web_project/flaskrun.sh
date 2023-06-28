#!/bin/bash

# Check if Flask is already running on port 5000
netstat -tln | grep ":5000 " > /dev/null
if [[ $? -eq 0 ]]; then
    echo "Flask is already running on port 5000. Exiting..."
    exit 0
fi

# Install necessary packages
sudo yum update -y
sudo yum install git -y
sudo yum install python3-pip -y

# Change to project directory
cd /home/ec2-user/ferari_website/web_project

# Install Flask
sudo pip3 install flask

# Run Flask on port 5000 in the background
export FLASK_APP=app
nohup flask run &
