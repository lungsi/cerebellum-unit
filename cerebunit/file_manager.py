# =============================================================================
# file_manager.py
#
# created  18 September 2017 Lungsi
# modified  
#
# This py-file contains file functions, initiated by
#
# from cerebunit import file_manager
#
# and individual file_manager initiated by:
#
# 1. file_manager.get_folder_path_and_name()
#    note: This utility is implemented by the                               
#
# =============================================================================

import os


def get_folder_path_and_name():
    """
    Use case: get_folder_path_and_name()
    Note: If you are in ~/cells/PurkinjeCell/some_test.py
          This function will return:
              1. path_to_folder -> ~/cells
              2. folder_name -> PurkinjeCell
    """
    path_with_folder = os.path.dirname(os.getcwd() + os.sep)
    path_to_folder, folder_name = os.path.split(path_with_folder)
    return path_to_folder, folder_name


#def check_and_make_directory(*directory_names): #"model_predictions"
#
#
