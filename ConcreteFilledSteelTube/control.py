import threading
from tasks.task import Task
from tqdm import tqdm



   
class Controller:
    def __init__(self,run_num_limit:int=1) -> None:
        self.task_pools:list[Task] = []
        self.thread_pools:list[threading.Thread] = []
        self.run_num_limit = run_num_limit
        
    def add_task(self, task):
        self.task_pools.append(task)
        thread =  threading.Thread(target=task.run)
        self.thread_pools.append(thread)
        
        
    def run(self):
        thread_pool = []
        for task in self.task_pools:
            thread_pool.append(threading.Thread(target=task.run))
            thread_pool.append(threading.Thread(target=task.run_fem_get_data))
        thread_run_with_limit_num(thread_pool,self.run_num_limit)
        self.run_FEM_get_data_plot()

    def run_FEM_calculation(self):
        thread_pool = [threading.Thread(target=task.run_fem_calculation) for task in self.task_pools]
        thread_run_with_limit_num(thread_pool,self.run_num_limit)
        
    def run_FEM_get_data(self):
        thread_pool = [threading.Thread(target=task.run_fem_get_data) for task in self.task_pools]
        thread_run_with_limit_num(thread_pool,self.run_num_limit)
        
    def run_FEM_get_data_plot(self,show=False):
        for task in tqdm(self.task_pools):
            task.run_fem_get_data_plot(show)
            
    def run_get_fu_as_excel(self):
        # thread_pool = [threading.Thread(target=task.get_fu_as_excel) for task in self.task_pools]
        self.task_pools[0].get_fu_as_excel()
        # thread_run_with_limit_num(thread_pool,self.run_num_limit)
        
        
          
def thread_run_with_limit_num(thread_pool:list[threading.Thread], run_num_limit:int):
    current_task_index = 0
    thread_num = len(thread_pool)
    
    with tqdm(total=thread_num) as pbar:
        while True:
            if current_task_index + run_num_limit <= thread_num:
                for i in range(run_num_limit):
                    thread_pool[current_task_index+i].daemon=True
                    thread_pool[current_task_index+i].start()
                for i in range(run_num_limit):
                    thread_pool[current_task_index+i].join()
                current_task_index += run_num_limit
            else:
                for i in range(thread_num - current_task_index):
                    thread_pool[current_task_index+i].start()
                for i in range(thread_num - current_task_index):
                    thread_pool[current_task_index+i].join()
                current_task_index = thread_num
                break
            pbar.update(run_num_limit)

        
            
            
            
        

# # subprocess test 
# CWD = os.getcwd()
# print(CWD)
# a = subprocess.call("abq2022 cae noGUI=get_curve_from_odb.py",shell=True,cwd=os.path.join(CWD,"subporcessTest"))
# print(a)


# # task test 
# CWD = os.getcwd()

# task = Task()
# parameters = {
#     "model_name" : "test_analysis",
#     "task_work_dir" : os.path.join(CWD,"taskTest"),
#     "controller_work_dir" : CWD,
#     "geometry" : {
#         'section_type': 'Circle',
#         "diameter":108.0,
#         "tube_thickness":8.0,
#         },
#     "material" : {"fc":140.0,"ft":10.0,"steel_yield":420.0},
#     "mesh" : {"concrete_meshsize":18,"steel_meshsize":18,"plate_meshsize":18},
    
# }
# task.set_parameters(parameters)
# task.run()