###
# This solution was taken from the following stack overflow question
#   https://stackoverflow.com/questions/19576742/how-to-clone-all-repos-at-once-from-github
#
# specifically one-line python answer updated to use f-strings and urllib functions supported by python 3.10+
#   https://stackoverflow.com/a/31937642/941476
#
###
import json
import os
import subprocess
import urllib.request

def clone_git_repo(perform_git_actions, repo, repos_dir, cloned_repo_names):
  repo_name = repo['name']
  cloned_repo_names.append(repo_name)

  full_clone_dir = f"{repos_dir}/{repo_name}"

  # if this directory exists, we have cloned the repo
  # let's switch to the default branch and get the latest code
  # need to use /bin/bash explicitly to support pushd/popd
  if os.path.isdir(full_clone_dir):
    git_command = f"/bin/bash -c 'pushd {full_clone_dir} && git pull && popd'"
  else:
    # since these are publically available, let's use html_url
    html_url = repo['html_url']
    git_command = f"git clone {html_url} {full_clone_dir}"

  print(f"{git_command}")

  # when not in debug mode, let's actually clone
  if perform_git_actions:
    # had some issues with os.system() as default shell is /bin/sh
    # made use of the new Python 3.5+ subprocess with shell=True which seems to work
    subprocess.run([git_command], shell=True)

def compare_git_repos_to_local_repos(cloned_repo_names, cloned_repo_dir_names):
    return list(set(cloned_repo_names) - set(cloned_repo_dir_names))

if __name__ == "__main__":

  # TODO: parametize these
  repos_dir = '../repos'
  org_name = 'RAPIDSai'
  perform_git_actions = True
  cloned_repo_names = []

  org_repos = json.load(urllib.request.urlopen(f"https://api.github.com/orgs/{org_name}/repos?per_page=100"))

  print(f"Number of Repos Found: {len(org_repos)}")

  [clone_git_repo(perform_git_actions, repo, repos_dir, cloned_repo_names) for repo in org_repos]

  # finally, let's get the list of directories we downloaded
  # so we can check against the list of repos for any failures
  cloned_repo_dir_names = os.listdir(repos_dir)

  # let's do some quick checking to make sure we didn't miss anything critical
  # compare local repo directories to the repo list we pulled from github
  cloned_repo_diff = compare_git_repos_to_local_repos(cloned_repo_names, cloned_repo_dir_names)

  print(f"retrieved vs downloaded diff: {cloned_repo_diff}")
