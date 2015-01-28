#!/bin/sh
/peps/opa_webmail.exe \
     --http-server-port 443 \
     --db-remote:webmail $MONGOD_PORT_27017_TCP_ADDR:$MONGOD_PORT_27017_TCP_PORT \
     --db-remote:rawdata $MONGOD_PORT_27017_TCP_ADDR:$MONGOD_PORT_27017_TCP_PORT \
     --db-remote:sessions $MONGOD_PORT_27017_TCP_ADDR:$MONGOD_PORT_27017_TCP_PORT \
     --db-remote:tokens $MONGOD_PORT_27017_TCP_ADDR:$MONGOD_PORT_27017_TCP_PORT \
     --solr-addr $SOLR_PORT_8983_TCP_ADDR --solr-port $SOLR_PORT_8983_TCP_PORT \
     --smtp-out-host $SMTPOUT_PORT_25_TCP_ADDR \
     --smtp-out-port $SMTPOUT_PORT_25_TCP_PORT

# Deprecated parameters.
# --smtp-server-port 25 --smtp-server-auth "" \
# --smtp-secure false --smtp-auth "" \

# To run as HTTP instead of HTTPS
#     --no-ssl true

# To enable SMTP debug
#    --smtp-debug true \
