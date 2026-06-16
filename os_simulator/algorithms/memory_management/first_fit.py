# First-Fit Memory Management Algorithm

class FirstFit:
    def __init__(self, memory_size, process_size, burst_time,):
        self.memory_size = None
        self.process_size = None
        self.burst_time = None

    def mft_logic(self):
        while True:
            try:
                memory_size_input = input("Enter partitions separated with comma (ex. 1,2,3): ").strip()
                memory_size_list = [int(size.strip()) for size in memory_size_input.split(',')]
                for size in memory_size_list:
                    if int(size) <= 0:
                        raise ValueError
                    else:
                        self.memory_size=memory_size_list
            except:
                print("Memory sizes should only be positive integers. Voiding initial inputs")
                memory_size_list.clear()

    def mvt_logic(self):
         while True:
            try:
                memory_size_input = input("Enter total memory block size: ").strip()
                if int(memory_size_input)>0:
                    pass
                else:
                    raise ValueError
            except:
                if int(memory_size_input)<=0:
                    print("Memory block size inserted is negative. Please input a positive number.")
                else:
                    print("Memory block size inserted is not a number. Please type a number")


# definitions
def user_input(first_fit):
    while True:
        try:
            memory_type_input=input("Enter memory type (MFT/MVT):").strip()
            if memory_type_input.upper()=="MFT":
                first_fit.mft_logic()
            elif memory_type_input.upper()=="MVT":
                first_fit.mvt_logic()
            else:
                raise ValueError

        except:
            print("Invalid input. Please enter 'MFT' or 'MVT'")
            continue

# main program
if __name__ == "__main__":
    first_fit = FirstFit()
    print("Welcome to the First-Fit Memory Management Algorithm Simulator!")
    user_input()