###
# nvidia-RAPIDS-repo-wranger main application
#
# The purpose of this application to do do some discovery
# on the composition of the RAPIDS repositories.
#
###
import os

# given an extension map, output the top max_top_records based a zero padding specified
def output_simple_metrics_from_extension_map(extension_map, zero_padding, max_top_records, title):
  # output statistics on ALL the files across all repos
  num_and_ext_count_str = []
  [num_and_ext_count_str.append(f"{len(extension_map[key]):0{zero_padding}}|{key}") for key in extension_map.keys()]

  print(f"{title}")
  print(f"====================")
  # let's output the top 20 sorted largest to smallest for now
  [print(f"{num_and_extention_str}") for num_and_extention_str in sorted(num_and_ext_count_str, reverse=True)[0:max_top_records]]

# given a map and a file name, get the extension and handle it appropriately
def handle_repo_info(extension_map, file_name):
  # let's do VERY simple and naive map based on "file extension" (1 or more . until end of string)
  # and group them that way, later we can get more intelligent and start grouping based on some analysis
  # this WILL include files that start with the character . like .gitignore
  last_period_index = file_name.rfind('.')

  # -1 is returned if the filename doesn't contain "."
  if last_period_index < 0:
      no_file_extension_key = 'no_file_ext'

      if no_file_extension_key not in extension_map:
        extension_map[no_file_extension_key] = []

      extension_map[no_file_extension_key].append(file_name)
  else:
    file_extension = file_name[last_period_index:]

    if file_extension not in extension_map:
        extension_map[file_extension] = []

    extension_map[file_extension].append(file_name)

def wrangle_repo(repos_dir, repo_name, all_repo_info_by_file_type):
  # let's use some os.walk to rip through the files
  # https://stackoverflow.com/questions/19587118/iterating-through-directories-with-python
  # recursion baby!
  full_repo_path = f"{repos_dir}/{repo_name}"
  repo_info_by_file_type = {}

  for subdir, dirs, files in os.walk(full_repo_path):
    for file in files:
        #print(os.path.join(subdir, file))

        # handle the local per-repo, extension map
        handle_repo_info(repo_info_by_file_type, file)

        # handle the global repo extension map
        handle_repo_info(all_repo_info_by_file_type, file)

  # output the summary information for the local repository
  output_simple_metrics_from_extension_map(repo_info_by_file_type, 6, 3, repo_name)

# main application entrypoint
if __name__ == "__main__":

  # TODO: parametize these
  repos_dir = '../repos'

  # gather some metrics accross ALL repos for final analysis
  all_repo_info_by_file_type = {}

  cloned_repo_dir_names = sorted(os.listdir(repos_dir))

  # rip through each repo we downloaded and apply some logic
  [wrangle_repo(repos_dir, repo_name, all_repo_info_by_file_type) for repo_name in cloned_repo_dir_names]

  # output the summary information for all repositories combined
  output_simple_metrics_from_extension_map(all_repo_info_by_file_type, 6, 10, 'TOTALS')
