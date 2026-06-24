# C-SCAN Scheduling Algorithm - Circular SCAN

#Class for C-SCAN
class CSCAN:

    #Initialize head, requests, disk size, and direction 
    def __init__(self, head, requests, disk_size, direction):
        self.head = head
        self.requests = requests
        self.disk_size = disk_size
        self.direction = direction.lower()    

    
    #Compute the total head movement and seek sequence
    def compute(self):
        total_movement = 0
        sequence = [self.head]
        current = self.head

        left = []
        right = []

        # Separate requests based on head position
        for request in self.requests:
            if request < current:
                left.append(request)
            else:
                right.append(request)

        # Sort both sides
        left.sort()
        right.sort()   

        #C-SCAN movement logic
        if self.direction == "right":

            #Service right side
            for request in right:
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

            #Move to end of disk
            if current != self.disk_size - 1:
                total_movement += abs(current - (self.disk_size - 1))
                current = self.disk_size - 1
                sequence.append(current)

            #Jump to beginning
            total_movement += self.disk_size - 1
            current = 0
            sequence.append(current)

            #Service left side
            for request in left:
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

        elif self.direction == "left":

            #Service left side
            for request in reversed(left):
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

            #Move to start of disk
            if current != 0:
                total_movement += current
                current = 0
                sequence.append(current)

            #Jump to end
            total_movement += self.disk_size - 1
            current = self.disk_size - 1
            sequence.append(current)

            #Service right side
            for request in reversed(right):
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

        return total_movement, sequence

    # Display result
    def display_result(self, total, sequence):
        print("\nC-SCAN Disk Scheduling Result")
        print("Seek Sequence:")
        print(" -> ".join(map(str, sequence)))
        print("\nTotal Head Movement:", total)

#For user input and program execution 

#Ask user input for head position
head = int(input("Enter initial head position: "))

#Ask user input disk size
requests_input = input("Enter disk requests (comma-separated): ")

#Store disk request
requests = []

#To process each disk request entered by the user
for request in requests_input.split(","):
    requests.append(int(request.strip()))

#Ask user input disk size
disk_size = int(input("Enter disk size (ex. 200): "))

#Ask user input direction
direction = input("Enter direction (left/right): ")

#Create C-SCAN object
cscan = CSCAN(head, requests, disk_size, direction)

#Compute results
total, sequence = cscan.compute()

#Display
cscan.display_result(total, sequence)