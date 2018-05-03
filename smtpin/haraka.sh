#!/bin/sh

# TLS Settings.
cp /etc/peps/server.key /usr/local/haraka/config/tls_key.pem
cp /etc/peps/server.crt /usr/local/haraka/config/tls_cert.pem
# Sleep to wait for PEPS to be ready
sleep 30
exec haraka -c /usr/local/haraka
