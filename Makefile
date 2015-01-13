# PEPS deployment based on Docker containers
# (c) 2014-2015 MLstate

HOSTNAME?=$(shell cat hostname)
DATA?=/data
MONGO_DATA=$(DATA)/db
SOLR_DATA=$(DATA)/solr
PEPS_DATA=$(DATA)/peps
EXIMIN_DATA=$(DATA)/eximin
EXIMOUT_DATA=$(DATA)/eximout

HTTPS_PORT?=443
SMTP_PORT?=25

# Handy if you need --no-cache=true
DOCKER_BUILD_OPTS?=
DOCKER_DAEMON=docker run -d -h $(HOSTNAME)

default:
	@echo make build: build docker containers
	@echo make run: run docker containers
	@echo make certificate: generate self-signed SSL certificate
	@echo ---
	@echo make start/stop/kill/rm

certificate:
	openssl genrsa -des3 -out server.key 1024
	openssl req -new -key server.key -out server.csr
	cp server.key server.key.org
	openssl rsa -in server.key.org -out server.key # strip passphrase
	openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

install_cert:
	cp -a server.key server.crt $(PEPS_DATA)

build:
	cd mongod; docker build $(DOCKER_BUILD_OPTS) -t mongod .
	cd opa; docker build $(DOCKER_BUILD_OPTS) -t opa .
	cd peps; docker build $(DOCKER_BUILD_OPTS) -t peps .
	cd solr; docker build $(DOCKER_BUILD_OPTS) -t solr .
	cd exim; docker build $(DOCKER_BUILD_OPTS) -t exim .

data_init:
	mkdir -p $(SOLR_DATA)/peps_mail $(SOLR_DATA)/peps_file $(SOLR_DATA)/peps_user $(SOLR_DATA)/peps_contact
	mkdir -p $(EXIMOUT_DATA) $(EXIMIN_DATA)
	mkdir -p $(MONGO_DATA)

run: data_init
	$(DOCKER_DAEMON) --name peps_mongod -v $(MONGO_DATA):/data/db:rw mongod
	$(DOCKER_DAEMON) --name peps_exim_out -v $(EXIMOUT_DATA):/exim_data:rw exim
	$(DOCKER_DAEMON) --name peps_solr -v $(SOLR_DATA):/solr_data:rw solr
	$(DOCKER_DAEMON) --name peps_server -p $(HTTPS_PORT):$(HTTPS_PORT) -v $(DATA):$(DATA):ro --link=peps_mongod:mongod --link=peps_solr:solr --link=peps_exim_out:exim peps
	$(DOCKER_DAEMON) --name peps_exim_in -p $(SMTP_PORT):$(SMTP_PORT) -v $(EXIMIN_DATA):/exim_data:rw --link peps_server:peps exim

start:
	docker start peps_mongod peps_solr peps_exim_out peps_server peps_exim_in

stop:
	docker stop peps_exim_in peps_server peps_mongod peps_solr peps_exim_out

kill:
	docker kill peps_exim_in peps_server peps_mongod peps_solr peps_exim_out

rm:
	docker rm peps_exim_in peps_server peps_mongod peps_solr peps_exim_out
