# 002~nvidia-RAPID-repo-wranger

Dockerized application that will run through the downloaded repos and do some basic analysis on being used per repo.

## Dependencies

The packages that are not default to python are all defined in the the included requirements.txt

* Python 3.10+

## pre-requisites

## OS

MacOS Monterey was used in all testing for this project.

```bash
❯ sw_vers
ProductName:	macOS
ProductVersion:	12.0.1
BuildVersion:	21A559
```

### docker

To avoid polluting our global python environment, we will make use of `requirements.txt` for dependencies and build an ephemeral docker image.

[Docker Desktop for Mac](https://docs.docker.com/desktop/mac/install/) was used.

```bash
❯ docker --version
Docker version 20.10.11, build dea9396
```

### python

Python was chosen for this project as the RAPIDS open source stack relies heavily on python + CUDA integration.

We are choosing to use Python 3 to make sure our solution works with an actively supported version of the language.

We are going to make use of the `slim-buster` variant as the most recent version of `bullseye` doesn't currently have a `slim` build available from docker-hub for the generic python version `3`. One is supported for the explicit python version `3.9` but let's keep it aligned with a flexible python version and a smaller docker image as the exact OS isn't that important for this particular use case.

`Dockerfile` dependency:

```docker
FROM python:3-slim-buster
```

#### Example build

```bash
❯ docker build -t download-rapids-repos:0.0.1 .
[+] Building 0.2s (10/10) FINISHED
 => [internal] load build definition from Dockerfile                                                                            0.0s
 => => transferring dockerfile: 37B                                                                                             0.0s
 => [internal] load .dockerignore                                                                                               0.0s
 => => transferring context: 2B                                                                                                 0.0s
 => [internal] load metadata for docker.io/library/python:3-slim-buster                                                         0.1s
 => [1/5] FROM docker.io/library/python:3-slim-buster@sha256:d4354e51d606b0cf335fca22714bd599eef74ddc5778de31c64f1f73941008a4   0.0s
 => [internal] load build context                                                                                               0.0s
 => => transferring context: 47B                                                                                                0.0s
 => CACHED [2/5] RUN apt-get -y update                                                                                          0.0s
 => CACHED [3/5] RUN apt-get -y install git                                                                                     0.0s
 => CACHED [4/5] WORKDIR /app                                                                                                   0.0s
 => CACHED [5/5] COPY ./clone_git_repos_by_org.py .                                                                             0.0s
 => exporting to image                                                                                                          0.0s
 => => exporting layers                                                                                                         0.0s
 => => writing image sha256:77b446e2683f4e1ee3b8ebddb1449dcaed9e992ac2a933c7d4bf06f290bc3f59                                    0.0s
 => => naming to docker.io/library/download-rapids-repos:0.0.1                                                                  0.0s
```

Checking the version and size:

```bash
❯ docker image ls
REPOSITORY              TAG       IMAGE ID       CREATED          SIZE
download-rapids-repos   0.0.1     77b446e2683f   14 minutes ago   220MB
```

*note* the inclusion of `git` tooling looks to have doubled the size of the image

#### Testing python version

```bash
❯ docker run -it download-rapids-repos:0.0.1 /bin/bash
root@e5b1a92b5aa2:/app# python --version
Python 3.10.1
root@e5b1a92b5aa2:/app#
```

## data download

In order for this application to function as expected, you need to have downloaded the repositories using the scripts in the [001~clone-RAPIDS-git-repos](001~clone-RAPIDS-git-repos/README.md)


