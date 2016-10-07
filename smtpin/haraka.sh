#!/bin/sh

# TLS Settings.
cp /etc/peps/server.key /usr/local/haraka/config/tls_key.pem
cp /etc/peps/server.crt /usr/local/haraka/config/tls_cert.pem
# Launch.
exec haraka -c /usr/local/haraka
