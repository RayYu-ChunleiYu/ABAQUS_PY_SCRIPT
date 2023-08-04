from control import *

import os 


CWD = os.getcwd()
controller = Controller(2)
for thickness in [4,6,8]:
    for fck in [120.0,130.0,140.0]:
        for steel_yield in [235,345,420]:
            for meshsize in [9,18,27]:
                task = Task()
                parameters = {
                    "model_name" : f"Cirle_T{int(thickness)}_F{int(fck)}_steelyield{int(steel_yield)}_meshsize{int(meshsize)}",
                    "task_work_dir" : os.path.join(CWD,'run_files_new',f"Cirle_T{int(thickness)}_F{int(fck)}_steelyield{int(steel_yield)}_meshsize{int(meshsize)}"),
                    "controller_work_dir" : CWD,
                    "geometry" : {
                        'section_type': 'Circle',
                        "diameter":108.0,
                        "tube_thickness":thickness,
                        },
                    "material" : {"fc":fck,"ft":10.0,"steel_yield":steel_yield},
                    "mesh" : {"concrete_meshsize":meshsize,"steel_meshsize":meshsize,"plate_meshsize":meshsize},
                    
                }
                task.set_parameters(parameters)
                controller.add_task(task)
controller.run()


