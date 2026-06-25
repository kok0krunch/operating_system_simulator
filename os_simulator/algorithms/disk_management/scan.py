# SCAN Scheduling Algorithm - Elevator Algorithm
#import libraries
import pygame
import sys

#Class for SCAN Scheduling
class SCANScheduling:

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


#Draw arrow
def draw_arrow(surface, color, start, end):

    pygame.draw.line(surface, color, start, end, 1)

    dx = end[0] - start[0]
    dy = end[1] - start[1]

    angle = pygame.math.Vector2(dx, dy).angle_to((1, 0))

    arrow_size = 10

    left = pygame.math.Vector2(arrow_size, 0).rotate(-angle + 150)

    right = pygame.math.Vector2( arrow_size, 0).rotate(-angle - 150)

    pygame.draw.line(surface,color,end,(end[0] + left.x, end[1] + left.y),3)

    pygame.draw.line(surface,color,end,(end[0] + right.x, end[1] + right.y),3)

    

#Main Program
def main():

    pygame.init()

    WIDTH = 1280
    HEIGHT = 720

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SCAN Disk Scheduling")

    clock = pygame.time.Clock()

    NEON_GREEN = (57, 255, 20)
    BLACK = (0, 0, 0)
    # ----------------------------------
    # Assets
    # ----------------------------------

    background = pygame.image.load("os_simulator\\components\\background.png")
    background = pygame.transform.scale(
        background,
        (WIDTH, HEIGHT)
    )

    font_title = pygame.font.Font("os_simulator\\components\\VT323-Regular.ttf",36)

    font_large = pygame.font.Font("os_simulator\\components\\VT323-Regular.ttf",46)

    font_small = pygame.font.Font("os_simulator\\components\\VT323-Regular.ttf",28)


    #Screens
    HEAD_INPUT = 0
    REQUEST_INPUT = 1
    DISK_SIZE_INPUT = 2
    DIRECTION_INPUT = 3
    RESULT_SCREEN = 4

    current_screen = HEAD_INPUT

    #Variables
    head_text = ""
    request_text = ""
    disk_size_text = ""
    direction_text = ""

    head = 0
    requests = []
    disk_size = 0
    direction = ""

    sequence = []
    total_head_movement = 0

    #Draw head screen

    def draw_head_screen():

        screen.blit(background, (0, 0))

        title = font_title.render("DISK SCHEDULING: Scan",True, BLACK)

        screen.blit(title, (20, 10))

        label = font_large.render("Input initial head position:",True,NEON_GREEN)

        screen.blit(label, (380, 280))

        value = font_large.render(head_text,True,NEON_GREEN)

        text_rect = value.get_rect(center= (WIDTH//2, 360))

        screen.blit(value,text_rect)

        back = font_large.render("< BACK",True,NEON_GREEN)

        screen.blit(back, (30, 650))

    #Draw request screen

    def draw_request_screen():

        screen.blit(background, (0, 0))

        title = font_title.render("DISK SCHEDULING: Scan",True,BLACK)

        screen.blit(title, (20, 10))

        label = font_large.render("Input disk requests (comma separated):",True,NEON_GREEN)

        screen.blit(label, (250, 280))

        value = font_large.render(request_text,True,NEON_GREEN)

        screen.blit(value, (260, 340))

        back = font_large.render("< BACK",True,NEON_GREEN)
    
        screen.blit(back, (30, 650))


    #Draw disk size screen
    def draw_disk_size_screen():

        screen.blit(background,(0,0))

        title = font_title.render("DISK SCHEDULING: SCAN",True,BLACK)

        screen.blit(title,(20,10))

        label = font_large.render("Input Disk Size (0-199):",True,NEON_GREEN)

        screen.blit(label,(450,280))

        value = font_large.render(disk_size_text,True,NEON_GREEN)

        rect = value.get_rect(center=(WIDTH//2,360))

        screen.blit(value,rect)

    #Draw direction screen
    def draw_direction_screen():

        screen.blit(background,(0,0))

        title = font_title.render("DISK SCHEDULING: SCAN",True,BLACK)

        screen.blit(title,(20,10))

        label = font_large.render("Direction (left/right):",True,NEON_GREEN)

        screen.blit(label,(400,280))

        value = font_large.render(direction_text,True,NEON_GREEN)

        rect = value.get_rect(center=(WIDTH//2,360))

        screen.blit(value,rect)
    #Draw graph

    def draw_graph():

        if len(sequence) == 0:
            return

        start_x = 100
        end_x = 1050

        axis_y = 120

        pygame.draw.line(screen,NEON_GREEN,(start_x, axis_y),(end_x, axis_y),3)

        max_value = max(sequence)

        # Draw cylinder markers
        for value in sequence:

            x = start_x + (value / max_value) * (end_x - start_x)

            pygame.draw.line(screen,NEON_GREEN,(x, 90),(x, 150),4)

            label = font_small.render(str(value),True, NEON_GREEN)

            screen.blit(label,(x - 10, 55))

        # Draw head movement
        base_y = 200
        step_y = 40

        for i in range(len(sequence) - 1):

            current = sequence[i]
            nxt = sequence[i + 1]

            x1 = start_x + (
                current / max_value) * (end_x - start_x)

            x2 = start_x + (nxt / max_value) * (end_x - start_x)

            y1 = base_y + i * step_y
            y2 = base_y + (i + 1) * step_y

            draw_arrow(screen,NEON_GREEN,(x1, y1),(x2, y2))

    #Draw result screen
    def draw_result_screen():

        screen.blit(background, (0, 0))

        title = font_title.render("DISK SCHEDULING: Scan",True,BLACK)

        screen.blit(title, (20, 10))

        draw_graph()

        total = font_large.render(f"Total Head Movement: {total_head_movement}",True,NEON_GREEN)

        screen.blit(total, (40, 650))

    #Game loop
    running = True

    while running:

        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                #Head input screen
                if current_screen == HEAD_INPUT:
                    if event.key == pygame.K_RETURN:
                        if head_text.strip() != "":
                            head = int(head_text)
                            current_screen = REQUEST_INPUT
                    elif event.key == pygame.K_BACKSPACE:
                        head_text = head_text[:-1]
                    elif event.unicode.isdigit():
                        head_text += event.unicode

                #Request input screen
                elif current_screen == REQUEST_INPUT:
                    if event.key == pygame.K_RETURN:
                        try:
                            
                            requests = [int(x.strip()) for x in request_text.split(",") if x.strip() != ""]
                            current_screen = DISK_SIZE_INPUT
                        except ValueError:
                            pass
                    elif event.key == pygame.K_BACKSPACE:
                        request_text = request_text[:-1]
                    else:
                        allowed = "0123456789, "
                        if event.unicode in allowed:
                            request_text += event.unicode

                #Disk size input screen
                elif current_screen == DISK_SIZE_INPUT:
                    if event.key == pygame.K_RETURN:
                        if disk_size_text.strip() != "":
                            disk_size = int(disk_size_text)
                            current_screen = DIRECTION_INPUT
                    elif event.key == pygame.K_BACKSPACE: 
                        disk_size_text = disk_size_text[:-1]
                    elif event.unicode.isdigit():         
                        disk_size_text += event.unicode  

                #DIrection input screen
                elif current_screen == DIRECTION_INPUT:
                    if event.key == pygame.K_RETURN:
                        direction = direction_text.lower().strip()
                        if direction in ["left", "right"]:
                            scan = SCANScheduling(head, requests, disk_size, direction)
                            total_head_movement, sequence = scan.compute()
                            current_screen = RESULT_SCREEN
                    elif event.key == pygame.K_BACKSPACE:
                        direction_text = direction_text[:-1]
                    elif event.unicode.isalpha():        
                        direction_text += event.unicode

                #Result screen
                elif current_screen == RESULT_SCREEN:
                    if event.key == pygame.K_ESCAPE:
                    
                        head_text = ""
                        request_text = ""
                        disk_size_text = ""
                        direction_text = ""
                        sequence = []
                        total_head_movement = 0
                        current_screen = HEAD_INPUT


        
        if current_screen == HEAD_INPUT:
            draw_head_screen()
        elif current_screen == REQUEST_INPUT:
            draw_request_screen()
        elif current_screen == DISK_SIZE_INPUT:
            draw_disk_size_screen()
        elif current_screen == DIRECTION_INPUT:
            draw_direction_screen()
        elif current_screen == RESULT_SCREEN:
            draw_result_screen()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


# ENTRY POINT
if __name__ == "__main__":
    main()