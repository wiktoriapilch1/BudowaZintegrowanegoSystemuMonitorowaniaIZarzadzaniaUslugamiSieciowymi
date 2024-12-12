#!/bin/sh
PROMETHEUS_SERVER="10.0.0.100"  # Adres IP serwera Prometheusa
REGISTER_ENDPOINT="http://${PROMETHEUS_SERVER}:5000/register"

# Pobierz adres IP maszyny
IP=$(ip addr show eth0 | grep "inet " | awk '{print $2}' | cut -d/ -f1)

if [ -n "$IP" ]; then
    curl -X POST -H "Content-Type: application/json" -d "{\"ip\": \"${IP}\", \"port\": \"8080\"}" "$REGISTER_ENDPOINT"
else
    echo "Error: No IP address found"
fi
