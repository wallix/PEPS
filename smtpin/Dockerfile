FROM node:6.7

# Install Haraka
RUN npm install -g Haraka
RUN haraka -i /usr/local/haraka

# Configure domain
ADD ./domain /usr/local/haraka/config/host_list

EXPOSE 25

# Configurations
COPY ./config /usr/local/haraka/config
# Plugins
COPY ./plugins /usr/local/haraka/plugins

# Install plugin dependencies
WORKDIR /usr/local/haraka
RUN npm install

# Mount /etc/peps for TLS certificates
VOLUME ["/etc/peps"]

# Configure domain name
COPY ./domain /usr/local/haraka/config/host_list

# Copy start script
COPY ./haraka.sh /

EXPOSE 25
# TODO: key + dual port
# EXPOSE 587

# Start haraka
CMD ["bash", "/haraka.sh"]
