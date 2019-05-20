#!/bin/sh

mkdir -p dist
cd ../../
python3 setup.py sdist
cp -vf dist/* docker_conf/webapp/dist/
cd $OLDPWD

docker build --no-cache -t webapp-odtest1 .
