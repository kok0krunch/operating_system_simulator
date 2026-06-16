# First-Fit Memory Management Algorithm

class FirstFit:
    def __init__(self, memory_sizes, process_sizes, burst_times):
        self.memory_sizes = memory_sizes
        self.process_sizes = process_sizes
        self.burst_times = burst_times