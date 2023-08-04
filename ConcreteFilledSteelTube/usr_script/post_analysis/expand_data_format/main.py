"""Process expand specimen and format the data to excel"""

import pandas as pd
import os

CWD = os.getcwd()
data_expand_path = os.path.join(CWD,"run_files_expand")
def parse_calculation_excel_to_format_dataframe(loading_condition:str):
    """
    Parse calculation excel to format dataframe.
    Basic parameters: Section_type,diameter,section_height,section_width,tube_thickness,height,fy,fck,e,length

    Args:
        loading_condition: The loading condition

    Returns:
        A dataframe that reformed

    """

    calculation_dataframe = pd.read_excel(os.path.join(data_expand_path,loading_condition,'final_data.xlsx'))
    section_series = []
    for i in calculation_dataframe['diameter']:
        if pd.isna(i):
            section_series.append('Rectangle')
        else:
            section_series.append('Circle')

    basic_parameters_list = ["specimen_name",'diameter', 'section_height', 'section_width','thickness','height','fy','fc','interpolate force','interpolate displacement',"interpolate strain"]
    if loading_condition == "eccentricCompression":
        basic_parameters_list.append('e')
    elif loading_condition == "bending":
        basic_parameters_list[8] = 'moment_1_interpolate'
    basic_parameter_dataframe = calculation_dataframe[basic_parameters_list]
    basic_parameter_dataframe.insert(1,'section_type',section_series)
    basic_parameter_dataframe.to_excel(os.path.join(CWD,"data_sheet","data_expand",f'{loading_condition}.xlsx'),index=False)


parse_calculation_excel_to_format_dataframe('axialCompression')

parse_calculation_excel_to_format_dataframe('eccentricCompression')

parse_calculation_excel_to_format_dataframe('axialTension')

parse_calculation_excel_to_format_dataframe('bending')

# Hybrid


# parameters: Section_shape_factor, height
# to
# width
# ratio, confining
# factor

