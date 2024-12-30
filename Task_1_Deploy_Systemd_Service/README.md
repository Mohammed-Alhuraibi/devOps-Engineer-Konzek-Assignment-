# Simple HTTP Server Setup Guide

## Prerequisites
- A Linux-based operating system with **systemd**.
- **Python 3** installed on your machine.

## Instructions to Run the HTTP Server as a Service

## Clone the repo and, inside the project folder, run the following instructions.


### Move the Python Server to `/opt` for Consistency
```bash
sudo mkdir -p /opt/simple-http-server
sudo cp simple-http-server.py /opt/simple-http-server/
sudo chmod +x /opt/simple-http-server/simple-http-server.py
```

## Create the Logging Directory
```bash
sudo mkdir -p /var/log/simple-http-server
sudo chown www-data:www-data /var/log/simple-http-server
sudo cp simple-http-server.service /etc/systemd/system/
```

## Enable and Start the Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable simple-http-server
sudo systemctl start simple-http-server
```

## Check the Service Status
```bash
sudo systemctl status simple-http-server
```
If it is active, access the server at [localhost:8000](http://localhost:8000). You'll see a hello message with the current time.


## Monitor the Logs
```bash
tail -f /var/log/simple-http-server/output.log
```
