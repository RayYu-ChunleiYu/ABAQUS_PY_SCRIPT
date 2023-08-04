import pandas as pd
import os
import matplotlib.pyplot as plt


def data_contraction(loading_condition: str, output_path: str, is_plot: bool = False):
    meshsize_analysis_path = os.path.join(CWD, 'run_files_meshsize_analysis3', loading_condition)

    dir_list = os.listdir(meshsize_analysis_path)

    current_dataframe = pd.DataFrame()

    if is_plot:
        plot_x = []
        plot_y = []
        legend_list = []

    for tension_dir in dir_list:
        if os.path.isdir(os.path.join(meshsize_analysis_path, tension_dir)):
            meshsize_str = tension_dir.split('_')[1]
            excel_path = os.path.join(meshsize_analysis_path, tension_dir, 'data.xlsx')
            fem_result = pd.read_excel(excel_path)
            fem_result_curve = fem_result[['displacement', 'force']].copy()
            fem_result_curve.columns = [f"displacement_{meshsize_str}", f"force_{meshsize_str}"]
            current_dataframe = pd.concat((current_dataframe, fem_result_curve), axis=1)
            if is_plot:
                plot_x.append(fem_result_curve.iloc[:, 0])
                plot_y.append(fem_result_curve.iloc[:, 1])
                legend_list.append(f"meshsize:{meshsize_str}")
    current_dataframe.to_excel(os.path.join(output_path, f'{loading_condition}.xlsx'))

    if is_plot:
        for x, y, legend in zip(plot_x, plot_y, legend_list):
            plt.plot(x, y, label=legend)

        plt.legend()
        plt.savefig(os.path.join(output_path, f'{loading_condition}.png'),dpi=600)
        plt.cla()


CWD = os.getcwd()

# # compression
# data_contraction('compression', os.path.join(CWD, 'data_sheet', 'meshsize'),is_plot=True)
#
# # tension
# data_contraction('tension', os.path.join(CWD, 'data_sheet', 'meshsize'),is_plot=True)

data_contraction('eccentric_compression', os.path.join(CWD, 'data_sheet', 'meshsize'),is_plot=True)

#
# # bending
# data_contraction('bending', os.path.join(CWD, 'data_sheet', 'meshsize'),is_plot=True)

# eccentric compression

