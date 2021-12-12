# Changelog for nvida-RAPODS-repo-wrangler application

## 2021-12-12 - 0.0.4

* Added basic summary showing various CI/CD integrations and number of repos using them
* Added detection for Jenkins CI/CD integration
* Added detection for CircleCI CI/CD integration
* Added detection for GithubActions CI/CD integration

## 2021-12-11 - 0.0.3

* Added basic processing for all repositories in the RAPIDSai organization
* Added VERY simple per and cross repo analysis of file types being used based on "extension"

## 2021-12-11 - 0.0.2

* Refactored original code into separate directories for downloading and analysis
* Added new application directory, Dockerfile and helper script to handle downloading the git repo retrieval
* Refactored "download" naming to "clone" for more consistent git-parlance

## 2021-12-10 - 0.0.1

* Added `CHANGELOG.md`
* Added `README.md`
* Initial repo creation, basic documentation and simple Dockerfile implementation.
* Added simple python application + testing docker commands + sample output.
