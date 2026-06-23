# Worst-Fit Memory Management Algorithm

class WorstFit:
    def __init__(self):
        self.memory_size = None
        self.jobs=[]


    def add_process(self, process_size_input, burst_time_input):
        process_number = len(self.jobs) + 1
        process_data = {
                        "process_id": f"P{process_number}",
                        "size": int(process_size_input),
                        "burst_time": int(burst_time_input),
                        "allocated_partition": None,
                        "fragmentation": 0}
        
        self.jobs.append(process_data)

    def first_fit_settings(self):
         while True:
            try:
                memory_size_input = input("Enter total memory block size: ").strip()
                if int(memory_size_input) <= 0:
                    raise ValueError
                
                else:
                    self.memory_size=int(memory_size_input)
                    break
            except:
                print("Memory size should only be positive integers. Please input a valid number.")
        
         while True:
            try:
                process_size_input= input("enter process size: ").strip()
                burst_time_input= input("enter burst time: ").strip()

                if int(process_size_input) > 0 and int(burst_time_input) > 0:
                    self.add_process(process_size_input, burst_time_input)
                    
                elif int(process_size_input) <= 0 or int(burst_time_input) <= 0:
                    raise ValueError
                
            except:
                print("Process size and burst time should be positive integers. Please input valid numbers.")  


    def first_fit_logic(self, compaction_enabled=False):
        pass

# main program
if __name__ == "__main__":
    worst_fit = WorstFit()
    worst_fit.mvt_settings()