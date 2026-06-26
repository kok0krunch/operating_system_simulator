# Import necessary modules to implement pygame
import pygame
import sys
import os

# Constants and Configurations
NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen Size Dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# First-Come, First-Served (FCFS) CPU Scheduling Algorithm

class Process_FCFS:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0

    def calc_ct(self, prev_completion_time):
        if self.arrival_time > prev_completion_time:
            self.completion_time = self.arrival_time + self.burst_time
        else:
            self.completion_time = prev_completion_time + self.burst_time
    
    def calc_tat(self):
        return self.completion_time - self.arrival_time
    
    def calc_wt(self):
        return self.calc_tat() - self.burst_time
    
    def fcfs_scheduling(processes):
        # Sort processes by arrival time, check if there are any processes to schedule
        if processes:
            processes.sort(key=lambda x: x.arrival_time)
        else: 
            print("No processes to schedule.")
            return [], [], [], 0, 0  # No processes to schedule, return empty lists and average TAT and WT of 0
        
        prev_completion_time = 0
        for process in processes:
            prev_completion_time += process.burst_time
            process.calc_ct(prev_completion_time)
            prev_completion_time = process.completion_time
        
        # Calculate Turnaround Time (TAT) for each process
        tat_list = [process.calc_tat() for process in processes]

        # Calculate average TAT
        avg_tat = sum(tat_list) / len(tat_list)

        # Calculate Waiting Time (WT) for each process
        wt_list = [process.calc_wt() for process in processes]

        # Calculate average WT
        avg_wt = sum(wt_list) / len(wt_list)
        
        return processes, tat_list, wt_list, avg_tat, avg_wt
    
def fcfs_menu(screen):
    """
    Main GUI function for First Come, First Served Scheduling.
    Can be imported and called from another script.
    """
    
    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Load resources with fallbacks
    try:
        background = pygame.image.load("os_simulator\\components\\background.png").convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    except Exception:
        background = None

    # Load the uploaded VT323-Regular.ttf font file explicitly
    font_path = "os_simulator\\components\\VT323-Regular.ttf"
    if not os.path.exists(font_path):
        print(f"CRITICAL ERROR: The font file '{font_path}' was not found in the directory.")
        pygame.quit()
        sys.exit()

    # Define font instances
    font_title = pygame.font.Font(font_path, 36) 
    font_setup = pygame.font.Font(font_path, 46) 
    font_input = pygame.font.Font(font_path, 48) 
    font_table = pygame.font.Font(font_path, 32) 

    # State machine variables 
    state = 0
    error_message = ""
    general_input = ""
    int_input = ""
    P_num = 1
    process_name_input = ""
    process_at_input = ""
    process_bt_input = ""

    # Process simulation variables
    process_list = []
    process_name = ""
    process_at = ""
    process_bt = ""

    # Post simulation variables
    completion_order = []
    turnaround_times = []
    waiting_times = []
    avg_turnaround = 0
    avg_waiting = 0

    # Run FCFS loop

    running = True 
    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Pre-create the < BACK button interaction area at the bottom left coordinates
        back_surf_idle = font_setup.render("< BACK", True, NEON_GREEN)
        back_rect = back_surf_idle.get_rect(topleft=(30, 650))

        # Pre-create buttons for Input Another Process and Simulate

        # This for-loop iterates through several if statements depending on event type
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left click
                if event.button == 1:
                    if back_rect.collidepoint(mouse_pos):
                        running = False
                        return

            elif event.type == pygame.KEYDOWN:
                # Escape = Back
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return
                
                elif state == 0: # Process name input
                    if event.key == pygame.K_RETURN:
                        raw = process_name_input.strip()
                        if raw == "":
                            process_name = f"P{P_num}"
                            P_num += 1
                            state += 1
                            error_message = ""
                        else: 
                            if len(raw) > 4: 
                                error_message = "Error: Process name must be 4 characters or less."
                                continue
                            else: 
                                process_name = raw
                                error_message = ""
                
                elif state == 1: # Process arrival time input

                    # On key event ENTER
                    if event.key == pygame.K_RETURN:
                        raw = process_at_input.strip()
                        # Default to 0 arrival if no input or input 0
                        if raw == "" or raw == "0":
                            process_at = 0
                            state += 1
                            error_message = ""

                        # Else if length of raw is more than 3, that would mean raw > 1000 or raw = str
                        elif len(raw) > 3:
                            error_message = "Error: Process arrival takes too long or is a string"
                            continue

                        # If there is an input and length is valid, try converting to int, increment state, and reset error
                        else: 
                            try:
                                process_at = int(raw)
                                state += 1
                                error_message = ""
                                
                            # Except if int conversion fails and a ValueError is raised
                            except ValueError:
                                error_message = "Error: Input is not an integer and is invalid"
                                continue

                elif state == 2: # Process burst time input

                    # On key event ENTER
                    if event.key == pygame.K_RETURN:

                        # Strip input of whitespaces on tail and rear
                        raw = process_bt_input.strip()

                        # Default to 1 when no input or input 1
                        if raw == "" or raw == "1":
                            process_bt = 1
                            state += 1
                            error_message = ""

                        # Else if length of raw is more than 3, that would mean raw > 1000 or raw = str
                        elif len(raw) > 3:
                            error_message = "Error: Process burst takes too long or is a string"
                            continue

                        # If there is an input and length is valid, try converting to int, increment state, and reset error
                        else: 
                            try:
                                process_bt = int(raw)
                                state += 1
                                error_message = ""
                                
                            # Except if int conversion fails and a ValueError is raised
                            except ValueError:
                                error_message = "Error: Input is not an integer and is invalid"
                                continue

                elif state == 3: # Repeat process attribute input
                    
                    if len(process_list) == 1:
                        state = 0

                    elif len(process_list) > 1: 
                        pass

                    # If process_list == 1: repeat immediately
                    # If process_list >= 2: ask if repeat
                    # If process_list is enough, increment state 

                elif state == 4: # Output (Gantt)
                    pass