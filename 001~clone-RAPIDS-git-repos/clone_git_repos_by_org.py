###
# This solution was taken from the following stack overflow question
#   https://stackoverflow.com/questions/19576742/how-to-clone-all-repos-at-once-from-github
#
# specifically one-line python answer updated to use f-strings and urllib functions supported by python 3.10+
#   https://stackoverflow.com/a/31937642/941476
#
###
import json, urllib.request, os

def clone_git_repo(is_debug_mode, ssh_url, repos_dir):
  git_command = f"git clone {ssh_url} {repos_dir}"

  print(git_command)

  # when not in debug mode, let's actually clone
  if not is_debug_mode:
    os.system(git_command)

if __name__ == "__main__":

  # TODO: parametize these
  repos_dir = '../repos'
  org_name = 'RAPIDSai'
  is_debug_mode = True

  org_repos = json.load(urllib.request.urlopen(f"https://api.github.com/orgs/{org_name}/repos?per_page=100"))

  print(f"Number of Repos Found: {len(org_repos)}")

  [clone_git_repo(is_debug_mode, r['ssh_url'], repos_dir) for r in org_repos]
