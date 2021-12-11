# doesn't look like there is a slim-bullseye yet, let's stick with buster
FROM python:3-slim-buster

# set working directory
WORKDIR /app

# copy app to working dir
COPY ./nvidia_rapids_repo_wrangler.py .

# run our basic application
CMD [ "python", "/app/nvidia_rapids_repo_wrangler.py"]
