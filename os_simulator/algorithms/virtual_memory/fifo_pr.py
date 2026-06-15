# First-In, First-Out (FIFO) Page Replacement Algorithm

class FIFOPageReplacement:
    def __init__(self, capacity=3): # Default capacity of page frames is set to 3, can be changed by user input
        self.capacity = capacity
        self.frames = [None] * capacity  # This will hold the pages currently in memory
        self.page_faults = 0
        self.pointer = 0  # This will point to the oldest page in the memory

    def user_input(self):
        # Ask the user for the capacity of the page frames
        print("The default capacity is set to 3. You can change it by entering a new value or type '3' to keep the default.")
        
        capacity_raw = input("Enter new capacity of the page frames: ").strip()
        
        if capacity_raw != '3' and capacity_raw != '':
            try:
                self.capacity = int(capacity_raw)
                # Re-initialize the array size based on the user's custom capacity choice
                self.frames = [None] * self.capacity
            except ValueError:
                print("❌ Invalid entry. Staying with default capacity: 3")
                self.capacity = 3
        
        print(f"Page frame capacity set to: {self.capacity}\n")

        # Ask the user for the entire list of page numbers to be accessed
        while True:
            page_raw = input("Enter a list of page numbers to access separated by comma (e.g., 1,2,3): ").strip()
            try:
                page_sequence = [int(page.strip()) for page in page_raw.split(',')]
                if not page_sequence:
                    print("Please enter at least one page number.")
                    continue
                break
            except ValueError:
                print("Invalid input format. Please enter a valid list of page numbers separated by commas.")
         
        self.run_simulation(page_sequence)
                    
    def run_simulation(self, page_sequence):
        print("\n" + "="*50)
        print("SIMULATION TABLE OUTPUT (FIFO)")
        print("="*50)
    
        # Table Header
        print(f"{'Page References':<6} | {'Page Frames':<18} | {'Status':<10}")
        print("-" * 50)
        
        # Iterate through each page reference and access it
        for page in page_sequence:
            status = ""
            
            # PAGE HIT: If the page is already in memory, it's a hit and we do nothing
            if page in self.frames:
                status = "⭐"
                
            # PAGE FAULT: If the page isn't in memory, we need to add it
            else:
                self.page_faults += 1
                self.frames[self.pointer] = page  # Replace inside the fixed slot position
                self.pointer = (self.pointer + 1) % self.capacity  # Advance pointer
                status = "FAULT"
            
            # Print current row matching a structured vertical snapshot
            # Formats the array visually like [7, 0, 1] but replaces None with '-' for neatness
            readable_frames = [str(f) if f is not None else "-" for f in self.frames]
            print(f"{page:<15} | {str(readable_frames):<18} | {status:<10}")

        print("-" * 45)
        print(f"Total Page Faults: {self.page_faults}")
        print("="*50)

fifo = FIFOPageReplacement()  # Default capacity, can be changed by user input
fifo.user_input()