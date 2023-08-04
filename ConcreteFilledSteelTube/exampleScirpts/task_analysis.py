from tasks.TaskBendingCircle_SupportEdgeBothRelaxAtZ import TaskBendingFixSymetryDiameter
import os 

CWD = os.getcwd()
thickness = 6.0
diameter = 114.0
steel_yield = 406.0
meshsize = 9.0
fck = 101.0

task = TaskBendingFixSymetryDiameter()
parameters = {
    "model_name" : f"Cirle_T{int(thickness)}_F{int(fck)}_steelyield{int(steel_yield)}_meshsize{int(meshsize)}",
    "task_work_dir" : os.path.join(CWD,"run_files_validation",f"Cirle_T{int(thickness)}_F{int(fck)}_steelyield{int(steel_yield)}_meshsize{int(meshsize)}"),
    "controller_work_dir" : CWD,
    "geometry" : {
        'section_type': 'Circle',
        "diameter":diameter,
        "tube_thickness":thickness,
        },
    "material" : {"fc":fck,"ft":10.0,"steel_yield":steel_yield},
    "mesh" : {"concrete_meshsize":meshsize,"steel_meshsize":meshsize,"plate_meshsize":meshsize},
    
}
task.set_parameters(parameters)
task.run()
task.run_fem_get_data_plot(show=True)

