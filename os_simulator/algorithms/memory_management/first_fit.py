# First-Fit Memory Management Algorithm

class FirstFit:
    def __init__(self, memory_sizes, process_sizes, burst_times, memory_type):
        self.memory_sizes = memory_sizes
        self.process_sizes = process_sizes
        self.burst_times = burst_times
        self.memory_type= memory_type

    def first_fit_logic(self):
        pass

# definitions
def user_input():
    while True:
        try:
            memory_type_input=input("Enter memory type (MFT/MVT):").strip()

        except:
            print("Invalid input. Please enter 'MFT' or MVT'")

# main program
if __name__ == "__main__":
    first_fit=FirstFit()
    print("Binary Search Tree\nTo start type:")
    user_input()