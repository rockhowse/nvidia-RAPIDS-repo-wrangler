#!/bin/bash

# build docker image
docker build -t nvidia-rapids-repo-wrangler:0.0.2 .

# clone repositories
docker run -it -v ${PWD}/../repos:/repos nvidia-rapids-repo-wrangler:0.0.2
