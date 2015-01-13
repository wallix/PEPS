# Exim4 container

FROM opa:latest

# Install Exim4
RUN apt-get update && apt-get install -y \
  debconf-utils \
  exim4

# Download the launch script and smtp_monitor program
RUN curl -sf -o /tmp/exim.zip -L https://github.com/MLstate/PEPS/releases/download/0.9.9/exim.zip
RUN cd / && unzip -q /tmp/exim.zip
RUN rm /tmp/exim.zip

# Since we run a service we seem to have to update via update-exim4.conf.conf
RUN rm /etc/exim4/update-exim4.conf.conf
RUN ln -s /exim_data/update-exim4.conf.conf /etc/exim4
RUN ln -s /exim_data/exim4.conf.localmacros /etc/exim4
RUN ln -s /exim_data/hubbed_hosts /etc/exim4
RUN rm /etc/exim4/passwd.client
RUN ln -s /exim_data/passwd.client /etc/exim4
RUN rm -rf /var/spool/exim4
RUN ln -s /exim_data/spool /var/spool/exim4

# Run the exim daemon.
EXPOSE 25
EXPOSE 80
CMD ["/exim/launch"]
