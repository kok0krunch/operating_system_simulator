# Shortest Seek Time First (SSTF) Disk Scheduling Algorithm

#SSTF Scheduling

#class for SSTF
class SSTF:

    #initialize head and requests
    def __init__(self, head, requests):
        self.head = head
        self.requests = requests.copy()  # so original list is not modified

    def compute(self): 
        total_movement = 0
        sequence = [self.head]
        current = self.head

        #Make a working copy of requests
        pending = self.requests.copy()

        #While loop the pending and ends the loop when empty
        while pending:
         
            #Find closest request to current head
            closest_request = min(pending, key=lambda x: abs(current - x))

            #Compute movement
            movement = abs(current - closest_request)
            total_movement += movement

            #Move head
            current = closest_request
            sequence.append(current)

            #Remove served request
            pending.remove(closest_request)

        return total_movement, sequence


#Display the SSTF Scheduling result
    def display_result(self, total, sequence):
        print("\nSSTF Disk Scheduling Result")
        print("Seek Sequence:")
        print(" -> ".join(map(str, sequence)))

        print("\nTotal Head Movement:", total)


#For user input and program execution
if __name__ == "__main__":

    head = int(input("Enter initial head position: "))

    requests_input = input("Enter disk requests (comma-separated): ")

    requests = []

    for request in requests_input.split(","):
        requests.append(int(request.strip()))

    sstf = SSTF(head, requests)

    total, sequence = sstf.compute()

    sstf.display_result(total, sequence)