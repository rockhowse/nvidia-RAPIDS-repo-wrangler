# doesn't look like there is a slim-bullseye yet, let's stick with buster
FROM python:3-slim-buster

# we are doing some git things, let's install it
RUN apt-get -y update
RUN apt-get -y install git

# need to add github hosts to known hosts
# https://github.com/ome/devspace/issues/38
RUN mkdir ~/.ssh/ && ssh-keyscan github.com >> ~/.ssh/known_hosts

# set working directory
WORKDIR /app

# copy app to working dir
COPY ./clone_git_repos_by_org.py .

# run our basic application
CMD [ "python", "/app/clone_git_repos_by_org.py"]
