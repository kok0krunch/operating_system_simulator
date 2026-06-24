# First-Come, First-Served (FCFS) CPU Scheduling Algorithm

class Process_FCFS:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0

    def calc_ct(self, prev_completion_time):
        if self.arrival_time > prev_completion_time:
            self.completion_time = self.arrival_time + self.burst_time
        else:
            self.completion_time = prev_completion_time + self.burst_time
    
    def calc_tat(self):
        return self.completion_time - self.arrival_time
    
    def calc_wt(self):
        return self.calc_tat() - self.burst_time
    
    def fcfs_scheduling(processes):
        # Sort processes by arrival time, check if there are any processes to schedule
        if processes:
            processes.sort(key=lambda x: x.arrival_time)
        else: 
            print("No processes to schedule.")
            return [], [], [], 0, 0  # No processes to schedule, return empty lists and average TAT and WT of 0
        
        prev_completion_time = 0
        for process in processes:
            prev_completion_time += process.burst_time
            process.calc_ct(prev_completion_time)
            prev_completion_time = process.completion_time
        
        # Calculate Turnaround Time (TAT) for each process
        tat_list = [process.calc_tat() for process in processes]

        # Calculate average TAT
        avg_tat = sum(tat_list) / len(tat_list)

        # Calculate Waiting Time (WT) for each process
        wt_list = [process.calc_wt() for process in processes]

        # Calculate average WT
        avg_wt = sum(wt_list) / len(wt_list)
        
        return processes, tat_list, wt_list, avg_tat, avg_wt