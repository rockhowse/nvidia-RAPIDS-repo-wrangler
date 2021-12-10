# nvidia-RAPIDS-repo-wrangler
Repo to host some code used to come up to speed on the Nvidia RAPIDS code repositories and to do some basica analysis on types of source being used and existing CI/CD technologies incorporated into the various repositories.

## Overall Goals

- [ ] dockerize our python runtime environment
- [ ] download RAPIDS git repositories for local analysis
- [ ] process the RAPIDS repos to get an overall view of the types of code used
- [ ] provide some basic metrics on types of code used, focusing on CI/CD integrations
- [ ] demonstrate understanding of CI/CD techniques incorporated in the repositories
- [ ] gain a solid understanding of the Conda build process for these repositories

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
❯ docker build -t nvidia-rapids-repo-wrangler:0.0.1 .
[+] Building 0.3s (5/5) FINISHED
 => [internal] load build definition from Dockerfile                                                                                  0.0s
 => => transferring dockerfile: 36B                                                                                                   0.0s
 => [internal] load .dockerignore                                                                                                     0.0s
 => => transferring context: 2B                                                                                                       0.0s
 => [internal] load metadata for docker.io/library/python:3-slim-buster                                                               0.2s
 => CACHED [1/1] FROM docker.io/library/python:3-slim-buster@sha256:d4354e51d606b0cf335fca22714bd599eef74ddc5778de31c64f1f73941008a4  0.0s
 => exporting to image                                                                                                                0.0s
 => => exporting layers                                                                                                               0.0s
 => => writing image sha256:8b231ccfd322862853dbd86c14ca68eb62a85be49e68c6573b0d4176fd984fe7                                          0.0s
 => => naming to docker.io/library/nvidia-rapids-repo-wrangler:0.0.1
```

Checking the version:

```bash
❯ docker image ls
REPOSITORY                    TAG       IMAGE ID       CREATED      SIZE
nvidia-rapids-repo-wrangler   0.0.1     8b231ccfd322   2 days ago   115MB
```

#### Testing python version

```bash
❯ docker run -it nvidia-rapids-repo-wrangler:0.0.1 /bin/bash
root@6de548d21c8c:/# python --version
Python 3.10.1
root@6de548d21c8c:/#
```

## Usage

```bash
❯ docker run nvidia-rapids-repo-wrangler:0.0.1
The Cake Is A Lie!
```
