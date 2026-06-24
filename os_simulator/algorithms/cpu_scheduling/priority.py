# Priority Scheduling Algorithm - Preemptive and Non-Preemptive
class Process_prio:
    # Initialize the process with name, arrival time, burst time, priority, completion time, and remaining time
    def __init__(self, name, arrival_time, burst_time, priority):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.completion_time = 0
        # This is for preemptive priority scheduling
        self.remaining_time = burst_time

    # Calculate the completion time of the process based on the previous completion time
    def calc_ct(self, prev_completion_time):
        if self.arrival_time > prev_completion_time:
            self.completion_time = self.arrival_time + self.burst_time
        else:
            self.completion_time = prev_completion_time + self.burst_time

    # Calculate the turnaround time of the process
    def calc_tat(self):
        return self.completion_time - self.arrival_time

    # Calculate the waiting time of the process
    def calc_wt(self):
        return self.calc_tat() - self.burst_time
    
    # Simulate the execution of the process, if remaining time not 0, return False and continue execution
    def execute(self):
        # Simulate the execution of the process
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            return True  # Process has completed execution
        return False  # Process is still running
    
    def prio_sched_nonpre(processes: list):
        # Sort processes by arrival time and then by priority
        processes.sort(key=lambda x: (x.arrival_time, x.priority))
        
        # Initialize a time variable to keep track of the current time since the start of scheduling
        time = 0

        # Initialize a list of completed processes
        completed_processes = []

        # Arrived processes that are ready to execute
        ready_processes = []

        while processes:

            # Get the ready processes that have arrived by the current time
            for process in processes:
                if process.arrival_time <= time and process not in ready_processes:
                    ready_processes.append(process)

            # If there are no ready processes at time, increment time and continue to the next iteration
            if not ready_processes:
                time += 1
                continue

            # Sort ready processes by priority (lower number indicates higher priority)
            ready_processes.sort(key=lambda x: x.priority)

            current_process = ready_processes[0]  # The process with the earliest arrival time and highest priority

            # Execute the current process until it completes
            while current_process.remaining_time > 0:
                time += 1  # Increment time
                # Sort ready processes by priority (lower number indicates higher priority)
                ready_processes.sort(key=lambda x: x.priority)

                if current_process.execute():  # Execute the current process
                    current_process.calc_ct(prev_completion_time=time)  # Calculate completion time for current process
                    completed_processes.append(current_process)  # Add current process to completed processes
                    if current_process in ready_processes:
                        ready_processes.remove(current_process)  # Remove current process from ready processes
                    processes.remove(current_process)  # Remove current process from processes
                    current_process = ready_processes[0] if ready_processes else None  # Select the next process to execute
                    break  # Exit the loop to select the next process

        # Calculate Turnaround Time (TAT) for each process
        tat_list = [process.calc_tat() for process in completed_processes]

        # Calculate average TAT
        avg_tat = sum(tat_list) / len(tat_list)

        # Calculate Waiting Time (WT) for each process
        wt_list = [process.calc_wt() for process in completed_processes]

        # Calculate average WT
        avg_wt = sum(wt_list) / len(wt_list)

        return completed_processes, tat_list, wt_list, avg_tat, avg_wt
    
    def prio_sched_pre(processes: list):
        # Initialize a time variable to keep track of the current time since the start of scheduling
        time = 0 

        # Initialize a list of completed processes
        completed_processes = []   

        # Initialize a list of ready processes that have arrived and are ready to execute
        ready_processes = []

        # Initialize a boolean whether to preempt or not, if a higher priority process arrives
        preempt = False

        # Protocol for case of no processes to schedule, return empty lists and average TAT and WT of 0
        if processes:
            processes.sort(key=lambda x: (x.arrival_time, x.priority))
            while not ready_processes:
                for process in processes:
                    if process.arrival_time <= time and process not in ready_processes:
                        ready_processes.append(process)
                    if not ready_processes:
                        time += 1
                        continue
        else:
            print("No processes to schedule.")
            return [], [], [], 0, 0  # No processes to schedule, return empty lists and average TAT and WT of 0
        
        current_process = ready_processes[0]  # The process with the earliest arrival time and highest priority

        while processes:
            # Get the ready processes that have arrived by the current time
            for process in processes:
                if process.arrival_time <= time and process not in ready_processes:
                    ready_processes.append(process)
                    ready_processes.sort(key=lambda x: x.priority)  # Sort ready processes by priority (lower number indicates higher priority)
                    # If a new process arrives with higher priority than the current process, preempt the current process
                    if process.priority < current_process.priority and current_process in ready_processes:
                        current_process = process  # Preempt current process if a higher priority job arrives
                        continue
            
            # If there are no ready processes at time, increment time and continue to the next iteration
            if not ready_processes:
                time += 1
                continue

            # Execute the current process until it completes
            while current_process.remaining_time > 0:
                time += 1  # Increment time
                # Execute the current process
                if current_process.execute():
                    current_process.calc_ct(prev_completion_time=time)  # Calculate completion time for current process
                    completed_processes.append(current_process)  # Add current process to completed processes
                    if current_process in ready_processes:
                        ready_processes.remove(current_process)  # Remove current process from ready processes
                    processes.remove(current_process)  # Remove current process from processes
                else: 
                    # Get the ready processes that have arrived by the current time
                    for process in processes:
                        if process.arrival_time <= time and process not in ready_processes:
                            ready_processes.append(process)
                            ready_processes.sort(key=lambda x: x.priority)  # Sort ready processes by priority (lower number indicates higher priority)
                        # If a new process arrives with higher priority than the current process, preempt the current process
                        if process.priority < current_process.priority and current_process in ready_processes:
                            current_process = process  # Preempt current process if a higher priority job arrives
                            preempt = True
                            continue  # continue the for loop to select the next process

                    # If preempt is True, break the while loop to select the next process
                    if preempt:
                        preempt = False
                        break  # Exit the loop to select the next process

                    continue # Continue iterating if preemption is not required and the current process is still executing
        
        # Calculate Turnaround Time (TAT) for each process
        tat_list = [process.calc_tat() for process in completed_processes]

        # Calculate average TAT
        avg_tat = sum(tat_list) / len(tat_list)

        # Calculate Waiting Time (WT) for each process
        wt_list = [process.calc_wt() for process in completed_processes]

        # Calculate average WT
        avg_wt = sum(wt_list) / len(wt_list)

        return completed_processes, tat_list, wt_list, avg_tat, avg_wt
                    
    
