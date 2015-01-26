# Generic Opa container

FROM phusion/baseimage:0.9.16

MAINTAINER MLstate <contact@mlstate.com>

# Install stuff we need
RUN apt-get update && apt-get install -y \
  curl \
  unzip \
  nodejs \
  npm

# Bodge for missing "node" executable
RUN ln -s /usr/bin/nodejs /usr/bin/node

# Download the opa libs
RUN curl -sf -o /tmp/opa.zip -L https://github.com/MLstate/PEPS/releases/download/0.9.9/opa.zip
RUN mkdir -p /opa && cd /opa && unzip -q /tmp/opa.zip

# Point opa to our downloaded libraries
ENV OPADIR /opa/usr/local/lib/opa
ENV NODE_PATH $OPADIR/static:$OPADIR/stdlib:$OPADIR/stdlib/stdlib.qmljs:/usr/local/lib/node_modules:node_modules:
