import os
from tasks.TaskBending import TaskBending


class TaskImplement(TaskBending):

  
  
    def script_read(self):
        controller_work_directory = self.parameters['controller_work_dir']
        
        fem_analysis_script = os.path.join(controller_work_directory,'template','bendingCircle.py')
        
        fem_get_data_script = os.path.join(controller_work_directory,'template','bendingAnalysisGetData.py')
        
        
        with open(fem_analysis_script,'r') as f:
            
            self.script_FEM_run_string = f.read()
            
        with open(fem_get_data_script,'r') as f:
            self.script_FEM_get_data_string = f.read()
            
        

            
    def script_refactor_special(self):
        geometry = self.parameters['geometry']
        
        # script FEM run 
        ## geometry setting 
        
        self.script_FEM_run_string=self.script_FEM_run_string.replace("tube_diameter = 108.0","tube_diameter = {}".format(geometry['diameter']))