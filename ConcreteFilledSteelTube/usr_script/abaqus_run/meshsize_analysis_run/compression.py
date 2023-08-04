import os
import sys
from control import *
from tasks.TaskAxialLoadingCircle import TaskImplement as TaskImplement_CircleAxialLoading
from tasks.TaskAxialLoadingRect import TaskImplement as TaskImplement_RectAxialLoading
import pandas as pd

CWD = os.getcwd()
exp_data_path = os.path.join(CWD, 'data_sheet', 'data.xlsx')
exp_data = pd.read_excel(exp_data_path, sheet_name='Strength')

controller = Controller(1)

exp_data_first = exp_data.iloc[:1,:]

specimen_name_series = exp_data_first['No']

operator_series = exp_data_first['Operator']
section_type_series = exp_data_first['Section_type']

section_height_series = exp_data_first['Height(Diameter)']
section_width_series = exp_data_first['Width(Diameter)']
thickness_series = exp_data_first['Tube_thickness']
fy_series = exp_data_first['fy']
fc_series = exp_data_first['fck']
length_series = exp_data_first['Length']

for meshsize in reversed([6, 9, 18, 27, 36]):
    for specimen_name, operator, section_type, section_height, section_width, length, thickness, fy, fc in zip(
            specimen_name_series, operator_series, section_type_series, section_height_series, section_width_series,
            length_series, thickness_series, fy_series, fc_series):
        if section_type == 'Rectangle':
            task = TaskImplement_RectAxialLoading()
            geometry = {
                "section_height": section_height,
                "section_width": section_width,
                "tube_thickness": thickness,
                "height": length
            }
        elif section_type == 'Circle':
            task = TaskImplement_CircleAxialLoading()
            geometry = {
                "diameter": section_width,
                "tube_thickness": thickness,
                "height": length
            }

        parameters = {
            # "model_name" : f"{section_type}_{section_height}_{section_width}_t{int(thickness)}_fc{int(fc)}fy{int(fy)}",
            "model_name": f"{section_type}_axialCompression",
            "task_work_dir": os.path.join(CWD, 'run_files_meshsize_analysis2', "compression", f"meshsize_{meshsize}"),
            "controller_work_dir": CWD,
            "geometry": geometry,
            "load_displacement_target": -length / 20,
            "material": {"fc": fc, "ft": fc / 20, "steel_yield": fy},
            "mesh": {"concrete_meshsize": meshsize, "steel_meshsize": meshsize/2, "plate_meshsize": meshsize},
        }

        task.set_parameters(parameters)
        controller.add_task(task)

controller.run()
controller.run_FEM_get_data()
controller.run_FEM_get_data_plot()
controller.run_get_fu_as_excel()