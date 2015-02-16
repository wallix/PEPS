PEPS = open source email for teams
====

Innovative open source email and collaboration server with unique social features.

Main Features  | 
------------- | 
Clean UX/UI |
Messages  | 
File sharing |
Newsfeed |
Client-side encryption |
New internal message protocol |
Extensible |
RESTful APIs |
Powered by Node.js |
Data in MongoDB |
Open Source |

![Messages View](https://cloud.githubusercontent.com/assets/817369/5923743/09105572-a656-11e4-9305-eb2a2bc578ce.png)

![Dashboard View](https://cloud.githubusercontent.com/assets/817369/5923753/1a5dfd20-a656-11e4-959f-f19d9df12c0e.png)

![Files View](https://cloud.githubusercontent.com/assets/817369/5923759/2596cc3a-a656-11e4-8397-b9296a39001c.png)

# Why PEPS?

PEPS is an email, file sharing and collaboration server that intends to fullfil the need for high-quality on-premises software that could rival with top-notch SaaS products such as Gmail or Dropbox, and innovate with new features.

PEPS is built to be extensible thanks to complete APIs and we aim at creating an ecosystem of compatible apps and services.

Please read more [about PEPS](http://github.com/MLstate/PEPS/wiki/About) and its [roadmap](http://github.com/MLstate/PEPS/wiki/Roadmap). We also have a [FAQ](http://github.com/MLstate/PEPS/wiki/FAQ).

PEPS source is available from a [separate repository](https://github.com/MLstate/PEPS-source) under the Affero GPL License.

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
server.crt and server.key in the `$(PEPS_ETC)` directory (by default `/etc/peps`) which is shared by several containers.
If you want to start quickly with a self-signed certificate, type:

```sh
make certificate
```

before running `make run`.

Note that the same certificates are used for the HTTPS server and the SMTPS services.

<!--  and you
should initialise the $(EXIMIN_DATA) and $(EXIMOUT_DATA) directories
with the exim configuration files.
 -->

## PEPS Configuration

You should now be able to run the PEPS server at `https://YOUR_DOMAIN_NAME` and connect to it, you then need to:

1. Set up the 'admin' password at first launch and accept the license
2. Go to the "Users" tab in the topbar
3. Create users, teams, and go!

# Documentation

Manuals for both users and admins are available in form of the PEPS wiki:

- [User Manual](http://github.com/MLstate/PEPS/wiki/User-Manual)
- [Admin/Operator Manual](http://github.com/MLstate/PEPS/wiki/Admin-Manual)
- [Developer Manual](http://github.com/MLstate/PEPS/wiki/Developer-Manual)

# Twitter contacts

- Project created by [@henri_opa](https://twitter.com/henri_opa) at [MLstate](http://mlstate.com)
- Design/UX: [@tweetfr](https://twitter.com/tweetfr)
- Main developers: [henrichataing](https://github.com/henrichataing), [Aqua-Ye](https://github.com/Aqua-Ye), [cedricss](https://github.com/cedricss), [matbd](https://github.com/matbd), [nrs135](https://github.com/nrs135)
