from control import Controller
from tasks.TaskBendingCircle import TaskImplement as TaskImplement_CircleBending
from tasks.TaskbendingRect import TaskImplement as TaskImplement_RectBending
import pandas as pd
import os

CWD = os.getcwd()

exp_data_path = os.path.join(CWD, 'exp_verified', 'data.xlsx')
exp_data = pd.read_excel(exp_data_path, sheet_name='Strength')

section_material_data = exp_data[
    ["Height(Diameter)", "Width(Diameter)", "Section_type", "Tube_thickness", "fy", "fck", "fcu"]]

controller = Controller()

pure_bending_data = exp_data[exp_data['Load_pattern'] == 'Pure_bending']

pure_bending_section_material_data = pure_bending_data[
    ["Height(Diameter)", "Width(Diameter)", "Section_type", "Tube_thickness", "fy", "fck", "fcu"]]
pure_bending_data_merge = pd.merge(section_material_data, pure_bending_section_material_data,
                                   on=["Height(Diameter)", "Width(Diameter)", "Section_type", "Tube_thickness", "fy",
                                       "fck", "fcu"], how='outer', indicator=True)
expand_pure_bending_data = pure_bending_data_merge[pure_bending_data_merge['_merge'] == 'left_only']

section_type_series = expand_pure_bending_data['Section_type']
section_height_series = expand_pure_bending_data['Height(Diameter)']
section_width_series = expand_pure_bending_data['Width(Diameter)']
thickness_series = expand_pure_bending_data['Tube_thickness']
fy_series = expand_pure_bending_data['fy']
fc_series = expand_pure_bending_data['fck']

length = 1500

meshsize = 9

expand_index = 1
for section_type, section_height, section_width, thickness, fy, fc in zip(section_type_series, section_height_series,
                                                                          section_width_series, thickness_series,
                                                                          fy_series, fc_series):
    # if expand_index < 130:
    #     expand_index += 1
    #     continue
    if section_type == 'Rectangle':
        task = TaskImplement_RectBending()
        geometry = {
            "section_height": section_height,
            "section_width": section_width,
            "tube_thickness": thickness,
            "height": length + 200
        }
    elif section_type == 'Circle':
        task = TaskImplement_CircleBending()
        geometry = {
            "diameter": section_width,
            "tube_thickness": thickness,
            "height": length + 200
        }

    parameters = {
        # "model_name" : f"{section_type}_{section_height}_{section_width}_t{int(thickness)}_fc{int(fc)}fy{int(fy)}",
        "model_name": f"{section_type}_bending",
        "task_work_dir": os.path.join(CWD, 'run_files_expand', "bending", f"expand_{expand_index}"),
        "controller_work_dir": CWD,
        "geometry": geometry,
        "load_support_location": {
            "load": 100 / (length + 200),
            "support": (100 + length / 3) / (length + 200),
        },
        "load_displacement_target": length / 40,  # positive as tension ; negative as compression
        "material": {"fc": fc, "ft": fc / 20, "steel_yield": fy},
        "mesh": {"concrete_meshsize": meshsize, "steel_meshsize": meshsize, "plate_meshsize": meshsize},
    }
    task.set_parameters(parameters)
    controller.add_task(task)
    expand_index += 1


controller.run_FEM_get_data()
controller.run_FEM_get_data_plot()
controller.run_get_fu_as_excel()
