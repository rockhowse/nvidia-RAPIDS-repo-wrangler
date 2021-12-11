# 002~nvidia-RAPID-repo-wranger

Dockerized application that will run through the downloaded repos and do some basic analysis on being used per repo.

## Dependencies

The packages that are not default to python are all defined in the the included requirements.txt

* Python 3.10+
  * json - (python built-in) used to parse, format and write json
  * numpy - provides numerically efficient data structures useful for computation
  * requests - simple and clean HTTP client
  * unittest - (python built-in) provides simple unit-test functionality

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

## Usage

```bash
❯ docker run -v ${PWD}/repos:/repos download-rapids-repos:0.0.1
Number of Repos Found: 77
git clone git@github.com:rapidsai/cudf.git ../repos
git clone git@github.com:rapidsai/libgdf.git ../repos
git clone git@github.com:rapidsai/dask-cudf.git ../repos
...
git clone git@github.com:rapidsai/ptxcompiler.git ../repos
git clone git@github.com:rapidsai/rvc.git ../repos
git clone git@github.com:rapidsai/rapids_triton_pca_example.git ../repos
```

## clone_rapids_repos.sh

A shell script has been provided that will build, tag and run the most basic configuration shown above.

```bash
❯ ./clone_rapids_repos.sh
[+] Building 0.4s (10/10) FINISHED
 => [internal] load build definition from Dockerfile                                                                            0.0s
 => => transferring dockerfile: 37B                                                                                             0.0s
 => [internal] load .dockerignore                                                                                               0.0s
...
 => => exporting layers                                                                                                         0.0s
 => => writing image sha256:77b446e2683f4e1ee3b8ebddb1449dcaed9e992ac2a933c7d4bf06f290bc3f59                                    0.0s
 => => naming to docker.io/library/clone-rapids-repos:0.0.1                                                                     0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
Number of Repos Found: 77
```

### Example Expected Output

#### un-cloned repository

```bash
git clone https://github.com/rapidsai/nvbench ../repos/nvbench
Cloning into '../repos/nvbench'...
remote: Enumerating objects: 1714, done.
remote: Counting objects: 100% (1714/1714), done.
remote: Compressing objects: 100% (549/549), done.
remote: Total 1714 (delta 1160), reused 1695 (delta 1144), pack-reused 0
Receiving objects: 100% (1714/1714), 480.78 KiB | 792.00 KiB/s, done.
Resolving deltas: 100% (1160/1160), done.
```

#### Previously cloned with no changes

```bash
/bin/bash -c 'pushd ../repos/cupy && git pull && popd'
/repos/cupy /app
Already up to date.
/app
```

#### Previously cloned with new upstream changes

```bash
#TODO: update with example
```

#### Possible error state on repeated pull

```bash
/bin/bash -c 'pushd ../repos/pre-commit-hooks && git pull && popd'
/repos/pre-commit-hooks /app
Your configuration specifies to merge with the ref 'refs/heads/master'
from the remote, but no such ref was fetched.
/bin/bash -c 'pushd ../repos/node && git pull && popd'
/repos/node /app
Already up to date.
/app
```

## Notable Issues

### after initial clone, attempts to pull `refs/heads/master` for a couple repos

```bash
/bin/bash -c 'pushd ../repos/cugraphblas && git pull && popd'
/repos/cugraphblas /app
Your configuration specifies to merge with the ref 'refs/heads/master'
from the remote, but no such ref was fetched.
```

and

```bash
/bin/bash -c 'pushd ../repos/pre-commit-hooks && git pull && popd'
/repos/pre-commit-hooks /app
Your configuration specifies to merge with the ref 'refs/heads/master'
from the remote, but no such ref was fetched.
```

### performance issues

When limit the script to just a single repo it took 2+ minutes to clone using this method... while docker + python CAN work as demonstrated going to include a simpler bash implementation to speed up this portion of the code.

#### docker clone speed: `2m 52s`

