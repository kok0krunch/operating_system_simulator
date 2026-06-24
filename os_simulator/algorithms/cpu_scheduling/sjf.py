# Shortest Job First (SJF) Scheduling Algorithm - Preemptive and Non-Preemptive
class Process_SJF:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.remaining_time = burst_time # For preemptive SJF, we need to keep track

    def calc_ct(self, prev_completion_time):
        if self.arrival_time > prev_completion_time:
            self.completion_time = self.arrival_time + self.burst_time
        else:
            self.completion_time = prev_completion_time + self.burst_time

    def calc_tat(self):
        return self.completion_time - self.arrival_time
    
    def execute(self):
        # Simulate the execution of the process
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            return True  # Process has completed execution
        return False  # Process is still running
    
    def calc_wt(self):
        return self.calc_tat() - self.burst_time
    
    def sjf_sched_nonpre(processes: list):

        # Initialize a list of completed processes
        completed_processes = []

        # time that has passed since the start of scheduling
        time = 0

        # Arrived processes that are ready to execute
        ready_processes = []
        
        # Protocol to handle the case when there are no ready processes at the current time
        if processes:
            # Sort processes by arrival time and then by burst time
            processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
            while not ready_processes:
                # Get the ready processes that have arrived by the current time
                for process in processes:
                    if process.arrival_time <= time and process not in ready_processes:
                        ready_processes.append(process)

                if not ready_processes:
                    time += 1
                    continue
        # else: no processes to schedule, return empty lists and average TAT of 0
        else:
            print("No processes to schedule.")
            return [], [], [], 0, 0  # No processes to schedule, return empty lists and average TAT and WT of 0

        current_process = ready_processes[0]  # The process with the earliest arrival time and shortest burst time
        while processes:
            
            # Get the next process to execute based on SJF
            while current_process.remaining_time > 0:
                # Check for newly arrived processes
                for process in processes:
                    if process.arrival_time <= time and process not in ready_processes:
                        ready_processes.append(process)
                
                # Increment time and decrement the remaining time of the current process
                time += 1

                # If current process is completed, sort ready processes by burst time, select next process,
                # remove current process from processes, and calculate completion time for current process
                if current_process.execute():
                    for process in processes:
                        if process.arrival_time <= time and process not in ready_processes:
                            ready_processes.append(process)
                    ready_processes.sort(key=lambda x: x.burst_time)  # Sort ready processes by burst time
                    current_process.calc_ct(prev_completion_time=time)  # Calculate completion time for current process
                    completed_processes.append(current_process) # Add current process to completed processes
                    # If current process is in ready processes, remove it from ready processes
                    if current_process in ready_processes:
                        ready_processes.remove(current_process)  # Remove current process from ready processes
                    processes.remove(current_process)
                    current_process = ready_processes[0] if ready_processes else None  # Select the next process to execute
                    break  # Break out of the loop
                else:
                    # If current process is not completed, continue executing it
                    continue

        # Calculate Turnaround Time (TAT) for each process
        tat_list = [process.calc_tat() for process in completed_processes]

        # Calculate average TAT
        avg_tat = sum(tat_list) / len(tat_list)

        # Calculate Waiting Time (WT) for each process
        wt_list = [process.calc_wt() for process in completed_processes]

        # Calculate average WT
        avg_wt = sum(wt_list) / len(wt_list)
        
        return completed_processes, tat_list, wt_list, avg_tat, avg_wt
    
    def sjf_sched_pre(processes: list):
        # Sort processes by arrival time and then by burst time
        processes.sort(key=lambda x: (x.arrival_time, x.burst_time))

        # Initialize a list of completed processes
        completed_processes = []

        # time that has passed since the start of scheduling
        time = 0
        
        # Arrived processes that are ready to execute
        ready_processes = []

        # Protocol to handle the case when there are no ready processes at the current time
        if processes: 
            while not ready_processes:
                # Get the ready processes that have arrived by the current time
                for process in processes:
                    if process.arrival_time <= time and process not in ready_processes:
                        ready_processes.append(process)

                if not ready_processes:
                    time += 1
                    continue
        else: 
            print("No processes to schedule.")
            return [], [], [], 0, 0  # No processes to schedule, return empty lists and average TAT and WT of 0


        current_process = ready_processes[0]  # The process with the earliest arrival time and shortest burst time

        while processes:
            
            # Get the next process to execute based on SJF
            while current_process.remaining_time > 0:
                # Check for newly arrived processes
                for process in processes:
                    if process.arrival_time <= time and process not in ready_processes:
                        ready_processes.append(process)
                        ready_processes.sort(key=lambda x: x.burst_time)  # Sort ready processes by burst time
                    if process in ready_processes and process.remaining_time < current_process.remaining_time:
                        current_process = process  # Preempt current process if a shorter job arrives
                        # If a new process arrives with equal remaining time, we will not preempt the current process, 
                        # as it is already executing and has the same remaining time as the new process. 
                        # This is a common tie-breaking rule in SJF scheduling to avoid unnecessary context switches when two processes have the same remaining time. 
                        # We will continue executing the current process until it completes or a new process arrives with a shorter remaining time.
                
                # Increment time and decrement the remaining time of the current process
                time += 1

                # If current process is completed, sort ready processes by burst time, select next process,
                # remove current process from processes, and calculate completion time for current process
                if current_process.execute():
                    ready_processes.sort(key=lambda x: x.burst_time)  # Sort ready processes by burst time
                    current_process.calc_ct(prev_completion_time=time)  # Calculate completion time for current process
                    completed_processes.append(current_process) # Add current process to completed processes
                    # If current process is in ready processes, remove it from ready processes
                    if current_process in ready_processes:
                        ready_processes.remove(current_process)  # Remove current process from ready processes
                    processes.remove(current_process)
                    current_process = ready_processes[0] if ready_processes else None  # Select the next process to execute
                    break  # Break out of the loop
                else:
                    # If current process is not completed, continue executing it
                    # But first, check if any new process has arrived that has a shorter remaining time than the current process
                    if ready_processes:
                        for process in ready_processes:
                            if process.remaining_time < current_process.remaining_time:
                                current_process = process  # Preempt current process if a shorter job arrives
                                continue  # Continue to next iteration to check for newly arrived processes and execute the new current process
                            else:
                                continue

        # Calculate Turnaround Time (TAT) for each process
        tat_list = [process.calc_tat() for process in completed_processes]

        # Calculate average TAT
        avg_tat = sum(tat_list) / len(tat_list)

        # Calculate Waiting Time (WT) for each process
        wt_list = [process.calc_wt() for process in completed_processes]

        # Calculate average WT
        avg_wt = sum(wt_list) / len(wt_list)

        return completed_processes, tat_list, wt_list, avg_tat, avg_wt