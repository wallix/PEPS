#!/bin/sh
mkdir -p /etc/peps
echo "host = $PEPS_PORT_8999_TCP_ADDR:$PEPS_PORT_8999_TCP_PORT" > /etc/peps/smtpin.ini
exec haraka -c /usr/local/haraka >>/var/log/haraka.log 2>&1
