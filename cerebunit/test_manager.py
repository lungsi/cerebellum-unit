# =============================================================================
# test_manager.py
#
# created  04 September 2017 Lungsi
# modified 
#
# This py-file contains file functions, initiated by
#
# from models import test_manager
#
# and individual test_manager initiated by:
#
# 1. test_manager.get_available_tests ( model_scale="cells",
#                                      model_type="PurkinjeCell" )
#
#    note: If you want to get the list of available models for a particular
#          scale of modelling (say, "cells") use the above command.
#
# 2. model_manager.check_and_compile_model ( model_mod_path,
#                                            model_lib_path )
#    note: This utility is implemented by the py-files (__init__)
#          containing models written in NEURON simulator.
#          a. from models imprt file_manager
#          b. model_mod_path, model_lib_path =
#             file_manager.get_model_lib_path( model_scale="cells",
#                                              model_name="PC2015Masoli" )
#          Based on the model_mod_path and model_lib_path this function
#          checks if the model is already compiled in the lib-path.
#          If its not compiled the model mod-files in the mod-path
#          is compiled.
#          c. 2.
#
# =============================================================================

import os


def get_available_tests(model_scale=None, model_type=None):
    """
    Use case: get_available_models(model_scale="cells")
    ------------------------------------
    Function gives you the list of available models for the chosen
    modelling scale.
    """
    current_working_path = os.getcwd() + os.sep + "models"
    model_path = current_working_path + os.sep + model_scale
    os.chdir(model_path) # change pwd path to model_path
    model_directories = \
            [item for item in os.listdir(os.getcwd()) if os.path.isdir(item)]
    #print os.path.isdir(model_directories[0]) # will return True
    os.chdir(os.path.dirname(model_path)) # reset to original path
    #print os.path.isdir(model_directories[0]) # will return False
    return model_directories #return os.listdir(model_path)


def check_and_compile_model(model_mod_path, model_lib_path):
    """
    Use case: check_and_compile_model(model_mod_path, model_lib_path)
    where model_mod_path and model_lib_path strings are obtained by calling the
    get_model_lib_path() function like
    get_model_lib_path(model_scale="cells", model_name="PC2015Masoli")
    ------------------------------------
    If compiled NEURON files are not already present the mod files
    are compiled. The mod directory & compiled directory are both
    childs of their parent model directory.
    """
    if os.path.isfile(model_lib_path) is False:
        #os.system("cd " + modelpath + "; nrnivmodl")
        #os.system("nrnivmodl " + modelpath)
        paths = os.path.split(model_mod_path)
        subprocess.call("cd " + paths[0] + ";nrnivmodl " + paths[1], shell=True)
    else:  # uncomment to debug this function
        print("compiled files already exists")
#
#
