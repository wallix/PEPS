#!/bin/sh

# Basic configuration.
echo "20000000" > /usr/local/haraka/config/databytes
# SMTP in configuration.
echo "host = $PEPS_PORT_8999_TCP_ADDR:$PEPS_PORT_8999_TCP_PORT" > /usr/local/haraka/config/smtpin.ini
# TLS Settings.
cp /etc/peps/server.key /usr/local/haraka/config/tls_key.pem
cp /etc/peps/server.crt /usr/local/haraka/config/tls_cert.pem
# Launch.
exec haraka -c /usr/local/haraka >>/var/log/haraka.log 2>&1
