import subprocess
import os
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from .Task import Task
import json
import scipy


class TaskAxialLoading(Task):

    def copy_material_file(self):
        controller_work_directory = self.parameters['controller_work_dir']
        task_work_directory = self.parameters['task_work_dir']
        print("copy material file")
        subprocess.call("copy {} {}".format(os.path.join(controller_work_directory, "materials", 'materials.py'),
                                            os.path.join(controller_work_directory, task_work_directory)), shell=True)
        subprocess.call("copy {} {}".format(os.path.join(controller_work_directory, "materials", 'UHPCCAConstitute.py'),
                                            os.path.join(controller_work_directory, task_work_directory)), shell=True)
        print("copy material file done")

    def script_read(self):
        pass

    def script_store(self):
        controller_work_directory = self.parameters['controller_work_dir']

        task_work_dir = self.parameters['task_work_dir']

        model_name = self.parameters['model_name']

        with open(os.path.join(controller_work_directory, task_work_dir, model_name + "_run.py"), "w") as f:
            f.write(self.script_FEM_run_string)

        with open(os.path.join(controller_work_directory, task_work_dir, model_name + "_getData.py"), "w") as f:
            f.write(self.script_FEM_get_data_string)

    def script_refactor_common(self):

        geometry = self.parameters['geometry']

        material = self.parameters['material']

        mesh = self.parameters['mesh']

        model_name = self.parameters['model_name']

        load_displacement_target = self.parameters['load_displacement_target']

        # run script 

        self.script_FEM_run_string = self.script_FEM_run_string.replace("thickness = 4.0", "thickness = {}".format(
            geometry['tube_thickness']))
        self.script_FEM_run_string = self.script_FEM_run_string.replace("load_displacement_target = height/10",
                                                                        "load_displacement_target = {}".format(
                                                                            load_displacement_target))

        ## material setting
        self.script_FEM_run_string = self.script_FEM_run_string.replace("fc = 120.0", "fc = {}".format(material['fc']))
        self.script_FEM_run_string = self.script_FEM_run_string.replace("ft = 7.0", "ft = {}".format(material['ft']))
        self.script_FEM_run_string = self.script_FEM_run_string.replace("steel_yield = 400.0",
                                                                        "steel_yield = {}".format(
                                                                            material['steel_yield']))

        ## mesh setting
        self.script_FEM_run_string = self.script_FEM_run_string.replace("concrete_meshsize = 9",
                                                                        "concrete_meshsize = {}".format(
                                                                            mesh['concrete_meshsize']))
        self.script_FEM_run_string = self.script_FEM_run_string.replace("steel_meshsize = 9",
                                                                        "steel_meshsize = {}".format(
                                                                            mesh['steel_meshsize']))
        self.script_FEM_run_string = self.script_FEM_run_string.replace("plate_meshsize = 9",
                                                                        "plate_meshsize = {}".format(
                                                                            mesh['plate_meshsize']))

        ## name setting
        self.script_FEM_run_string = self.script_FEM_run_string.replace("model_name = 'bending_analysis'",
                                                                        "model_name = '{}'".format(model_name))

        # get data script

        controller_work_directory = self.parameters['controller_work_dir']

        task_work_dir = self.parameters['task_work_dir']

        odb_path = os.path.join(controller_work_directory, task_work_dir, model_name + ".odb")
        self.script_FEM_get_data_string = self.script_FEM_get_data_string.replace(
            "o1 = session.openOdb(name=r'E:/YuChunlei/data_expand_FEM/bending_analysis.odb')",
            "o1 = session.openOdb(name=r'{}')".format(os.path.basename(odb_path))
        )
        self.script_FEM_get_data_string = self.script_FEM_get_data_string.replace(
            "odb = session.odbs[r'E:/YuChunlei/data_expand_FEM/bending_analysis.odb']",
            "odb = session.odbs[r'{}']".format(os.path.basename(odb_path))
        )

    def script_refactor_special(self):
        pass

    def script_refactor(self):
        self.script_read()
        self.script_refactor_common()
        self.script_refactor_special()
        self.script_store()

    def run_fem_get_data_plot(self, show: bool = False, capacity_point: int = None):
        controller_work_directory = self.parameters['controller_work_dir']
        task_work_directory = self.parameters['task_work_dir']
        dataframe = self.get_data_parse()
        dataframe.to_excel(os.path.join(controller_work_directory, task_work_directory, 'data.xlsx'))
        fig = plt.figure()
        ax1 = fig.subplots()
        ax2 = ax1.twinx()
        ax1.plot(dataframe['displacement'], dataframe['force'], label="curve")
        ax2.plot(dataframe['displacement'], dataframe['max_steel_strain'], label='max_steel_strain')
        ax2.plot(dataframe['displacement'], dataframe['min_steel_strain'], label='min_steel_strain')
        ax1.set_xlabel('displacement')
        ax1.set_ylabel('force')
        ax2.set_ylabel('steel_strain')
        plt.legend()
        plt.savefig(os.path.join(controller_work_directory, task_work_directory, 'curve.png'), dpi=600)
        if show:
            plt.show()
        plt.clf()

    def get_fu_as_excel(self):
        controller_work_directory = self.parameters['controller_work_dir']
        task_work_dir = self.parameters['task_work_dir']
        task_work_dir_abs = os.path.dirname(os.path.join(controller_work_directory, task_work_dir))
        dirs = os.listdir(task_work_dir_abs)
        final_dataframe = pd.DataFrame()
        for current_dir in dirs:
            dir_abs = os.path.join(task_work_dir_abs, current_dir)
            if os.path.isdir(dir_abs):
                specimen_name = os.path.basename(dir_abs)
                excel_path = os.path.join(task_work_dir_abs, current_dir, 'data.xlsx')
                parameter_path = os.path.join(task_work_dir_abs, current_dir, 'parameter.json')
                with open(parameter_path, 'r') as f:
                    parameters = json.load(f)
                current_data = pd.read_excel(excel_path)

                if 'diameter' in parameters['geometry']:
                    current_data.insert(0, 'diameter', parameters['geometry']['diameter'])
                else:
                    current_data.insert(0, 'section_height', parameters['geometry']['section_height'])
                    current_data.insert(0, 'section_width', parameters['geometry']['section_width'])
                current_data.insert(0, 'thickness', parameters['geometry']['tube_thickness'])
                current_data.insert(0, 'height', parameters['geometry']['height'])
                current_data.insert(0, "fc", parameters['material']['fc'])
                current_data.insert(0, "fy", parameters['material']['steel_yield'])
                current_data.insert(0, "specimen_name", specimen_name)

                max_steel_strain = current_data['max_steel_strain']
                min_steel_strain = current_data['min_steel_strain']
                # Bearing capacity definition:
                # Tension:5000, Compression:-5000

                tension_capacity_limit = 10000 / 1000000
                compression_capacity_limit = -5000 / 1000000

                find_steel_array_compression = abs(min_steel_strain - compression_capacity_limit)
                find_steel_array_tension = abs(max_steel_strain - tension_capacity_limit)

                compression_capacity_index = find_steel_array_compression.argmin()
                tension_capacity_index = find_steel_array_tension.argmin()

                if compression_capacity_index < tension_capacity_index:
                    if compression_capacity_index != 0:
                        target_index = compression_capacity_index
                        current_header = "min_steel_strain"
                        current_limit = compression_capacity_limit
                    else:
                        target_index = tension_capacity_index
                        current_header = "max_steel_strain"
                        current_limit = tension_capacity_limit
                else:
                    if tension_capacity_index != 0:
                        target_index = tension_capacity_index
                        current_header = "max_steel_strain"
                        current_limit = tension_capacity_limit
                    else:
                        target_index = compression_capacity_index
                        current_header = "min_steel_strain"
                        current_limit = compression_capacity_limit

                interpolate_strain = current_data[current_header][target_index - 1:target_index + 2]
                interpolate_force = current_data['force'][target_index - 1:target_index + 2]
                interpolate_displacement = current_data['displacement'][target_index - 1:target_index + 2]

                compression_flag = False
                if current_limit < 0:
                    interpolate_displacement = -interpolate_displacement
                    interpolate_force = -interpolate_force
                    interpolate_strain = -interpolate_strain
                    current_limit = -current_limit
                    compression_flag = True

                force = np.interp(current_limit, interpolate_strain, interpolate_force)
                displacement = np.interp(current_limit, interpolate_strain, interpolate_displacement)
                strain = np.interp(current_limit, interpolate_strain, interpolate_strain)

                if compression_flag:
                    force = -force
                    displacement = -displacement
                    strain = -strain

                target_data = current_data.iloc[target_index].copy()
                target_data.loc["interpolate force"] = force
                target_data.loc["interpolate displacement"] = displacement
                target_data.loc["interpolate strain"] = strain

                final_dataframe = pd.concat([final_dataframe, target_data], ignore_index=True, axis=1)
        final_dataframe = final_dataframe.T
        final_dataframe.to_excel(os.path.join(task_work_dir_abs, 'final_data.xlsx'), index=False)

    def get_data_parse(self):
        controller_work_directory = self.parameters['controller_work_dir']
        task_work_directory = self.parameters['task_work_dir']
        curve1_path = os.path.join(controller_work_directory, task_work_directory, 'curve.txt')
        max_steel_strain_path = os.path.join(controller_work_directory, task_work_directory, 'max_steel_strain.txt')
        min_steel_strain_path = os.path.join(controller_work_directory, task_work_directory, 'min_steel_strain.txt')
        with open(curve1_path, "r") as f:
            curve1_string = f.readlines()
        with open(max_steel_strain_path, "r") as f:
            max_steel_strain_string = f.readlines()
        with open(min_steel_strain_path, "r") as f:
            min_steel_strain_string = f.readlines()
        curve1_array = self.parse_string_to_array(curve1_string)
        max_steel_strain_array = self.parse_string_to_array(max_steel_strain_string)
        min_steel_strain_array = self.parse_string_to_array(min_steel_strain_string)

        curve_dataframe_dict = {
            "time": max_steel_strain_array[:, 0],
            "displacement": curve1_array[:, 0],
            "force": curve1_array[:, 1],
            "max_steel_strain": max_steel_strain_array[:, 1],
            "min_steel_strain": min_steel_strain_array[:, 1]

        }
        return pd.DataFrame(curve_dataframe_dict)

    def parse_string_to_array(self, string: list[str]):
        x = []
        y = []

        # find where data starts
        valid_data_index = 0
        single_line = string[valid_data_index]
        single_line = single_line.strip()
        single_line = single_line.split(" ")

        while single_line[0] != '0.':
            single_line = string[valid_data_index]
            single_line = single_line.strip()
            single_line = single_line.split(" ")
            valid_data_index += 1

        for single_line in string[valid_data_index + 1:]:
            single_line = single_line.strip()
            single_line = single_line.split(" ")
            if single_line[0] == '':
                break
            else:
                x.append(float(single_line[0]))
                y.append(float(single_line[-1]))
        return np.array([x, y]).T
