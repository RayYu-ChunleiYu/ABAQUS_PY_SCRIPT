import os
import pandas as pd
import matplotlib.pyplot as plt

CWD = os.getcwd()

exp_data_path = os.path.join(CWD, 'exp_verified', 'data.xlsx')
exp_data_all = pd.read_excel(exp_data_path, sheet_name='Strength')

#


output_data_path = os.path.join("data_sheet",'exp_verified')
exp_verify_files_path = os.path.join(CWD,'run_files_exp_verify')

exp_tick_list = ["Short_column_under_axial_compression","Short_column_under_axial_tension","Short_column_under_eccentric_compression"]
fem_tick_list = ["axialCompression","axialTension","eccentricCompression"]


for exp_tick,fem_tick in zip(exp_tick_list,fem_tick_list):
    print(f"-------------------{exp_tick}--------------------")
    exp_data = exp_data_all[exp_data_all['Load_pattern'] == exp_tick]
    print(exp_data)
    fem_data = pd.read_excel(os.path.join(exp_verify_files_path,fem_tick,'final_data.xlsx'))

    if exp_tick == "Short_column_under_axial_compression":
        fem_data['No'] = [i.split("_")[0] for i in fem_data['specimen_name']]
    else:
        fem_data['No'] = fem_data['specimen_name']
    print(fem_data)

    concat_dataframe = pd.merge(exp_data, fem_data, on='No')
    if "tension" in exp_tick:
        interpolate_force = concat_dataframe['interpolate force'] / 1000
    else:
        interpolate_force = -concat_dataframe['interpolate force'] / 1000
    print(concat_dataframe['Nu_kN'])
    plt.scatter(concat_dataframe['Nu_kN'], interpolate_force)
    plt.xlim((0,concat_dataframe['Nu_kN'].max()*1.2))
    plt.ylim((0,concat_dataframe['Nu_kN'].max()*1.2))
    plt.plot([0,concat_dataframe['Nu_kN'].max()*1.2],[0,concat_dataframe['Nu_kN'].max()*1.2])
    plt.plot([0,concat_dataframe['Nu_kN'].max()*1.2],[0,concat_dataframe['Nu_kN'].max()*1.2*0.8])
    plt.xlabel("exp")
    plt.ylabel("fem")
    plt.savefig(os.path.join(output_data_path,f'{fem_tick}.png'),dpi=600)
    plt.cla()
    concat_dataframe.to_excel(os.path.join(output_data_path,f"{fem_tick}.xlsx"))


exp_data = exp_data_all[exp_data_all['Load_pattern'] == "Pure_bending"]

print(exp_data)
fem_data = pd.read_excel(os.path.join(exp_verify_files_path,"bending",'final_data.xlsx'))

fem_data['No'] = [i.split("_")[0] for i in fem_data['specimen_name']]
print(fem_data)

concat_dataframe = pd.merge(exp_data, fem_data, on='No')
print(concat_dataframe)
interpolate_moment= -concat_dataframe['moment_1_interpolate']
print(concat_dataframe['Nu_kN'])
plt.scatter(concat_dataframe['Nu_kN'], interpolate_moment)
plt.xlim((0,concat_dataframe['Nu_kN'].max()*1.2))
plt.ylim((0,concat_dataframe['Nu_kN'].max()*1.2))
plt.plot([0,concat_dataframe['Nu_kN'].max()*1.2],[0,concat_dataframe['Nu_kN'].max()*1.2])
plt.plot([0,concat_dataframe['Nu_kN'].max()*1.2],[0,concat_dataframe['Nu_kN'].max()*1.2*0.8])
plt.xlabel("exp")
plt.ylabel("fem")
plt.savefig(os.path.join(output_data_path,f'{"bending"}.png'),dpi=600)
plt.cla()
concat_dataframe.to_excel(os.path.join(output_data_path,f"bending.xlsx"))



