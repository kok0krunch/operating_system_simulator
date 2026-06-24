# First-Come, First-Served (FCFS) Disk Scheduling Algorithm

#Create class for FCFS
class FCFSDiskScheduling:

    #initialize head and requests
    def __init__(self, head, requests):
        self.head = head
        self.requests = requests

    #To compute total head movement
    def compute(self):
        total_movement = 0
        sequence = [self.head]
        current = self.head

    #Process each disk request in arrival order
        for request in self.requests:
            
            #Computes distance betweet current head and next request then adds to the total head movement
            total_movement += abs(current - request)

            #Move head to the next request
            current = request

            #Store sequence of head movement
            sequence.append(current)


        return total_movement, sequence

    #Display the FCFS Scheduling result
    def display_result(self, total, sequence):
        print("\nFCFS Disk Scheduling Result")
        print("Seek Sequence:")
        print(" -> ".join(map(str, sequence)))
        print("\nTotal Head Movement:", total)


#For user input and program execution
if __name__ == "__main__":

    #Get inital head position from user
    head = int(input("Enter initial head position: "))

    #Ask for disk requests 
    requests_input = input("Enter disk requests (comma-separated): ")

    requests = []

    for raw_request in requests_input.split(","):
        requests.append(int(raw_request.strip()))


    #Create object
    fcfs = FCFSDiskScheduling(head, requests)

    #Compute total head movement 
    total, sequence = fcfs.compute()

    #Display final result 
    fcfs.display_result(total, sequence)