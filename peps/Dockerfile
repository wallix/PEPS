# The main peps container

# Based on our generic opa container which has mlstatelibs and node built in.
FROM opa:latest

# Download the peps executable
RUN curl -sf -o /tmp/peps.zip -L https://github.com/MLstate/PEPS/releases/download/0.9.9/peps.zip
RUN mkdir -p /peps && cd /peps && unzip -q /tmp/peps.zip
RUN rm /tmp/peps.zip

RUN /usr/bin/npm install -g \
  ursa \
  simplesmtp \
  rai \
  nodemailer \
  ldapjs \
  iconv \
  nodemailer-smtp-transport \
  mailparser \
  html-to-text \
  tweetnacl

# Patch the rai.js node module
RUN cd /usr/local/lib/node_modules/rai/lib; patch rai.js < /peps/rai.patch

# We need to add the webmail modules to the node path
ENV NODE_PATH $NODE_PATH:/peps/_build

# Note the externally mounted volumes
VOLUME ["/data"]

# Run the peps executable
EXPOSE 25
EXPOSE 443
CMD /peps/opa_webmail.exe \
     --http-server-port 443 \
     --db-remote:webmail $MONGOD_PORT_27017_TCP_ADDR:$MONGOD_PORT_27017_TCP_PORT \
     --db-remote:rawdata $MONGOD_PORT_27017_TCP_ADDR:$MONGOD_PORT_27017_TCP_PORT \
     --db-remote:sessions $MONGOD_PORT_27017_TCP_ADDR:$MONGOD_PORT_27017_TCP_PORT \
     --db-remote:tokens $MONGOD_PORT_27017_TCP_ADDR:$MONGOD_PORT_27017_TCP_PORT \
     --solr-addr $SOLR_PORT_8983_TCP_ADDR --solr-port $SOLR_PORT_8983_TCP_PORT \
     --smtp-server-port 25 --smtp-server-auth "" \
     --smtp-monitor-server $EXIM_PORT_80_TCP_ADDR --smtp-monitor-port $EXIM_PORT_80_TCP_PORT \
     --smtp-monitor2-server localhost --smtp-monitor2-port 80 \
     --smtp-server $EXIM_PORT_25_TCP_ADDR --smtp-port $EXIM_PORT_25_TCP_PORT \
     --smtp-secure false --smtp-auth ""

# To run as HTTP instead of HTTPS
#     --no-ssl true

# To enable SMTP debug
#    --smtp-debug true \
