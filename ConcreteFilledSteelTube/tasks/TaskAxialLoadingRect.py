import subprocess
import os
import pandas as pd 
import matplotlib 
matplotlib.use('Agg')        
import matplotlib.pyplot as plt 
import numpy as np 
from .TaskAxialLoading import TaskAxialLoading


class TaskImplement(TaskAxialLoading):

    
    def script_read(self):
        controller_work_directory = self.parameters['controller_work_dir']
        
        fem_analysis_script = os.path.join(controller_work_directory,'template','axialLoadingRect.py')
        
        fem_get_data_script = os.path.join(controller_work_directory,'template','axialLoadingAnalysisGetData.py')
        
        with open(fem_analysis_script,'r') as f:
            
            self.script_FEM_run_string = f.read()
            
        with open(fem_get_data_script,'r') as f:
            self.script_FEM_get_data_string = f.read()

            
    def script_refactor_special(self):
        geometry = self.parameters['geometry']
        
        # script FEM run 
        ## geometry setting 
        
        self.script_FEM_run_string=self.script_FEM_run_string.replace("section_height = 108.0","section_height = {}".format(geometry['section_height']))
        self.script_FEM_run_string=self.script_FEM_run_string.replace("section_width = 108.0","section_width = {}".format(geometry['section_width'])) 
        self.script_FEM_run_string = self.script_FEM_run_string.replace("height = section_height*3","height = {}".format(geometry['height']))
        
        

    
