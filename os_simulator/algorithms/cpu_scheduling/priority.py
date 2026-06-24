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
    
