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
❯ docker build -t nvidia-rapids-repo-wrangler:0.0.2 .
[+] Building 0.4s (8/8) FINISHED
 => [internal] load build definition from Dockerfile                                                                          0.0s
 => => transferring dockerfile: 37B                                                                                           0.0s
 => [internal] load .dockerignore                                                                                             0.0s
 => => transferring context: 2B                                                                                               0.0s
 => [internal] load metadata for docker.io/library/python:3-slim-buster                                                       0.3s
 => [1/3] FROM docker.io/library/python:3-slim-buster@sha256:d4354e51d606b0cf335fca22714bd599eef74ddc5778de31c64f1f73941008a  0.0s
 => [internal] load build context                                                                                             0.0s
 => => transferring context: 52B                                                                                              0.0s
 => CACHED [2/3] WORKDIR /app                                                                                                 0.0s
 => CACHED [3/3] COPY ./nvidia_rapids_repo_wrangler.py .                                                                      0.0s
 => exporting to image                                                                                                        0.0s
 => => exporting layers                                                                                                       0.0s
 => => writing image sha256:3cbf63be3cb69c625b60adfc5603a7e7b297d92eb5a3b4fa96cbeaba423c8b80                                  0.0s
 => => naming to docker.io/library/nvidia-rapids-repo-wrangler:0.0.2                                                          0.0s
```

Checking the version and size:

```bash
❯ docker image ls
REPOSITORY                    TAG       IMAGE ID       CREATED          SIZE
nvidia-rapids-repo-wrangler   0.0.2     3cbf63be3cb6   32 seconds ago   115MB
```

#### Testing python version

```bash
❯ docker run -it -v ${PWD}/../repos:/repos nvidia-rapids-repo-wrangler:0.0.2 /bin/bash
root@2420d20ab319:/app# python --version
Python 3.10.1
root@2420d20ab319:/app#
```

## rapids repo data download

In order for this application to function as expected, you need to have downloaded the repositories using the scripts in the [001~clone-RAPIDS-git-repos](../001~clone-RAPIDS-git-repos/README.md)

### verify mounted data directory

```bash
❯ docker run -it -v ${PWD}/../repos:/repos nvidia-rapids-repo-wrangler:0.0.2 /bin/bash
root@2420d20ab319:/app# ls -al /repos | head
total 8
drwxr-xr-x 80 root root 2560 Dec 11 18:09 .
drwxr-xr-x  1 root root 4096 Dec 11 21:34 ..
-rw-r--r--  1 root root   39 Dec 11 18:09 .gitignore
drwxr-xr-x 13 root root  416 Dec 11 15:32 asvdb
drwxr-xr-x 12 root root  384 Dec 11 17:09 benchmark
drwxr-xr-x 37 root root 1184 Dec 11 15:33 blazingsql-release-staging
drwxr-xr-x  8 root root  256 Dec 11 15:35 blazingsql-testing-files
drwxr-xr-x 19 root root  608 Dec 11 17:09 ccache-feedstock
drwxr-xr-x  7 root root  224 Dec 11 15:32 clang-recipe
root@2420d20ab319:/app# ls -al /repos | tail
drwxr-xr-x 13 root root  416 Dec 11 17:08 spark-examples
drwxr-xr-x 16 root root  512 Dec 11 15:29 thirdparty-cub
drwxr-xr-x 10 root root  320 Dec 11 15:32 thirdparty-freestanding
drwxr-xr-x 23 root root  736 Dec 11 17:09 thirdparty-libcxx
drwxr-xr-x 10 root root  320 Dec 11 17:08 thirdparty-moderngpu
drwxr-xr-x 29 root root  928 Dec 11 17:10 ucx
drwxr-xr-x 25 root root  800 Dec 11 17:07 ucx-py
drwxr-xr-x 17 root root  544 Dec 11 15:32 ucx-split-feedstock
drwxr-xr-x 34 root root 1088 Dec 11 17:07 xgboost
drwxr-xr-x  6 root root  192 Dec 11 17:08 xgboost-conda
```

## basic file type analysis

The nvidia_rapids_repo_wranger application processes the downloaded repositories and dumps out a bunch of infomration about the repos based on simple "file extension" information.

While not perfect, this sets us up to create some more in-depth analysis based on some human evaluation of the results.

### pre-repo summary (top 3 extensions)

Each repository outputs something similar to this output:

```bash
cudf
====================
000343|cpp
000318|cu
000273|py
```

### TOTAL summary (top 10 extensions across all repositories)

```bash
TOTALS
====================
017793|.html
007523|.cpp
005957|.png
005626|.md5
004533|.map
003374|.js
002833|.py
001815|.txt
001803|no_file_ext
001541|.dot
```

## interesting findings

Some interesting findings even at this very basic level of analysis.

### no_file_ext is top count

There are several repos that have the `no_file_ext` count as the highest. These are files that don't have a `.` anywhere inside the file name. More analysis needed to find out what these files are so we can more properly account for them.

Example:

```bash
asvdb
====================
000014|no_file_ext
000011|.sample
000006|.py
```

### The highest number of files by raw count across all repos is `html` with 17k

Kind of surprising. However the more rational `.cpp` extension comes in as second with another suprising `.js` beating out `.py`.

```bash
TOTALS
====================
017793|.html
007523|.cpp
005957|.png
005626|.md5
004533|.map
003374|.js
002833|.py
001815|.txt
001803|no_file_ext
001541|.dot
```

### cross repo top N frequency numbers

`ORIGINAL FINDINDS` updated analysis below:

If we count the number of times a particular extension is in the top based on number of repos we get some interesting data.

```bash
`=== RANK: #01 ===
030|no_file_ext
014|.py
006|.cuh
=== RANK: #02 ===
026|.sample
009|no_file_ext
009|.cu
=== RANK: #03 ===
014|no_file_ext
011|.sh
008|.py
```

