# Best-Fit Memory Management Algorithm

class BestFit:
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
                process_size_input = input("enter process size: ").strip()
                burst_time_input = input("enter burst time: ").strip()

                if int(process_size_input) > 0 and int(burst_time_input) > 0:
                    self.add_process(process_size_input, burst_time_input)
                    
                elif int(process_size_input) <= 0 or int(burst_time_input) <= 0:
                    raise ValueError
                
            except:
                print("Process size and burst time should be positive integers. Please input valid numbers.")  
    

    def mft_logic(self):
        # Tracking variables using localized naming conventions matching the original scope
        mft_partitions = list(self.memory_size)
        partition_count = len(mft_partitions)
        partition_busy = [False] * partition_count

        for job_item in self.jobs:
            optimal_index = -1
            for block_index in range(partition_count):
                if mft_partitions[block_index] >= job_item["size"] and not partition_busy[block_index]:
                    if optimal_index == -1 or mft_partitions[block_index] < mft_partitions[optimal_index]:
                        optimal_index = block_index
            
            if optimal_index != -1:
                job_item["allocated_partition"] = optimal_index + 1
                job_item["fragmentation"] = mft_partitions[optimal_index] - job_item["size"]
                partition_busy[optimal_index] = True
            else:
                job_item["allocated_partition"] = "Not Allocated"

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
                process_size_input = input("enter process size: ").strip()
                burst_time_input = input("enter burst time: ").strip()

                if int(process_size_input) > 0 and int(burst_time_input) > 0:
                    self.add_process(process_size_input, burst_time_input)
                    
                elif int(process_size_input) <= 0 or int(burst_time_input) <= 0:
                    raise ValueError
                
            except:
                print("Process size and burst time should be positive integers. Please input valid numbers.")  


    def mvt_logic(self, compaction_enabled=False):
        # Free segments mapped tracking pairs: [start_address, remaining_capacity]
        mvt_free_segments = [[0, self.memory_size]]

        for dynamic_job in self.jobs:
            best_segment_pos = -1
            for seg_idx, target_segment in enumerate(mvt_free_segments):
                if target_segment[1] >= dynamic_job["size"]:
                    if best_segment_pos == -1 or target_segment[1] < mvt_free_segments[best_segment_pos][1]:
                        best_segment_pos = seg_idx
            
            # Compaction Implementation: If no single block fits, check if total space allows it
            if best_segment_pos == -1 and compaction_enabled:
                total_free_space = sum(segment[1] for segment in mvt_free_segments)
                if total_free_space >= dynamic_job["size"]:
                    print(f"\n[Compaction Triggered for {dynamic_job['process_id']}]")
                    
                    # Compute where the new unified block starts
                    used_space_boundary = self.memory_size - total_free_space
                    mvt_free_segments = [[used_space_boundary, total_free_space]]
                    
                    # The first index is now guaranteed to be the best-fitting unified partition
                    best_segment_pos = 0

            if best_segment_pos != -1:
                matched_seg = mvt_free_segments[best_segment_pos]
                dynamic_job["allocated_partition"] = f"Address Range {matched_seg[0]} to {matched_seg[0] + dynamic_job['size']}"
                dynamic_job["fragmentation"] = 0
                
                if matched_seg[1] == dynamic_job["size"]:
                    mvt_free_segments.pop(best_segment_pos)
                else:
                    matched_seg[0] += dynamic_job["size"] # Increment starting address
                    matched_seg[1] -= dynamic_job["size"] # Reduce chunk capacity 
            else:
                dynamic_job["allocated_partition"] = "Not Allocated"
# definitions
def user_input(best_fit):
    while True:
        try:
            memory_type_input=input("Enter memory type (MFT/MVT):").strip()
            if memory_type_input.upper()=="MFT":
                best_fit.mft_settings()
                best_fit.mft_logic()
            elif memory_type_input.upper()=="MVT":
                best_fit.mvt_settings()
                compact_choice = input("Enable compaction? (y/n): ").strip().lower()
                is_compact = True if compact_choice in ['y', 'yes'] else False
                best_fit.mvt_logic(compaction_enabled=is_compact) 
            else:
                raise ValueError

        except:
            print("Invalid input. Please enter 'MFT' or 'MVT'")
            continue

# main program
if __name__ == "__main__":
    best_fit = BestFit()
    print("Welcome to the Best-Fit Memory Management Algorithm Simulator!")
    user_input(best_fit)