# Solr container
# This version is a temporary fix as the upstream container definition has been ugraded to Solr 5

# This container does not use baseimage yet
FROM    makuk66/docker-oracle-java7
MAINTAINER MLstate <contact@mlstate.com>

ENV SOLR_VERSION 4.10.4
ENV SOLR solr-$SOLR_VERSION
RUN export DEBIAN_FRONTEND=noninteractive && \
  apt-get update && \
  apt-get -y install lsof curl procps && \
  mkdir -p /opt && \
  wget -nv --output-document=/opt/$SOLR.tgz http://www.mirrorservice.org/sites/ftp.apache.org/lucene/solr/$SOLR_VERSION/$SOLR.tgz && \
  tar -C /opt --extract --file /opt/$SOLR.tgz && \
  rm /opt/$SOLR.tgz && \
  ln -s /opt/$SOLR /opt/solr

# Install stuff we need
RUN apt-get update && apt-get install -y \
  curl \
  unzip

# Download the solr config information
RUN curl -sf -o /tmp/solr.zip -L https://github.com/MLstate/PEPS/releases/download/0.9.9/solr.zip
RUN mkdir -p /solr && cd /solr && unzip -q /tmp/solr.zip
RUN rm /tmp/solr.zip

# The solr installation directories.
ENV SOLR_ROOT /opt/solr
ENV SOLR_DATA $SOLR_ROOT/example/solr

# Install the four cores; mail, file, user and contact.
# We need to install the schema file plus a link from the
# solr data directory to the externally mounted data directory.
RUN cp -r $SOLR_DATA/collection1 $SOLR_DATA/peps_mail
RUN echo "name=peps_mail" > $SOLR_DATA/peps_mail/core.properties
RUN cp /solr/conf/solr_schema_mail.xml $SOLR_DATA/peps_mail/conf/schema.xml
RUN ln -s /solr_data/peps_mail $SOLR_DATA/peps_mail/data

RUN cp -r $SOLR_DATA/collection1 $SOLR_DATA/peps_file
RUN echo "name=peps_file" > $SOLR_DATA/peps_file/core.properties
RUN cp /solr/conf/solr_schema_file.xml $SOLR_DATA/peps_file/conf/schema.xml
RUN ln -s /solr_data/peps_file $SOLR_DATA/peps_file/data

RUN cp -r $SOLR_DATA/collection1 $SOLR_DATA/peps_user
RUN echo "name=peps_user" > $SOLR_DATA/peps_user/core.properties
RUN cp /solr/conf/solr_schema_user.xml $SOLR_DATA/peps_user/conf/schema.xml
RUN ln -s /solr_data/peps_user $SOLR_DATA/peps_user/data

RUN cp -r $SOLR_DATA/collection1 $SOLR_DATA/peps_contact
RUN echo "name=peps_contact" > $SOLR_DATA/peps_contact/core.properties
RUN cp /solr/conf/solr_schema_contact.xml $SOLR_DATA/peps_contact/conf/schema.xml
RUN ln -s /solr_data/peps_contact $SOLR_DATA/peps_contact/data

# Run the Solr server.
EXPOSE 8983
CMD ["/bin/bash","-c","cd /opt/solr/example; java -Djetty.port=8983 -jar start.jar"]
