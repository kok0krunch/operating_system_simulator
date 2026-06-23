class BestAvailableFit:
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


    def mft_settings(self):
        while True:
            try:
                memory_size_input = input("Enter partitions separated with comma (ex. 1,2,3): ").strip()
                memory_size_list = [int(size.strip()) for size in memory_size_input.split(',')]
                for size in memory_size_list:
                    if int(size) <= 0:
                        raise ValueError
                    
                self.memory_size=memory_size_list
                break

            except:
                print("Memory sizes should only be positive integers. Voiding initial inputs")


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
    

    def mft_logic(self):
        pass

    def mvt_settings(self):
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


    def mvt_logic(self, compaction_enabled=False):
        pass
    
# definitions
def user_input(best_available_fit):
    while True:
        try:
            memory_type_input=input("Enter memory type (MFT/MVT):").strip()
            if memory_type_input.upper()=="MFT":
                best_available_fit.mft_settings()
            elif memory_type_input.upper()=="MVT":
                best_available_fit.mvt_settings()
            else:
                raise ValueError

        except:
            print("Invalid input. Please enter 'MFT' or 'MVT'")
            continue

# main program
if __name__ == "__main__":
    best_available_fit = BestAvailableFit()
    print("Welcome to the Best-Available-Fit Memory Management Algorithm Simulator!")
    user_input(best_available_fit)