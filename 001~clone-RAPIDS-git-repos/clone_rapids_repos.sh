#!/bin/bash

# build docker image
docker build -t clone-rapids-repos:0.0.1 .

# clone repositories
docker run -it -v ${PWD}/repos:/repos download-rapids-repos:0.0.1
