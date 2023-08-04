import subprocess
import os
import json

from abc import ABC, abstractmethod


class Task(ABC):
    def __init__(self) -> None:
        pass

    def set_parameters(self, parameters: dict):
        """Set parameters for this task
        
        args:
            parameters: dict of parameters
        
        retrun: 
            None
        
        arg parameters keys and values:
        
        'model_name' : name of task
        
        'test_work_dir' : work directory where task will be run
        
        'controller_work_dir' : work directory where controller will be run
        
        'geometry' : {'section_type':Option['Circle','Rectangle'],"diameter":float,"height":float,"width":float,"tube_thickness":float,'length':float}
        
        'material' : {"fc":float,"ft":float,"steel_yield":float}
        
        'mesh' : {"concrete_meshsize":int,"steel_meshsize":int,"plate_meshsize":int}
        """
        self.parameters = parameters

    def create_work_directory(self):
        task_work_dir = self.parameters['task_work_dir']
        # check if dir exist 
        if os.path.isdir(task_work_dir):
            pass
        else:
            os.mkdir(task_work_dir)

    def clear_lck_file(self):
        task_work_dir = self.parameters['task_work_dir']
        files_in_dir = os.listdir(task_work_dir)
        for file in files_in_dir:
            if file.endswith(".lck"):
                os.remove(os.path.join(task_work_dir, file))

    def run_fem_run_script(self):
        self.script_refactor()
        controller_work_directory = self.parameters['controller_work_dir']
        task_work_directory = self.parameters['task_work_dir']
        with open(os.path.join(controller_work_directory, task_work_directory, 'parameter.json'), 'w') as f:
            json.dump(self.parameters, f)
        model_name = self.parameters['model_name']
        print(
            f"run_fem_run_script: {os.path.join(controller_work_directory, task_work_directory, model_name + '_run.py')}")
        return subprocess.call("abq2022 cae noGUI={}".format(
            os.path.join(controller_work_directory, task_work_directory, model_name + "_run.py")), shell=True,
                               cwd=os.path.join(controller_work_directory, task_work_directory))

    def run_fem_get_data_script(self):
        self.script_refactor()
        controller_work_directory = self.parameters['controller_work_dir']
        task_work_directory = self.parameters['task_work_dir']
        model_name = self.parameters['model_name']
        files = os.listdir(os.path.join(controller_work_directory,task_work_directory))
        txt_files = [i for i in files if i.split('.')[-1]=='txt']
        lck_files = [i for i in files if i.split('.')[-1]=='lck']

        for file in txt_files:
            os.remove(os.path.join(controller_work_directory,task_work_directory,file))
        for file in lck_files:
            os.remove(os.path.join(controller_work_directory,task_work_directory,file))

        # try:
        #     os.remove(os.path.join(controller_work_directory, task_work_directory, "curve.txt"))
        #     os.remove(os.path.join(controller_work_directory, task_work_directory, "max_steel_strain.txt"))
        #     os.remove(os.path.join(controller_work_directory, task_work_directory, "min_steel_strain.txt"))
        # except FileNotFoundError:
        #     try:
        #         os.remove(os.path.join(controller_work_directory, task_work_directory, "curve_1.txt"))
        #         os.remove(os.path.join(controller_work_directory, task_work_directory, "curve_2.txt"))
        #         os.remove(os.path.join(controller_work_directory, task_work_directory, "max_steel_strain.txt"))
        #         os.remove(os.path.join(controller_work_directory, task_work_directory, "min_steel_strain.txt"))
        #     except FileNotFoundError:
        #         pass
        # finally:
        #     print(
        #         f'run_fem_get_data_script: {os.path.join(controller_work_directory, task_work_directory, model_name + "_getData.py")}')
        print(
            f'run_fem_get_data_script: {os.path.join(controller_work_directory, task_work_directory, model_name + "_getData.py")}')
        return subprocess.call("abq2022 cae noGUI={}".format(
            os.path.join(controller_work_directory, task_work_directory, model_name + "_getData.py")), shell=True,
                               cwd=os.path.join(controller_work_directory, task_work_directory))

    def run_fem_calculation(self):
        self.create_work_directory()
        self.copy_material_file()
        self.run_fem_run_script()

    def run_fem_get_data(self):
        self.create_work_directory()
        self.run_fem_get_data_script()

    def run(self):
        self.run_fem_calculation()
        self.run_fem_get_data()
        # self.run_fem_get_data_plot()

    # methods that need implementation
    @abstractmethod
    def copy_material_file(self):
        pass

    @abstractmethod
    def run_fem_get_data_plot(self, show: bool = False):
        pass

    @abstractmethod
    def script_refactor(self):
        pass

    @abstractmethod
    def get_fu_as_excel(self):
        pass

    @abstractmethod
    def get_data_parse(self):
        pass

    @abstractmethod
    def parse_string_to_array(self, string: list[str]):
        pass
