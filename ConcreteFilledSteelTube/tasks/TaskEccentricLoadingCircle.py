import subprocess
import os
import pandas as pd 
import matplotlib 
matplotlib.use('Agg')        
import matplotlib.pyplot as plt 
import numpy as np 
from .TaskEccentricLoading import TaskEccentricLoading


class TaskImplement(TaskEccentricLoading):
    
    
    
    def script_read(self):
        controller_work_directory = self.parameters['controller_work_dir']
        
        fem_analysis_script = os.path.join(controller_work_directory,'template','eccentricLoadingCircle.py')
        
        fem_get_data_script = os.path.join(controller_work_directory,'template','eccentricLoadingAnalysisGetData.py')
        
        with open(fem_analysis_script,'r') as f:
            
            self.script_FEM_run_string = f.read()
            
        with open(fem_get_data_script,'r') as f:
            self.script_FEM_get_data_string = f.read()

            
    def script_refactor_special(self):
        geometry = self.parameters['geometry']
        
        # script FEM run 
        ## geometry setting 
        
        self.script_FEM_run_string=self.script_FEM_run_string.replace("tube_diameter = 108.0","tube_diameter = {}".format(geometry['diameter']))
        
        self.script_FEM_run_string = self.script_FEM_run_string.replace("height = tube_diameter*3","height = {}".format(geometry['height']))
        
    
    