* The `no_file_extension` appears as the most frequent in the 1st and 3rd slots the highest.
* The `.py` appears as the second most frequent for the top spot and 3rd most frequent for the third highest.
* The `.sample` one is not a file type I am familiar with but gives me some clues on where to dig next.

#### Exclude `.git/` from file inclusion in analysis

This reduces the number of `no_file_ext` which contained a ton of hash files and other files specific to the git process but not necessarily part of the code being managed.

After excluding the `.git/` folder, we get some results that are a bit more expected, but still not 100% convinced this is providing the full picture.

```bash
=== RANK: #01 ===
020|.py
007|.cuh
005|.yaml
=== RANK: #02 ===
011|.sh
009|.cu
008|.py
=== RANK: #03 ===
010|no_file_ext
010|.sh
007|.py
```

* The `.py` extension appears as the most frequent for the top spot and 3rd most frequent for the second and third highest.
* The `.cuh` and `.cu` extensions now show up as the second most occurring files for the First and Second rankings respectively.
* The `.sh` extension appears as the top most and second most of the rank 2 and 3 positions respectively.
* `no_file_ext` still exists as the top in the third rank, but isn't dominating throughout all the top 3 ranks

## CI/CD integrations

The primary use case for the next phase of functionality is to identify existing CI/CD integrations. Given there are 77 repositories, this CAN occur by hand, but given I have the code to itterate all files in every repo, we can do some simple analysis on the files and directories of common CI/CD implementations to see if we can tease out a bit more information.

### Jenkinsfile

Typically jenkins integration is indicated by the use of files containing the word `Jenkinsfile`. Here's the output of the CI/CD integration with repos that possibly contain jenkins integration.

```json
{
  "ci-cd-jenkins": {
    "cugunrock": [
      "Jenkinsfile"
    ],
    "gpuci-build-environment": [
      "Jenkinsfile"
    ],
    "xgboost": [
      "Jenkinsfile-win64",
      "Jenkinsfile"
    ]
  }
}
```
