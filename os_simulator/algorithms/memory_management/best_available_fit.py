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

                elif state == 1:  # Step 2: Add Multiple Processes (Size Only)
                    if event.key == pygame.K_RETURN:
                        if proc_size_input.strip() != "":
                            try:
                                s_val = int(proc_size_input.strip())
                                if s_val <= 0:
                                    raise ValueError
                                
                                # --- INLINE INTEGRATED BEST-AVAILABLE-FIT LOGIC ---
                                process_number = len(jobs) + 1
                                job_item = {
                                    "process_id": f"P{process_number}",
                                    "size": s_val,
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
                                error_message = ""
                            except ValueError:
                                error_message = "Values must be positive numbers greater than 0!"
                        else:
                            error_message = "Please enter a process size!"
                    elif event.key == pygame.K_BACKSPACE:
                        proc_size_input = proc_size_input[:-1]
                    else:
                        if event.unicode.isdigit():
                            proc_size_input += event.unicode

        # Rendering Background Graphics
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)

        # 1. Top Left Header Panel
        title_surface = font_title.render("MEMORY MANAGEMENT: Best-Available-Fit Algorithm", True, BLACK)
        screen.blit(title_surface, (20, 10))

        # 2. Rendering Content States
        if state == 0:
            txt1 = "Initialize the Fixed Partition Arrays Map"
            txt2 = "Enter memory block partitions separated with commas"
            txt3 = "(e.g., 200,400,150):"
            txt4 = f"[{partitions_input}]"

            surf1 = font_input.render(txt1, True, NEON_GREEN)
            surf2 = font_input.render(txt2, True, NEON_GREEN)
            surf3 = font_input.render(txt3, True, NEON_GREEN)
            surf4 = font_input.render(txt4, True, NEON_GREEN)

            screen.blit(surf1, surf1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140)))
            screen.blit(surf2, surf2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))
            screen.blit(surf3, surf3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 95)))
            screen.blit(surf4, surf4.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 165)))


        elif state == 1:
            part_str = ",".join(map(str, memory_size))
            txt1 = f"Add Incoming Tasks to Fixed Partitions Matrix [{part_str}]"
            txt2 = f"Enter Process Size:  {proc_size_input}"
            txt3 = "Press [ENTER] to execute evaluation logic."

            surf1 = font_input.render(txt1, True, NEON_GREEN)
            surf2 = font_input.render(txt2, True, NEON_GREEN)
            surf3 = font_table.render(txt3, True, NEON_GREEN)

            screen.blit(surf1, surf1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140)))
            screen.blit(surf2, surf2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))
            screen.blit(surf3, surf3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))

            if error_message:
                err_surf = font_title.render(error_message, True, RED)
                screen.blit(err_surf, err_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120)))

        # 4. Render the Interactive < BACK Button
        if back_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, NEON_GREEN, back_rect.inflate(10, 5), 0, 4)
            back_surface = font_setup.render("< BACK", True, BLACK)
        else:
            back_surface = font_setup.render("< BACK", True, NEON_GREEN)
            screen.blit(back_surface, back_rect.topleft)
            pygame.display.flip()
            clock.tick(30)