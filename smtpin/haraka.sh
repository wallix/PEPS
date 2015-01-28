#!/bin/sh
echo "host = $PEPS_PORT_8999_TCP_ADDR:$PEPS_PORT_8999_TCP_PORT" > /usr/local/haraka/config/smtpin.ini
cp /etc/peps/server.key /usr/local/haraka/config/tls_key.pem
cp /etc/peps/server.crt /usr/local/haraka/config/tls_cert.pem
exec haraka -c /usr/local/haraka >>/var/log/haraka.log 2>&1
