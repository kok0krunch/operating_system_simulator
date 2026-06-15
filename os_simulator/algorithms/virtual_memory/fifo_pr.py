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

        # Ask the user for page numbers to be accessed
        while True:
            page_input = input("Enter a page number (or 'exit' to stop): ").strip().lower()
            
            if page_input == 'exit':
                print(f"\nFinal Total Page Faults: {self.page_faults}")
                break
            
            try:
                self.access_page(int(page_input))
            except ValueError:
                print("Please enter a valid integer.")
                
    def access_page(self, page):
        # PAGE HIT: If the page is already in memory, it's a hit and we do nothing
        if page in self.frames:
            print(f"✨ Page Hit! Page {page} is already in memory.")
        
        # PAGE FAULT: If the page isn't in memory, we need to add it
        else:
            self.page_faults += 1
            old_page = self.frames[self.pointer] # Save old value for the print message before overriding it
            self.frames[self.pointer] = page  # Replace the oldest page with the new page in its exact position
            
            if old_page is None:
                print(f"🔄 Page Fault! Placed {page} into an empty slot.")
            else:
                print(f"🔄 Page Fault! Overwrote oldest page ({old_page}) with new page ({page}) at Slot {self.pointer}.")
        
            # Move the pointer to the next slot for the NEXT fault. 
            # If it reaches the end of the capacity, it wraps back to 0.
            self.pointer = (self.pointer + 1) % self.capacity
                
        print(f"Current Pages in Memory: {self.frames}")
        print(f"Total Page Faults: {self.page_faults}\n")

fifo = FIFOPageReplacement()  # Default capacity, can be changed by user input
fifo.user_input()