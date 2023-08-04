import os
from control import Controller
from tasks.TaskAxialLoadingCircle import TaskImplement as TaskImplement_CircleAxialLoading
from tasks.TaskAxialLoadingRect import TaskImplement as TaskImplement_RectAxialLoading

import pandas as pd

CWD = os.getcwd()

exp_data_path = os.path.join(CWD, 'exp_verified', 'data.xlsx')
exp_data = pd.read_excel(exp_data_path, sheet_name='Strength')

section_material_data = exp_data[
    ["Height(Diameter)", "Width(Diameter)", "Section_type", "Tube_thickness", "fy", "fck", "fcu"]]

controller = Controller()

axial_tension_data = exp_data[exp_data['Load_pattern'] == 'Short_column_under_axial_tension']

specimen_name_series = axial_tension_data['No']
section_type_series = axial_tension_data['Section_type']
section_height_series = axial_tension_data['Height(Diameter)']
section_width_series = axial_tension_data['Width(Diameter)']
thickness_series = axial_tension_data['Tube_thickness']
fy_series = axial_tension_data['fy']
fc_series = axial_tension_data['fck']

meshsize = 9
expand_index = 1

for specimen_name,section_type, section_height, section_width, thickness, fy, fc in zip(specimen_name_series,section_type_series, section_height_series,
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
        # "model_name" : f"{section_type}_{section_height}_{section_width}_t{int(thickness)}_fc{int(fc)}fy{int(fy)}",
        "model_name": f"{section_type}_axialTension",
        "task_work_dir": os.path.join(CWD, 'run_files_exp_verify', "axialTension", f"{specimen_name}"),
        "controller_work_dir": CWD,
        "geometry": geometry,
        "load_displacement_target": -geometry['height'] / 20,  # positive as tension ; negative as tension
        "material": {"fc": fc, "ft": fc / 20, "steel_yield": fy},
        "mesh": {"concrete_meshsize": meshsize, "steel_meshsize": meshsize, "plate_meshsize": meshsize},
    }

    task.set_parameters(parameters)
    controller.add_task(task)
    expand_index += 1

# controller.run_FEM_get_data_plot()
controller.run_get_fu_as_excel()