```bash
❯ ./clone_rapids_repos.sh
[+] Building 0.4s (11/11) FINISHED
 => [internal] load build definition from Dockerfile                                                                            0.0s
 => => transferring dockerfile: 37B                                                                                             0.0s
 => [internal] load .dockerignore                                                                                               0.0s
 => => transferring context: 2B                                                                                                 0.0s
 => [internal] load metadata for docker.io/library/python:3-slim-buster                                                         0.3s
 => [1/6] FROM docker.io/library/python:3-slim-buster@sha256:d4354e51d606b0cf335fca22714bd599eef74ddc5778de31c64f1f73941008a4   0.0s
 => [internal] load build context                                                                                               0.0s
 => => transferring context: 1.18kB                                                                                             0.0s
 => CACHED [2/6] RUN apt-get -y update                                                                                          0.0s
 => CACHED [3/6] RUN apt-get -y install git                                                                                     0.0s
 => CACHED [4/6] RUN mkdir ~/.ssh/ && ssh-keyscan github.com >> ~/.ssh/known_hosts                                              0.0s
 => CACHED [5/6] WORKDIR /app                                                                                                   0.0s
 => [6/6] COPY ./clone_git_repos_by_org.py .                                                                                    0.0s
 => exporting to image                                                                                                          0.0s
 => => exporting layers                                                                                                         0.0s
 => => writing image sha256:a6096e85b573f49ff065823de8af8a307f29400bda2430ee5ed81617b8437107                                    0.0s
 => => naming to docker.io/library/clone-rapids-repos:0.0.1                                                                     0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
Number of Repos Found: 77
git clone https://github.com/rapidsai/cudf ../repos/cudf
Cloning into '../repos/cudf'...
remote: Enumerating objects: 293960, done.
remote: Counting objects: 100% (3418/3418), done.
remote: Compressing objects: 100% (1549/1549), done.
remote: Total 293960 (delta 1971), reused 2837 (delta 1707), pack-reused 290542
Receiving objects: 100% (293960/293960), 92.26 MiB | 1.81 MiB/s, done.
Resolving deltas: 100% (215924/215924), done.
Checking out files: 100% (1913/1913), done.

~/Projects/nvidia/nvidia-RAPIDS-repo-wrangler/001~clone-RAPIDS-git-repos 002-download-RAPIDS-git-repos* 2m 52s
```

#### raw shell clone speed: `17s`

```bash
❯ git clone https://github.com/rapidsai/cudf
Cloning into 'cudf'...
remote: Enumerating objects: 293960, done.
remote: Counting objects: 100% (3418/3418), done.
remote: Compressing objects: 100% (1594/1594), done.
remote: Total 293960 (delta 1963), reused 2785 (delta 1662), pack-reused 290542
Receiving objects: 100% (293960/293960), 92.29 MiB | 7.94 MiB/s, done.
Resolving deltas: 100% (215901/215901), done.

~/Projects/nvidia/nvidia-RAPIDS-repo-wrangler/repos 002-download-RAPIDS-git-repos* 17s
```

## listed vs cloned diff check

In the event there was an issue cloning a repo, this should catch the disparity.

Example after manually removing the `nvbench` repo and running in read-only mode:

```bash
...
git clone https://github.com/rapidsai/nvbench ../repos/nvbench
/bin/bash -c 'pushd ../repos/ucx && git pull && popd'
/bin/bash -c 'pushd ../repos/rapids-triton && git pull && popd'
/bin/bash -c 'pushd ../repos/rapids-triton-template && git pull && popd'
/bin/bash -c 'pushd ../repos/rapids-triton-linear-example && git pull && popd'
/bin/bash -c 'pushd ../repos/blazingsql-release-staging && git pull && popd'
/bin/bash -c 'pushd ../repos/blazingsql-testing-files && git pull && popd'
/bin/bash -c 'pushd ../repos/dask-sql && git pull && popd'
/bin/bash -c 'pushd ../repos/ptxcompiler && git pull && popd'
/bin/bash -c 'pushd ../repos/rvc && git pull && popd'
/bin/bash -c 'pushd ../repos/rapids_triton_pca_example && git pull && popd'
retrieved vs downloaded diff: ['nvbench']
```
