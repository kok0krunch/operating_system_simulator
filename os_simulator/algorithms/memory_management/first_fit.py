# First-Fit Memory Management Algorithm

class FirstFit:
    def __init__(self):
        self.memory_size = None
        self.process_size = None
        self.burst_time = None

    def mft_settings(self):
        while True:
            try:
                memory_size_input = input("Enter partitions separated with comma (ex. 1,2,3): ").strip()
                memory_size_list = [int(size.strip()) for size in memory_size_input.split(',')]
                for size in memory_size_list:
                    if int(size) <= 0:
                        raise ValueError
                    
                self.memory_size=memory_size_list
                break

            except:
                print("Memory sizes should only be positive integers. Voiding initial inputs")


        while True:
            try:
                process_size_input= input("enter process size: ").strip()
                burst_time_input= input("enter burst time: ").strip()

                if int(process_size_input) > 0 and int(burst_time_input) > 0:
                    self.process_size=int(process_size_input)
                    self.burst_time=int(burst_time_input)
                    print("Process size:", self.process_size)
                    print("Burst time:", self.burst_time)
                    break

                elif int(process_size_input) <= 0 or int(burst_time_input) <= 0:
                    raise ValueError
                
            except:
                print("Process size and burst time should be positive integers. Please input valid numbers.")  
    
    def mft_logic(self):
        pass


    def mvt_settings(self):
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


    def mvt_logic(self):
        pass

# definitions
def user_input(first_fit):
    while True:
        try:
            memory_type_input=input("Enter memory type (MFT/MVT):").strip()
            if memory_type_input.upper()=="MFT":
                first_fit.mft_settings()
            elif memory_type_input.upper()=="MVT":
                first_fit.mvt_settings()
            else:
                raise ValueError

        except:
            print("Invalid input. Please enter 'MFT' or 'MVT'")
            continue

# main program
if __name__ == "__main__":
    first_fit = FirstFit()
    print("Welcome to the First-Fit Memory Management Algorithm Simulator!")
    user_input(first_fit)