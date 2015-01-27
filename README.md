PEPS = Email for Teams
====

Innovative email and collaboration server with unique social features.

# Why PEPS?

PEPS is an email, file sharing and collaboration server that intends to fullfil the need for high-quality on-premises software that could rival with top-notch SaaS products such as Gmail or Dropbox, and innovate with new features.

Please read more [about PEPS](http://github.com/MLstate/PEPS/wiki/About) and its [roadmap](http://github.com/MLstate/PEPS/wiki/Roadmap). We also have a [FAQ](http://github.com/MLstate/PEPS/wiki/FAQ).

# Installation guide

The deployment of PEPS is using [Docker](http://docker.io) to simplify the installation process.
This quick guide covers the deployment of a single server, which you should have up and running in 30 minutes.

## Docker containers

First install Docker on your server. If you are new to Docker, you can use Docker-ready linux instances at [DigitalOcean](http://digitalocean.com) or similar services. We recommend to have at least 2 Gb RAM in your PEPS instance.

To build the Docker containers and run on a Docker instance, just type:

```sh
# Just in case, install make
apt-get install make
# Clone the repository
git clone https://github.com/MLstate/PEPS
cd PEPS

# Configure your domain name
echo YOUR_DOMAIN_NAME > domain

# Build the containers
make build
make certificate # or install existing certificates server.key and server.crt
# Run the containers
make run
```

To later stop, start and remove containers, you can use:

```sh
make stop
make start
make rm
```

## System Configuration

PEPS runs by default using HTTPS.
The only major pre-requisites are that you should have installed
server.crt and server.key in the `$(PEPS_DATA)` directory (by default `/data/peps`).
If you want to start quickly with a self-signed certificate, type:

```sh
make certificate
make install_cert
```

or copy your domain certificates to `$(PEPS_DATA)` manually before running the containers with `make run`.

<!--  and you
should initialise the $(EXIMIN_DATA) and $(EXIMOUT_DATA) directories
with the exim configuration files.
 -->

## PEPS Configuration

You should now be able to run the PEPS server and connect to it, you then need to:

1. Log in as "admin" user with the "admin" password
2. Go to the administration tab (wheels icon)
3. Change domain name, and activate license by clicking on "Activate"
4. Create users, teams, etc.

# Documentation

Manuals for both users and admins are available in form of the PEPS wiki:

- [User Manual](http://github.com/MLstate/PEPS/wiki/User-Manual)
- [Admin Manual](http://github.com/MLstate/PEPS/wiki/Admin-Manual)
- [Developer Manual](http://github.com/MLstate/PEPS/wiki/Developer-Manual)

# Twitter contacts

- Project created by [@henri_opa](https://twitter.com/henri_opa) at [MLstate](http://mlstate.com)
- Design/UX: [@tweetfr](https://twitter.com/tweetfr)
- Lead developer: [@hchataing](https://twitter.com/hchataing)
