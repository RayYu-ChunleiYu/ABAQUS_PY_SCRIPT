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

section_material_data.to_excel("all_section.xlsx")



controller = Controller()

axial_tension_data = exp_data[exp_data['Load_pattern'] == 'Short_column_under_axial_tension']
axial_tension_section_material_data = axial_tension_data[
    ["Height(Diameter)", "Width(Diameter)", "Section_type", "Tube_thickness", "fy", "fck", "fcu"]]


axial_tension_section_material_data.to_excel("section_tension.xlsx")

axial_tension_data_merge = pd.merge(section_material_data, axial_tension_section_material_data,
                                    on=["Height(Diameter)", "Width(Diameter)", "Section_type", "Tube_thickness", "fy",
                                        "fck", "fcu"], how='outer', indicator=True)
expand_axial_tension_data = axial_tension_data_merge[axial_tension_data_merge['_merge'] == 'left_only']

section_type_series = expand_axial_tension_data['Section_type']
section_height_series = expand_axial_tension_data['Height(Diameter)']
section_width_series = expand_axial_tension_data['Width(Diameter)']
thickness_series = expand_axial_tension_data['Tube_thickness']
fy_series = expand_axial_tension_data['fy']
fc_series = expand_axial_tension_data['fck']

expand_axial_tension_data.to_excel('section.xlsx', index=False)

meshsize = 18
expand_index = 1

calculate_data = pd.read_excel(os.path.join(CWD, 'run_files_expand', 'axialTension', 'final_data.xlsx'))
unfinished_job = calculate_data[calculate_data['interpolate strain'] != 0.01]
unfinished_job_index_name = unfinished_job["specimen_name"]
unfinished_job_index = [int(i.split("_")[-1]) for i in unfinished_job_index_name]



for section_type, section_height, section_width, thickness, fy, fc in zip(section_type_series, section_height_series,
                                                                          section_width_series, thickness_series,
                                                                          fy_series, fc_series):

    # task_dir = os.path.join(CWD, 'run_files_expand', "axialTension",
    #                         f"expand_{expand_index}")
    # # check if curve.txt file exist in task_dir
    # if os.path.exists(os.path.join(task_dir, "curve.txt")):
    # if expand_index not in [42,43]:
    #     expand_index += 1
    #     continue
    if expand_index not in unfinished_job_index:
        expand_index += 1
        continue
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
        "task_work_dir": os.path.join(CWD, 'run_files_expand', "axialTension", f"expand_{expand_index}"),
        "controller_work_dir": CWD,
        "geometry": geometry,
        "load_displacement_target": geometry['height'] / 50,  # positive as tension ; negative as compression
        "material": {"fc": fc, "ft": fc / 20, "steel_yield": fy},
        "mesh": {"concrete_meshsize": meshsize/2, "steel_meshsize": meshsize/3, "plate_meshsize": meshsize},
    }

    task.set_parameters(parameters)
    controller.add_task(task)
    expand_index += 1

controller.run()
# controller.run_FEM_get_data()
# controller.run_FEM_get_data_plot()
# controller.run_get_fu_as_excel()
