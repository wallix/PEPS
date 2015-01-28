FROM phusion/baseimage:0.9.16

MAINTAINER MLstate <contact@mlstate.com>

ENV HOME /root

RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN DEBIAN_FRONTEND=noninteractive apt-get -y -q update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y -q install python-software-properties g++ make git curl
RUN curl -sL https://deb.nodesource.com/setup | sudo bash -
RUN DEBIAN_FRONTEND=noninteractive apt-get -y -q install nodejs
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Mount /etc/peps for TLS certificates
VOLUME ["/etc/peps"]

# Install Haraka
RUN npm install -g Haraka
RUN haraka -i /usr/local/haraka

# Configure domain name
ADD ./domain /usr/local/haraka/config/host_list

# Configure plugins
ADD ./plugins/package.json /usr/local/haraka/package.json
ADD ./plugins/smtpin.js /usr/local/haraka/plugins/smtpin.js

# CHECK: required?
ADD ./config/smtp.ini /usr/local/haraka/config/
ADD ./config/plugins /usr/local/haraka/config/plugins
RUN cd /usr/local/haraka && npm install

# Create haraka runit service
RUN mkdir /etc/service/haraka
ADD haraka.sh /etc/service/haraka/run

EXPOSE 25
# TODO: key + dual port
# EXPOSE 587

# Start the init daemon - runit will launch the Haraka process
CMD ["/sbin/my_init"]
