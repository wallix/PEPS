# MongoDB container

FROM phusion/baseimage:0.9.16

MAINTAINER MLstate <contact@mlstate.com>

# Add 10gen official apt source to the sources list.
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | tee /etc/apt/sources.list.d/10gen.list

# Install MongoDB.
RUN apt-get update && apt-get install -y \
  mongodb-org-server \
  mongodb-org-shell \
  mongodb-org-tools \
  mongodb-org-mongos

# Bodge for missing "node" executable
#RUN ln -s /usr/bin/nodejs /usr/bin/node
#RUN /usr/bin/npm install -g forever

# Run the mongo daemon.
EXPOSE 27017
CMD ["/usr/bin/mongod", \
     "--port","27017", \
     "--smallfiles", \
     "--dbpath","/data/db", \
     "--logpath","/mongo.log"]
