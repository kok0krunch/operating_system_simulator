# SCAN Scheduling Algorithm - Elevator Algorithm

#Class for SCAN Scheduling
class SCAN:

    #Initialize head, requests, disk_size, direction
    def __init__(self, head, requests, disk_size, direction):
        self.head = head
        self.requests = requests
        self.disk_size = disk_size
        self.direction = direction.lower()

    #Compute total head movement and seek sequence
    def compute(self):
        total_movement = 0
        sequence = [self.head]
        current = self.head

        left = []
        right = []

        #Separate requests based on head position for directional scanning
        for request in self.requests:
            if request < current:
                left.append(request)
            else:
                right.append(request)

        
        #Sort both sides in ascending order
        left.sort()
        right.sort()

        #SCAN movement logic 
        if self.direction == "right":

            #Move right side first
            for request in right:
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

            # Go to end of disk
            total_movement += abs(current - (self.disk_size - 1))
            current = self.disk_size - 1
            sequence.append(current)

            # Then move left side
            for request in reversed(left):
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

        else:

            # Move left side first
            for request in reversed(left):
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

            # Go to start of disk
            total_movement += abs(current - 0)
            current = 0
            sequence.append(current)

            # Then move right side
            for request in right:
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

        return total_movement, sequence


    # Display result
    def display_result(self, total, sequence):
        print("\nSCAN Disk Scheduling Result")

        print("Seek Sequence:")
        print(" -> ".join(map(str, sequence)))

        print("\nTotal Head Movement:", total)

#For user input and program execution
if __name__ == "__main__":

    #Ask user to input initial head position
    head = int(input("Enter initial head position: "))

    #Ask user input disk requests
    requests_input = input("Enter disk requests (comma-separated): ")

    requests = []

    for request in requests_input.split(","):
        requests.append(int(request.strip()))

    #Ask user input disk size 
    disk_size = int(input("Enter disk size (ex. 200): "))

# Validate initial head position
if head < 0 or head >= disk_size:
    print(f"\nError: Initial head position must be between 0 and {disk_size - 1}.")
    exit()

# Validate disk requests
for request in requests:
    if request < 0 or request >= disk_size:
        print(f"\nError: Disk request {request} is outside the valid range (0-{disk_size - 1}).")
        exit()
        
    #Ask user input direction
    direction = input("Enter direction (left/right): ")

    #Create SCAN object

    scan = SCAN(head, requests, disk_size, direction)

    #Compute results
    total, sequence = scan.compute()

    #Display results
    scan.display_result(total, sequence)