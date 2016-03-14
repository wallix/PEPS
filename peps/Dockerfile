# The main peps container

# Based on our generic opa container which has mlstatelibs and node built in.
FROM opa:latest

MAINTAINER MLstate <contact@mlstate.com>

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
  tweetnacl@0.13.3 \
  intl-messageformat intl

# We need to add the webmail modules to the node path
ENV NODE_PATH $NODE_PATH:/peps/_build

# Get configuration data
VOLUME ["/etc/peps"]
# ADD ../domain /etc/peps/domain

# FIXME: SMTP out
# EXPOSE 25
EXPOSE 443
# SMTP in port
EXPOSE 8999

# Add startup scripts (or to /etc/service/peps?)
ADD peps.sh /etc/my_init.d/10peps.sh

# Start the init daemon
CMD ["/sbin/my_init"]
