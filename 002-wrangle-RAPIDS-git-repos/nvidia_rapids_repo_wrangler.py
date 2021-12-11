###
# nvidia-RAPIDS-repo-wranger main application
#
# The purpose of this application to do do some discovery
# on the composition of the RAPIDS repositories.
#
###
import os
import json

# given an extension map, output the top max_top_records based a zero padding specified
def output_simple_metrics_from_extension_map(extension_map, zero_padding, max_top_records, title):
  # output statistics on ALL the files across all repos
  num_and_ext_count_str = []
  [num_and_ext_count_str.append(f"{len(extension_map[key]):0{zero_padding}}|{key}") for key in extension_map.keys()]
  sorted_num_and_ext_count_str = sorted(num_and_ext_count_str, reverse=True)[0:max_top_records]

  print(f"{title}")
  print(f"====================")
  # let's output the top 20 sorted largest to smallest for now
  [print(f"{num_and_extention_str}") for num_and_extention_str in sorted_num_and_ext_count_str]

  return sorted_num_and_ext_count_str

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

def wrangle_repo(repos_dir, repo_name, all_repo_info_by_file_type, count_top_n_extensions):
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
  sorted_num_and_ext_count_str = output_simple_metrics_from_extension_map(repo_info_by_file_type, 6, 3, repo_name)

  # create a list for the top N we have selected above, then count frequency by extension
  for i in list(range(0,len(sorted_num_and_ext_count_str))):
    extension_at_index = sorted_num_and_ext_count_str[i].split("|")[1]

    # create one map per top N
    if i not in count_top_n_extensions:
      count_top_n_extensions[i] = {}

    # add in a place to start counting extension per top N
    if extension_at_index not in count_top_n_extensions[i]:
      count_top_n_extensions[i][extension_at_index] = 0

    # let's increment the count of this extension
    count_top_n_extensions[i][extension_at_index] += 1

def show_count_of_repos_at_top_n(count_top_n_extensions):
  ranked_extension_frequency = {}

  for rank, extensions in count_top_n_extensions.items():
    ranked_extension_frequency = []

    print(f"=== RANK: #{rank+1:02} ===")

    for extension, frequency in extensions.items():
      extension_freq_str = f"{frequency:03}|{extension}"

      ranked_extension_frequency.append(extension_freq_str)

    [print(f"{rank_item}") for rank_item in sorted(ranked_extension_frequency, reverse=True)[0:3]]


# main application entrypoint
if __name__ == "__main__":

  # TODO: parametize these
  repos_dir = '../repos'

  # gather some metrics accross ALL repos for final analysis
  all_repo_info_by_file_type = {}
  count_top_n_extensions = {}

  cloned_repo_dir_names = sorted(os.listdir(repos_dir))

  # rip through each repo we downloaded and apply some logic
  [wrangle_repo(repos_dir, repo_name, all_repo_info_by_file_type, count_top_n_extensions) for repo_name in cloned_repo_dir_names]

  # output the summary information for all repositories combined
  output_simple_metrics_from_extension_map(all_repo_info_by_file_type, 6, 10, 'TOTALS')

  print("Count of repos with the top extension for top N")
  print(f"{json.dumps(count_top_n_extensions, sort_keys=True, indent=2)}")

  show_count_of_repos_at_top_n(count_top_n_extensions)
