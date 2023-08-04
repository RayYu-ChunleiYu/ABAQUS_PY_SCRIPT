import os
from control import Controller
from tasks.TaskAxialLoadingCircle import TaskImplement as TaskImplement_CircleAxialLoading
from tasks.TaskAxialLoadingRect import TaskImplement as TaskImplement_RectAxialLoading

import pandas as pd

CWD = os.getcwd()

exp_data_path = os.path.join(CWD, 'exp_verified', 'data.xlsx')
exp_data = pd.read_excel(exp_data_path, sheet_name='Strength')

controller = Controller()

exp_data_first = exp_data.iloc[:1,:]
section_type_series = exp_data_first['Section_type']

section_height_series = exp_data_first['Height(Diameter)']
section_width_series = exp_data_first['Width(Diameter)']
thickness_series = exp_data_first['Tube_thickness']
fy_series = exp_data_first['fy']
fc_series = exp_data_first['fck']

meshsize = 18

for meshsize in reversed([6,9,18,27,36]):
    for section_type, section_height, section_width, thickness, fy, fc in zip(section_type_series, section_height_series,
                                                                              section_width_series, thickness_series,
                                                                              fy_series, fc_series):


        if section_type == 'Rectangle':
            task = TaskImplement_RectAxialLoading()
            geometry = {
                "section_height": section_height,
                "section_width": section_width,
                "tube_thickness": thickness,
                "height": section_height * 3
            }
        elif section_type == 'Circle':
            task = TaskImplement_CircleAxialLoading()
            geometry = {
                "diameter": section_width,
                "tube_thickness": thickness,
                "height": section_width * 3
            }

        parameters = {
            "model_name": f"{section_type}_axialTension",
            "task_work_dir": os.path.join(CWD, 'run_files_meshsize_analysis2', "tension", f"meshsize_{meshsize}"),
            "controller_work_dir": CWD,
            "geometry": geometry,
            "load_displacement_target": geometry['height'] / 20,  # positive as tension ; negative as tension
            "material": {"fc": fc, "ft": fc / 20, "steel_yield": fy},
            "mesh": {"concrete_meshsize": meshsize, "steel_meshsize": meshsize/2, "plate_meshsize": meshsize},
        }

        task.set_parameters(parameters)
        controller.add_task(task)

controller.run()
controller.run_FEM_get_data()
controller.run_FEM_get_data_plot()
controller.run_get_fu_as_excel()
