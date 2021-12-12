# nvidia-RAPIDS-repo-wrangler
Repo to host some code used to come up to speed on the Nvidia RAPIDS code repositories and to do some basic analysis on types of source being used and existing CI/CD technologies incorporated into the various repositories.

## Overall Goals

- [X] dockerize our python runtime environment
- [X] clone RAPIDS git repositories for local analysis
- [X] process the RAPIDS repos to get an overall view of the types of code used
- [X] provide some basic metrics on types of code used, focusing on CI/CD integrations
- [X] demonstrate understanding of CI/CD techniques incorporated in the repositories

## Basic components

In there are two main components to this projects

### [001-clone-RAPIDS-git-repos](001~clone-RAPIDS-git-repos)

This folder contains the code needed to build and run a dockerized python application that will clone all repositories from the [RAPIDS](https://github.com/RAPIDSai) source repository into the `./repos` folder.

### [002-wrangle-RAPIDS-git-repos](002-wrangle-RAPIDS-git-repos)

This folder contains the code needed to build and run a dockerized python application that will process the cloned repositories, output some summary data on the compostion of the repos with a focus on identifying CI/CD tooling involved.
