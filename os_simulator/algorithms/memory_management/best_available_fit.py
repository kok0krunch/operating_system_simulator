import pygame
import sys
import os

#font colors
NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen Size Dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def baf_menu(screen):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Best-Available-Fit Algorithm")
    clock = pygame.time.Clock()

    try:
        background = pygame.image.load("os_simulator\\components\\background.png").convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        background = None

    font_path = "os_simulator\\components\\VT323-Regular.ttf"
    if not os.path.exists(font_path):
        print(f"CRITICAL ERROR: The font file '{font_path}' was not found in the directory.")
        pygame.quit()
        sys.exit()

    font_title = pygame.font.Font(font_path, 36) 
    font_setup = pygame.font.Font(font_path, 46) 
    font_input = pygame.font.Font(font_path, 48) 
    font_table = pygame.font.Font(font_path, 32) 

    #Variables
    memory_size = None      
    jobs = []               
    partition_busy = None
    state = 0 
    partitions_input = ""
    proc_size_input = ""
    proc_burst_input = ""
    active_field = "size" 
    error_message = ""

    # Main UI loop
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Pre-create navigation hitboxes
        back_surf_idle = font_setup.render("< BACK", True, NEON_GREEN)
        back_rect = back_surf_idle.get_rect(topleft=(30, 650))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left Click
                    if back_rect.collidepoint(mouse_pos):
                        running = False
                        return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return

                if state == 0:  # Step 1: Input Partitions List
                    if event.key == pygame.K_RETURN:
                        raw = partitions_input.strip()
                        if raw != "":
                            try:
                                size_list = [int(s.strip()) for s in raw.split(',') if s.strip() != ""]
                                if any(val <= 0 for val in size_list):
                                    raise ValueError
                                if not size_list:
                                    raise ValueError
                                
                                memory_size = size_list
                                partition_busy = [False] * len(memory_size)
                                state = 1
                                error_message = ""
                            except ValueError:
                                error_message = "Sizes must be positive integers! (ex. 100,200,300)"
                        else:
                            error_message = "Input cannot be empty!"
                    elif event.key == pygame.K_BACKSPACE:
                        partitions_input = partitions_input[:-1]
                    else:
                        if event.unicode.isdigit() or event.unicode == ',':
                            partitions_input += event.unicode

                elif state == 1:  # Step 2: Add Multiple Processes
                    if event.key == pygame.K_TAB:
                        active_field = "burst" if active_field == "size" else "size"
                    elif event.key == pygame.K_RETURN:
                        if proc_size_input.strip() != "" and proc_burst_input.strip() != "":
                            try:
                                s_val = int(proc_size_input.strip())
                                b_val = int(proc_burst_input.strip())
                                if s_val <= 0 or b_val <= 0:
                                    raise ValueError
                                
                                # --- INLINE INTEGRATED BEST-AVAILABLE-FIT LOGIC ---
                                process_number = len(jobs) + 1
                                job_item = {
                                    "process_id": f"P{process_number}",
                                    "size": s_val,
                                    "burst_time": b_val,
                                    "allocated_partition": None,
                                    "fragmentation": 0
                                }
                                
                                partition_count = len(memory_size)
                                optimal_index = -1
                                
                                # Find smallest available partition that fits perfectly
                                for block_index in range(partition_count):
                                    if memory_size[block_index] >= job_item["size"] and not partition_busy[block_index]:
                                        if optimal_index == -1 or memory_size[block_index] < memory_size[optimal_index]:
                                            optimal_index = block_index
                                
                                if optimal_index != -1:
                                    job_item["allocated_partition"] = optimal_index + 1
                                    job_item["fragmentation"] = memory_size[optimal_index] - job_item["size"]
                                    partition_busy[optimal_index] = True
                                else:
                                    # If busy, look for best partition to suspend / swap out
                                    available_swap_index = -1
                                    for block_index in range(partition_count):
                                        if memory_size[block_index] >= job_item["size"]:
                                            if available_swap_index == -1 or memory_size[block_index] < memory_size[available_swap_index]:
                                                available_swap_index = block_index
                                    
                                if available_swap_index != -1:
                                    # Evict process currently occupying this specific partition index
                                    for old_job in jobs:
                                        if old_job["allocated_partition"] == available_swap_index + 1:
                                            old_job["allocated_partition"] = "Swapped Out"
                                            old_job["fragmentation"] = 0
                                        
                                    job_item["allocated_partition"] = available_swap_index + 1
                                    job_item["fragmentation"] = memory_size[available_swap_index] - job_item["size"]
                                    partition_busy[available_swap_index] = True
                                else:
                                    job_item["allocated_partition"] = "Too Large"
                                    
                                jobs.append(job_item)
                                # ---------------------------------------------------
                                
                                proc_size_input = ""
                                proc_burst_input = ""
                                active_field = "size"
                                error_message = ""
                            except ValueError:
                                error_message = "Values must be positive numbers greater than 0!"
                        else:
                            error_message = "Fill both fields! Press TAB to shift focus."
                    elif event.key == pygame.K_BACKSPACE:
                        if active_field == "size":
                            proc_size_input = proc_size_input[:-1]
                        else:
                            proc_burst_input = proc_burst_input[:-1]
                    else:
                        if event.unicode.isdigit():
                            if active_field == "size":
                                proc_size_input += event.unicode
                            else:
                                proc_burst_input += event.unicode

                elif state == 2:  # Step 3: View & Clear Variables on Reset
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        state = 0
                        partitions_input = ""
                        proc_size_input = ""
                        proc_burst_input = ""
                        jobs = []
                        memory_size = None
                        partition_busy = None
                        error_message = ""

        # Rendering base layer graphics
        if background:
            screen.blit(background, (0, 0))