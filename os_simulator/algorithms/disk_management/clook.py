# CLOOK Scheduling Algorithm

#Class for C-LOOK
class CLOOK:

    #Initialize head, requests, disk size, and direction 
    def __init__(self, head, requests, direction):
        self.head = head
        self.requests = requests
        self.direction = direction.lower()  

    #Compute total head movement and seek sequence
    def compute(self):
        total_movement = 0
        sequence = [self.head]
        current = self.head

        left = []
        right = []

    #Separate requests based on head position
        for request in self.requests:
            if request < current:
                left.append(request)
            else:
                right.append(request)

        #Sort both sides in ascending order
        left.sort()
        right.sort()

        #C-LOOK movement logic
        if self.direction == "right":

            #Service right side
            for request in right:
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

            #Jump to the smallest request
            if left:
                total_movement += abs(current - left[0])
                current = left[0]
                sequence.append(current)

                #Continue servicing remaining left requests
                for request in left[1:]:
                    total_movement += abs(current - request)
                    current = request
                    sequence.append(current)

        elif self.direction == "left":

            #Service left side
            for request in reversed(left):
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

            #Jump to the largest request
            if right:
                total_movement += abs(current - right[-1])
                current = right[-1]
                sequence.append(current)

                #Continue servicing remaining right requests
                for request in reversed(right[:-1]):
                    total_movement += abs(current - request)
                    current = request
                    sequence.append(current)

        return total_movement, sequence
    
    # Display result
    def display_result(self, total, sequence):
        print("\nC-LOOK Disk Scheduling Result")
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
c_look = CLOOK(head, requests, direction)

#Compute results
total, sequence = c_look.compute()

#Display
c_look.display_result(total, sequence)