class BestAvailableFit:
    def __init__(self):
        self.memory_size = None
        self.jobs=[]
        self.partition_busy = None

    def add_process(self, process_size_input, burst_time_input):
        process_number = len(self.jobs) + 1
        process_data = {
                        "process_id": f"P{process_number}",
                        "size": int(process_size_input),
                        "burst_time": int(burst_time_input),
                        "allocated_partition": None,
                        "fragmentation": 0}
        
        self.jobs.append(process_data)

    def best_available_fit_settings(self):
        if self.memory_size is None:
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
    

    def best_available_fit_logic(self):
        mft_partitions = list(self.memory_size)
        partition_count = len(mft_partitions)
        if self.partition_busy is None:
            self.partition_busy = [False] * partition_count

        for job_item in self.jobs:
            if job_item["allocated_partition"] is not None:
                continue

            optimal_index = -1
            for block_index in range(partition_count):
                if mft_partitions[block_index] >= job_item["size"] and not self.partition_busy[block_index]:
                    if optimal_index == -1 or mft_partitions[block_index] < mft_partitions[optimal_index]:
                        optimal_index = block_index
            
            if optimal_index != -1:
                job_item["allocated_partition"] = optimal_index + 1
                job_item["fragmentation"] = mft_partitions[optimal_index] - job_item["size"]
                self.partition_busy[optimal_index] = True
            
            else:
                available_swap_index = -1
                for block_index in range(partition_count):
                    if mft_partitions[block_index] >= job_item["size"]:
                        if available_swap_index == -1 or mft_partitions[block_index] < mft_partitions[available_swap_index]:
                            available_swap_index = block_index
                
                if available_swap_index != -1:
                    for old_job in self.jobs:
                        if old_job["allocated_partition"] == available_swap_index + 1:
                            old_job["allocated_partition"] = "Swapped Out / Suspended"
                            old_job["fragmentation"] = 0
                    
                    print(f"\n[!] Partition {available_swap_index + 1} is busy. Swapping out old process to make it AVAILABLE for {job_item['process_id']}.")
                    job_item["allocated_partition"] = available_swap_index + 1
                    job_item["fragmentation"] = mft_partitions[available_swap_index] - job_item["size"]
                    self.partition_busy[available_swap_index] = True
                else:
                    job_item["allocated_partition"] = "Not Allocated (Too Large)"

if __name__ == "__main__":
    best_available_fit = BestAvailableFit()
    print("Welcome to the Best-Available-Fit Memory Management Algorithm Simulator!")
   
    while True:
        best_available_fit. best_available_fit_settings()
        best_available_fit.best_available_fit_logic()