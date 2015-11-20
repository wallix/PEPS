PEPS
====

Innovative open source email and collaboration server with transparent **end-to-end encryption**.

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

![Messages View](https://cloud.githubusercontent.com/assets/817369/7520629/53915714-f4e8-11e4-8ad5-26065cdd9675.png)

![Dashboard View](https://cloud.githubusercontent.com/assets/817369/7517481/948ebf94-f4d5-11e4-98eb-06db45335a19.png)

![Files View](https://cloud.githubusercontent.com/assets/817369/7517512/c5f4153e-f4d5-11e4-8dd1-8e5c8e78f47a.png)

This open source portal enables you to download and install PEPS on your own server.
To get generic information on PEPS, go to [PEPS website](http://peps.in).

The project is active as of November 2015 and our goal is to stabilize Peps as a priority.

# Why PEPS?

PEPS is an open source email, file sharing and collaboration server that intends to fullfil the need for high-quality on-premises software that could rival with top-notch SaaS products such as Gmail or Dropbox, and innovate with new features.

PEPS is built to be extensible thanks to complete APIs and we aim at creating an ecosystem of compatible apps and services.

Please read more [about PEPS](http://github.com/MLstate/PEPS/wiki/About) and its [roadmap](http://github.com/MLstate/PEPS/wiki/Roadmap). We also have a [FAQ](http://github.com/MLstate/PEPS/wiki/FAQ).

This repository contains the source of the PEPS containers.
[PEPS application source](https://github.com/MLstate/PEPS-source) is available from a [separate repository](https://github.com/MLstate/PEPS-source) under the Affero GPL License.

# Installation guide

The deployment of a single PEPS server is made easy with [Docker](http://docker.io).
You should have your server up and running in 30 minutes.
PEPS uses technologies that can scale up, but this will require some more work or you can [contact our company](mailto:contact@mlstate.com). 

## Docker containers

First install Docker on your server. If you are new to Docker, you can use Docker-ready linux instances at [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-run-your-own-mail-server-and-file-storage-with-peps-on-ubuntu-14-04) or similar services. **You must have at least 2 Gb RAM for your PEPS instance**.

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
2. Head to the "Users" tab in the topbar
3. Create users, teams, and go!

# Documentation

Manuals for both users and admins are available in form of the PEPS wiki:

- [User Manual](http://github.com/MLstate/PEPS/wiki/User-Manual)
- [Admin Manual](http://github.com/MLstate/PEPS/wiki/Admin-Manual)
- [Developer Manual](http://github.com/MLstate/PEPS/wiki/Developer-Manual)
- [Operator Manual](https://github.com/MLstate/PEPS/wiki/Operator-Manual)

# Twitter contacts

- Project created by [@henri_opa](https://twitter.com/henri_opa) at [MLstate](http://mlstate.com)
- Design/UX by [@tweetfr](https://twitter.com/tweetfr)
- Main developers: [henrichataing](https://github.com/henrichataing), [Aqua-Ye](https://github.com/Aqua-Ye), [cedricss](https://github.com/cedricss), [matbd](https://github.com/matbd), [nrs135](https://github.com/nrs135)
