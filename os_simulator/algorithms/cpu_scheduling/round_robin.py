# Round Robin Scheduling Algorithm

class Process_RR:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.remaining_time = burst_time

    def calc_ct(self, prev_completion_time):
        if self.arrival_time > prev_completion_time:
            self.completion_time = self.arrival_time + self.burst_time
        else:
            self.completion_time = prev_completion_time + self.burst_time

    def calc_tat(self):
        return self.completion_time - self.arrival_time

    def calc_wt(self):
        return self.calc_tat() - self.burst_time
    
    def execute(self, time_quantum):
        # Simulate the execution of the process for a given time quantum
        if self.remaining_time > time_quantum:
            self.remaining_time -= time_quantum
            return False  # Process is still running
        else:
            self.remaining_time = 0
            return True  # Process has completed execution
        
    def round_robin(processes: list, time_quantum: int):
        # Initialize a time variable to keep track of the current time
        time = 0

        # Sort processes by arrival time
        processes.sort(key=lambda x: x.arrival_time)

        # Initialize a list of completed processes
        completed_processes = []

        # Initialize a list of ready processes
        ready_processes = []
    
        # Initialize a comparer which determines whether an entire list of processes have the same arrival times 
        comparer = processes[0].arrival_time

        # Initialize boolean of same arrival times or not
        equal_arrivals = False

        for process in processes:
            if process.arrival_time == comparer:
                score += 1
            if score == len(processes):
                equal_arrivals = True
            else: 
                equal_arrivals = False


        # Run an if statement: if all processes have the same arrival time then run without ready_processes. else run with ready_processes
        if equal_arrivals:
            while processes:
                

        # Else run with ready_processes
        else:
            pass