# First-Fit Memory Management Algorithm

class FirstFit:
    def __init__(self, memory_size, process_size, burst_time,):
        self.memory_size = memory_size
        self.process_size = process_size
        self.burst_time = burst_time

    def mft_logic(self):
        while True:
            try:
                memory_size_input = input("Enter partitions separated with comma (ex. 1,2,3): ").strip()
            except:
                pass

    def mvt_logic(self):
         while True:
            try:
                memory_size_input = input("Enter total memory block size: ").strip()
                if int(memory_size_input)>0:
                    pass
                else:
                    return ValueError
            except:
                if memory_size_input<=0:
                    print("Memory block size inserted is negative. Please input a positive number.")
                    continue
                else:
                    print("Memory block size inserted is not a number. Please type a number")
                    continue

# definitions
def user_input():
    while True:
        try:
            memory_type_input=input("Enter memory type (MFT/MVT):").strip()
            if memory_type_input.upper()=="MFT":
                FirstFit.mft_logic()
            elif memory_type_input.upper()=="MVT":
                FirstFit.mvt_logic()
            else:
                return ValueError

        except:
            print("Invalid input. Please enter 'MFT' or MVT'")
            continue

# main program
if __name__ == "__main__":
    first_fit=FirstFit()
    print("Binary Search Tree\nTo start type:")
    user_input()