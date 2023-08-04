from control import Controller
from tasks.TaskBendingCircle import TaskImplement as TaskImplement_CircleBending
from tasks.TaskbendingRect import TaskImplement as TaskImplement_RectBending
import pandas as pd
import os

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

length = 1500

for meshsize in [81,54,36,27,18,9,6]:
    for section_type, section_height, section_width, thickness, fy, fc in zip(section_type_series, section_height_series,
                                                                          section_width_series, thickness_series,
                                                                          fy_series, fc_series):
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
            "task_work_dir": os.path.join(CWD, 'run_files_meshsize_analysis2', "bending", f"meshsize_{meshsize}"),
            "controller_work_dir": CWD,
            "geometry": geometry,
            "load_support_location": {
                "support": 100 / (length + 200),
                "load": (100 + length / 3) / (length + 200),
            },
            "load_displacement_target": length / 40,
            "material": {"fc": fc, "ft": fc / 20, "steel_yield": fy},
            "mesh": {"concrete_meshsize": meshsize, "steel_meshsize": meshsize/2, "plate_meshsize": meshsize},
        }
        task.set_parameters(parameters)
        controller.add_task(task)

controller.run()
controller.run_FEM_get_data()
controller.run_FEM_get_data_plot()
controller.run_get_fu_as_excel()
