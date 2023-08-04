from control import *

import os 
from tasks.TaskbendingCircle_SupportEdgeBothRelaxAtZEndPlateFixAtZ import TaskImplement


CWD = os.getcwd()


diameter_list = []
height_list = []
load_location = []
support_location = 0.5
fck_list = []
fy_list = []
meshsize = 18
thickness_list = []

run_floder_path = "run_files_"+"new"

controller = Controller(2)
for diameter,height,thickness,fck,fy in zip(diameter_list,height_list,thickness_list,fck_list,fy_list):            
    task = TaskImplement()
    parameters = {
        "model_name" : f"Cirle_T{int(thickness)}_F{int(fck)}_steelyield{int(fy)}_meshsize{int(meshsize)}",
        "task_work_dir" : os.path.join(CWD,run_floder_path,f"Cirle_T{int(thickness)}_F{int(fck)}_steelyield{int(fy)}_meshsize{int(meshsize)}"),
        "controller_work_dir" : CWD,
        "geometry" : {
            "diameter":diameter,
            "tube_thickness":thickness,
            "height":height
            },
        "load_support_location":{
            "load":load_location,
            "support":support_location
        },
        "material" : {"fc":fck,"ft":10.0,"steel_yield":fy},
        "mesh" : {"concrete_meshsize":meshsize,"steel_meshsize":meshsize,"plate_meshsize":meshsize},
        
    }
    task.set_parameters(parameters)
    controller.add_task(task)
controller.run()


