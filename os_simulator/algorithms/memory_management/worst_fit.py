# Worst-Fit Memory Management Algorithm

class WorstFit:
    def __init__(self):
        self.memory_size = None
        self.jobs=[]
        self.mvt_free_segments = None


    def add_process(self, process_size_input, burst_time_input):
        process_number = len(self.jobs) + 1
        process_data = {
                        "process_id": f"P{process_number}",
                        "size": int(process_size_input),
                        "burst_time": int(burst_time_input),
                        "allocated_partition": None,
                        "fragmentation": 0}
        
        self.jobs.append(process_data)

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
                    # FIX: Triggers calculation and output right after adding a process
                    self.first_fit_logic(compaction_enabled=True)
                    
                elif int(process_size_input) <= 0 or int(burst_time_input) <= 0:
                    raise ValueError
                
            except:
                print("Process size and burst time should be positive integers. Please input valid numbers.")  


    def first_fit_logic(self, compaction_enabled=False):
        if self.mvt_free_segments is None:
            self.mvt_free_segments = [[0, self.memory_size]]

        for dynamic_job in self.jobs:
            if dynamic_job["allocated_partition"] is not None:
                continue

            first_segment_pos = -1

            for seg_idx, target_segment in enumerate(self.mvt_free_segments):
                if target_segment[1] >= dynamic_job["size"]:
                    first_segment_pos = seg_idx
                    break
            
            if first_segment_pos == -1 and compaction_enabled:
                total_free_space = sum(segment[1] for segment in self.mvt_free_segments)
                if total_free_space >= dynamic_job["size"]:
                    print(f"\n[Compaction Triggered for {dynamic_job['process_id']}]")
                    used_space_boundary = self.memory_size - total_free_space
                    self.mvt_free_segments = [[used_space_boundary, total_free_space]]
                    first_segment_pos = 0

            if first_segment_pos != -1:
                matched_seg = self.mvt_free_segments[first_segment_pos]
                dynamic_job["allocated_partition"] = f"Address Range {matched_seg[0]} to {matched_seg[0] + dynamic_job['size']}"
                dynamic_job["fragmentation"] = 0
                
                if matched_seg[1] == dynamic_job["size"]:
                    self.mvt_free_segments.pop(first_segment_pos)
                else:
                    matched_seg[0] += dynamic_job["size"]
                    matched_seg[1] -= dynamic_job["size"]
                print(f"-> SUCCESS: {dynamic_job['process_id']} allocated!")
            else:
                dynamic_job["allocated_partition"] = "Not Allocated"
                print(f"-> FAILED: No continuous chunk is large enough for {dynamic_job['process_id']}.")

        print(f"Current Free Memory Segments: {self.mvt_free_segments}")

# main program
if __name__ == "__main__":
    worst_fit = WorstFit()
    worst_fit.mvt_settings()