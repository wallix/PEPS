#!/bin/sh

# Basic configuration.
echo "20000000" > /usr/local/haraka/config/databytes
# Launch.
exec haraka -c /usr/local/haraka >>/var/log/haraka.log 2>&1

