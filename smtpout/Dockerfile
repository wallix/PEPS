FROM node:6

# Install Haraka
RUN npm install -g Haraka
RUN haraka -i /usr/local/haraka

# Copy package.json for plugin dependencies
COPY ./package.json /usr/local/haraka

# Install plugin dependencies
WORKDIR /usr/local/haraka
RUN npm install

# Configure domain
COPY ./domain /usr/local/haraka/config/host_list

# Configurations
COPY ./config /usr/local/haraka/config
# Plugins
COPY ./plugins /usr/local/haraka/plugins

# Mount /etc/peps for TLS certificates
VOLUME ["/etc/peps"]

# Copy start script
COPY ./haraka.sh /

EXPOSE 25
# TODO: key + dual port
# EXPOSE 587

# Start haraka
CMD ["bash", "/haraka.sh"]
