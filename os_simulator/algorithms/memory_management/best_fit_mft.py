# Best-Fit Memory Management Algorithm
import pygame
import sys
import os

NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def mvt_menu(screen):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Best-Fit Algorithm")
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

    # Variables
    memory_size = None      
    jobs = []            
    partition_busy = None
    state = 0 
    partitions_input = ""
    proc_size_input = ""
    error_message = ""
    part_str = ""

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
                                
                                # Check maximum partition size limit
                                if len(size_list) > 5:
                                    error_message = "Too many partitions! Maximum allowed is 5."
                                    raise ValueError
                                
                                # Check for invalid zero or negative integers
                                if any(val <= 0 for val in size_list):
                                    error_message = "Sizes must be positive integers!"
                                    raise ValueError
                                if not size_list:
                                    raise ValueError
                                
                                # If all checks pass safely, advance the state machine
                                memory_size = size_list
                                partition_busy = [False] * len(memory_size)
                                state = 1
                                error_message = ""
                            except ValueError:
                                # Fallback message if specific error flags weren't caught above
                                if not error_message:
                                    error_message = "Sizes must be positive integers! (ex. 100,200,300)"
                                # NOTE: We do not clear partitions_input here, so it stays on screen!
                        else:
                            error_message = "Input cannot be empty!"
                    elif event.key == pygame.K_BACKSPACE:
                        partitions_input = partitions_input[:-1]
                    else:
                        if event.unicode.isdigit() or event.unicode == ',':
                            partitions_input += event.unicode

                elif state == 1:  
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
                                available_swap_index = -1  
                                
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
                                    # If busy, return error message
                                    job_item["allocated_partition"] = "Out of Space"

                                    
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


    
            pygame.draw.line(screen, NEON_GREEN, (50, 520), (SCREEN_WIDTH - 50, 520), 2)
            
            txt_title = f"MFT FIXED MATRIX ACTIVATED: [{part_str}]"
            txt_input = f"Enter Process Size: [{proc_size_input}]"
            txt_hint  = "Press [ENTER] to execute evaluation logic loops."

            surf_title = font_title.render(txt_title, True, NEON_GREEN)
            surf_input = font_input.render(txt_input, True, NEON_GREEN)
            surf_hint  = font_table.render(txt_hint, True, NEON_GREEN)

            # Draw the texts horizontally aligned along the lower panel section
            screen.blit(surf_title, (50, 535))
            screen.blit(surf_input, (50, 580))
            screen.blit(surf_hint,  (SCREEN_WIDTH - surf_hint.get_width() - 50, 580))

            if error_message:
                err_surf = font_title.render(error_message, True, RED)
                screen.blit(err_surf, (50, 620))

        # Rendering Background Graphics
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)

        # 1. Top Left Header Panel
        title_surface = font_title.render("MEMORY MANAGEMENT: Best-Fit Algorithm (MFT)", True, BLACK if background else NEON_GREEN)
        screen.blit(title_surface, (20, 10))

        # 2. Rendering Content States
        if state == 0:
            txt1 = "Initialize the Fixed Partition Memory Map"
            txt2 = "Enter memory block partitions separated with commas"
            txt5 = "Memory partition is limited to 5 parts only"
            txt3 = "(e.g., 200,400,150):"
            txt4 = f"[{partitions_input}]"

            surf1 = font_input.render(txt1, True, NEON_GREEN)
            surf2 = font_input.render(txt2, True, NEON_GREEN)
            surf3 = font_input.render(txt3, True, NEON_GREEN)
            surf4 = font_input.render(txt4, True, NEON_GREEN)
            surf5 = font_input.render(txt5, True, NEON_GREEN)

            screen.blit(surf1, surf1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140)))
            screen.blit(surf2, surf2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))
            screen.blit(surf3, surf3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 95)))
            screen.blit(surf4, surf4.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 155)))
            screen.blit(surf5, surf5.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))

        elif state == 1:
            # 1. Setup Text Prompts (Shifted higher to make room below)
            part_str = ",".join(map(str, memory_size))
            txt1 = f"Add Incoming Tasks to Fixed Partitions Matrix[{part_str}]"
            txt2 = f"Enter Process Size:  [{proc_size_input}]"
            txt3 = "Press [ENTER] to execute evaluation logic."
            
            surf1 = font_input.render(txt1, True, NEON_GREEN)
            surf2 = font_input.render(txt2, True, NEON_GREEN)
            surf3 = font_table.render(txt3, True, NEON_GREEN)

            screen.blit(surf1, surf1.get_rect(center=(SCREEN_WIDTH // 2, 120)))
            screen.blit(surf2, surf2.get_rect(center=(SCREEN_WIDTH // 2, 170)))
            screen.blit(surf3, surf3.get_rect(center=(SCREEN_WIDTH // 2, 210)))

            # 2. Render On-Screen Error Validation Flags
            if error_message:
                err_surf = font_title.render(error_message, True, RED)
                screen.blit(err_surf, err_surf.get_rect(center=(SCREEN_WIDTH // 2, 210)))

            # --- DYNAMIC VERTICAL MEMORY MAP GRAPHICS ---
            map_width = 300
            map_height_per_block = 60
            start_x = (SCREEN_WIDTH - map_width) // 2
            start_y = 300
            
            partition_count = len(memory_size)
            
            # Find which job is currently occupying which partition
            block_occupants = [None] * partition_count
            for job in jobs:
                if isinstance(job["allocated_partition"], int):
                    idx = job["allocated_partition"] - 1
                    if 0 <= idx < partition_count:
                        block_occupants[idx] = job

            # Render each partition block vertically
            current_y = start_y
            for i in range(partition_count):
                block_rect = pygame.Rect(start_x, current_y, map_width, map_height_per_block)
                occupant = block_occupants[i]
                
                if occupant:
                    # Partition is occupied (Render with RED boundary and cross mark)
                    pygame.draw.rect(screen, RED, block_rect, 2)
                    
                    info_text = f"{occupant['process_id']} ({occupant['size']} units)"
                    info_surf = font_table.render(info_text, True, RED)
                    screen.blit(info_surf, info_surf.get_rect(center=block_rect.center))
                    
                    # Draw visual X cross inside the block
                    pygame.draw.line(screen, RED, (start_x, current_y), (start_x + map_width, current_y + map_height_per_block), 1)
                    pygame.draw.line(screen, RED, (start_x, current_y + map_height_per_block), (start_x + map_width, current_y), 1)
                else:
                    # Partition is FREE (NEON_GREEN layout)
                    pygame.draw.rect(screen, NEON_GREEN, block_rect, 2)
                    info_surf = font_table.render("FREE", True, NEON_GREEN)
                    screen.blit(info_surf, info_surf.get_rect(center=block_rect.center))
                
                # Partition ID label and capacity boundaries [Left side alignment]
                label_text = f"Part {i+1} [{memory_size[i]}]"
                label_surf = font_table.render(label_text, True, NEON_GREEN if not occupant else RED)
                screen.blit(label_surf, (start_x - 160, current_y + (map_height_per_block // 2) - 12))
                
                # Fragmentation data metrics tracking [Right side alignment]
                if occupant:
                    frag_text = f"Frag: {occupant['fragmentation']}"
                    frag_surf = font_table.render(frag_text, True, RED)
                    screen.blit(frag_surf, (start_x + map_width + 20, current_y + (map_height_per_block // 2) - 12))
                
                current_y += map_height_per_block + 10  # Spacing layout gap

            # Display Starvation processes below the visual map blocks
            waiting_jobs = [j for j in jobs if j["allocated_partition"] == "Out of Space"]
            if waiting_jobs:
                queue_y = current_y + 15
                queue_txt = "Waiting Queue: " + ", ".join([f"{j['process_id']} ({j['size']})" for j in waiting_jobs])
                queue_surf = font_table.render(queue_txt, True, RED)
                screen.blit(queue_surf, queue_surf.get_rect(center=(SCREEN_WIDTH // 2, queue_y)))

        # 4. Render the Interactive < BACK Button
        if back_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, NEON_GREEN, back_rect.inflate(10, 5), 0, 4)
            back_surface = font_setup.render("< BACK", True, BLACK)
        else:
            back_surface = font_setup.render("< BACK", True, NEON_GREEN)
        screen.blit(back_surface, back_rect.topleft)
            
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    test_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    mvt_menu(test_screen)