# Auth0 and Flask Integration POC

This is a learning space for me separate form the official Auth0 [GitHub Flask project](https://github.com/auth0-samples/auth0-python-web-app)

## Quick Start

The basic steps as listed below will get the project cloned, built as started.

It assumes you have set some `environment` variables (see below) required for the integration.

Quick start commands:

    $ git clone https://github.com/nicc777/od-test-1.git
    $ cd od-test-1
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ cd docker_conf/base/
    (venv) $ ./build_docker_base.sh
    (venv) $ cd ../webapp/
    (venv) $ ./build_webapp.sh
    ...set your environment variables (see below) ...
    (venv) $ docker container rm auth0-flask-poc
    (venv) $ docker run -e DEBUG=$DEBUG \
    -e DEBUG=$DEBUG \
    -e AUTH0_CALLBACK_URL=$AUTH0_CALLBACK_URL \
    -e AUTH0_CLIENT_ID=$AUTH0_CLIENT_ID \
    -e AUTH0_CLIENT_SECRET=$AUTH0_CLIENT_SECRET \
    -e AUTH0_DOMAIN=$AUTH0_DOMAIN \
    -e AUTH0_BASE_URL=$AUTH0_BASE_URL \
    -e AUTH0_AUDIENCE=$AUTH0_AUDIENCE \
    --network container-net \
    -p 127.0.0.1:4000:4000 \
    --name auth0-flask-poc webapp-odtest1

## Environment Variables

You can set the required environment variables with the following values:

    (venv) $ export DEBUG=1
    (venv) $ export AUTH0_CALLBACK_URL=
    (venv) $ export AUTH0_CLIENT_ID=
    (venv) $ export AUTH0_CLIENT_SECRET=
    (venv) $ export AUTH0_DOMAIN="localhost:4000"
    (venv) $ export AUTH0_BASE_URL="https://${AUTH0_DOMAIN}"
    (venv) $ export AUTH0_AUDIENCE="${AUTH0_BASE_URL}/userinfo"

