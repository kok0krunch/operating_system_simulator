# First-Fit Memory Management Algorithm

class FirstFit:
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
        print("\nMFT Allocation Simulation\n")
        partition_occupied = [False] * len(self.memory_size)
        
        for job in self.jobs:
            allocated = False
            for index, part_size in enumerate(self.memory_size):
                if part_size >= job["size"] and not partition_occupied[index]:
                    internal_frag = part_size - job["size"]
                    job["allocated_partition"] = f"Partition {index + 1} ({part_size})"
                    job["fragmentation"] = internal_frag
                    partition_occupied[index] = True
                    allocated = True
                    print(f"{job['process_id']} (Size {job['size']}) allocated to Partition {index + 1} (Size {part_size}). Fragmentation: {internal_frag}")
                    break  # Stop searching for this job; move to the next one
        
            if not allocated:
                job["allocated_partition"] = "Wait / Unallocated"
                job["fragmentation"] = "N/A"
                print(f"{job['process_id']} (Size {job['size']}) must WAIT. No matching free partition available.")

        print("\n" + "="*60)
        print(f"{'Job ID':<10}{'Size':<10}{'Burst':<10}{'Allocated To':<22}{'Frag':<10}")
        print("="*60)
        for job in self.jobs:
            print(f"{job['process_id']:<10}{job['size']:<10}{job['burst_time']:<10}{str(job['allocated_partition']):<22}{str(job['fragmentation']):<10}")
        print("="*60)


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


    def mvt_logic(self):
        print("\nMVT Allocation Simulation\n")
        total_memory_capacity = self.memory_size
        memory_map = [[0, total_memory_capacity, "FREE"]]
        for job in self.jobs:
            allocated = False
            for index, block in enumerate(memory_map):
                start_address, block_size, status = block
                if status == "FREE" and block_size >= job["size"]:
                    # Update job data
                    job["allocated_partition"] = f"Address {start_address}"
                    job["fragmentation"] = 0
                    memory_map[index] = [start_address, job["size"], job["process_id"]]
                    leftover_space = block_size - job["size"]

                    if leftover_space > 0:
                        new_free_start = start_address + job["size"]
                        memory_map.insert(index + 1, [new_free_start, leftover_space, "FREE"])

                    allocated = True
                    print(f" {job['process_id']} allocated at Address {start_address} (Carved {job['size']} KB)")
                    break  # Allocation complete for this job; move to the next one
            
            if not allocated:
                job["allocated_partition"] = "Wait (External Frag)"
                job["fragmentation"] = "N/A"
                print(f" {job['process_id']} (Size {job['size']}) must WAIT. No single free block is big enough.")


        print("\n" + "="*60)
        print(f"{'Job ID':<10}{'Size':<10}{'Burst':<10}{'Allocated To':<22}{'Internal Frag':<10}")
        print("="*60)
        for job in self.jobs:
            print(f"{job['process_id']:<10}{job['size']:<10}{job['burst_time']:<10}{str(job['allocated_partition']):<22}{str(job['fragmentation']):<10}")
        print("="*60)

# definitions
def user_input(first_fit):
    while True:
        try:
            memory_type_input=input("Enter memory type (MFT/MVT):").strip()
            if memory_type_input.upper()=="MFT":
                first_fit.mft_settings()
            elif memory_type_input.upper()=="MVT":
                first_fit.mvt_settings()
            else:
                raise ValueError

        except:
            print("Invalid input. Please enter 'MFT' or 'MVT'")
            continue

# main program
if __name__ == "__main__":
    first_fit = FirstFit()
    print("Welcome to the First-Fit Memory Management Algorithm Simulator!")
    user_input(first_fit)