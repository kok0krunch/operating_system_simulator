# LOOK Scheduling Algorithm

#Class for LOOK
class LOOK: 

    #Initialize head, requests, disk size, and direction 
    def __init__(self, head, requests, direction):
        self.head = head
        self.requests = requests
        self.direction = direction.lower()  

    
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

        #Sort both sides in ascending order 
        left.sort()
        right.sort()

        #LOOK movement logic
        if self.direction == "right":
            #Service right side

            for request in right:
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

            # Reverse direction and service left side
            for request in reversed(left):
                total_movement += abs(current - request)
                current = request
                sequence.append(current)     

        elif self.direction == "left":
            
            #Service left side
            for request in reversed(left):
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

            # Reverse direction and service right side
            for request in right:
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

        return total_movement, sequence    

    # Display result
    def display_result(self, total, sequence):
        print("\nLOOK Disk Scheduling Result")
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

#Ask user input direction
direction = input("Enter direction (left/right): ")

#Create C-SCAN object
look = LOOK(head, requests, direction)

#Compute results
total, sequence = look.compute()

#Display
look.display_result(total, sequence)