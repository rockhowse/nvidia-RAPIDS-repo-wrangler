###
# nvidia-RAPIDS-repo-wranger main application
#
# The purpose of this application to do do some discovery
# on the composition of the RAPIDS repositories.
#
###
import os

def get_basic_filetypes_for_repo(repo):
    pass

def wrangle_repo(repos_dir, repo_name, all_repo_info_by_file_type):
  # let's use some os.walk to rip through the files
  # https://stackoverflow.com/questions/19587118/iterating-through-directories-with-python
  # recursion baby!
  full_repo_path = f"{repos_dir}/{repo_name}"
  num_and_ext_count_str = []

  for subdir, dirs, files in os.walk(full_repo_path):
    for file in files:
        #print(os.path.join(subdir, file))

        # let's do VERY simple and naive map based on "file extension" (1 or more . until end of string)
        # and group them that way, later we can get more intelligent and start grouping based on some analysis

        last_period_index = file.rfind('.')

        # -1 is returned if the filename doesn't contain "."
        if last_period_index < 0:
            no_file_extension_key = 'no_file_ext'

            if no_file_extension_key not in all_repo_info_by_file_type:
              all_repo_info_by_file_type[no_file_extension_key] = []

            all_repo_info_by_file_type[no_file_extension_key].append(file)
        else:
          file_extension = file[last_period_index+1:]

          if file_extension not in all_repo_info_by_file_type:
              all_repo_info_by_file_type[file_extension] = []

          all_repo_info_by_file_type[file_extension].append(file)


# main application entrypoint
if __name__ == "__main__":

  # TODO: parametize these
  repos_dir = '../repos'

  # gather some metrics accross ALL repos for final analysis
  all_repo_info_by_file_type = {}

  cloned_repo_dir_names = os.listdir(repos_dir)

  # rip through each repo we downloaded and apply some logic
  [wrangle_repo(repos_dir, repo_name, all_repo_info_by_file_type) for repo_name in cloned_repo_dir_names]

  # output statistics on ALL the files across all repos
  num_and_ext_count_str = []
  [num_and_ext_count_str.append(f"{len(all_repo_info_by_file_type[key]):06}|{key}") for key in all_repo_info_by_file_type.keys()]

  print(f"TOTAL")
  print(f"====================")
  # let's output the top 20 sorted largest to smallest for now
  [print(f"{num_and_extention_str}") for num_and_extention_str in sorted(num_and_ext_count_str, reverse=True)[0:20]]
