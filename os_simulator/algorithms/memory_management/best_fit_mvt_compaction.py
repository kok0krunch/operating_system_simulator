import pygame
import sys
import os

NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def baf_menu(screen):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Best-Fit MVT Algorithm with Compaction")
    clock = pygame.time.Clock()

    try:
        background = pygame.image.load("os_simulator\\components\\background.png").convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        background = None

    font_path = "os_simulator\\components\\VT323-Regular.ttf"
    if not os.path.exists(font_path):
        # Fallback to system monospace if template asset directory isn't present locally
        font_title = pygame.font.SysFont("monospace", 36)
        font_setup = pygame.font.SysFont("monospace", 46)
        font_input = pygame.font.SysFont("monospace", 48)
        font_table = pygame.font.SysFont("monospace", 32)
    else:
        font_title = pygame.font.Font(font_path, 36) 
        font_setup = pygame.font.Font(font_path, 46) 
        font_input = pygame.font.Font(font_path, 48) 
        font_table = pygame.font.Font(font_path, 32) 

    # --- MVT State Variables ---
    total_memory_size = 0
    # memory_map holds dynamic blocks: [{'start': 0, 'size': X, 'status': 'FREE' or 'P1'}]
    memory_map = []
    
    state = 0 
    total_mem_input = ""
    proc_size_input = ""
    error_message = ""
    log_message = "Initialize system capacity to begin."
    process_counter = 1

    # Main UI loop
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        back_surf_idle = font_setup.render("< BACK", True, NEON_GREEN)
        back_rect = back_surf_idle.get_rect(topleft=(30, 650))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_rect.collidepoint(mouse_pos):
                        running = False
                        return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return

                # STEP 1: Input Total Memory Capacity for MVT pool
                if state == 0:  
                    if event.key == pygame.K_RETURN:
                        raw = total_mem_input.strip()
                        if raw != "":
                            try:
                                val = int(raw)
                                if val <= 0:
                                    error_message = "Capacity must be greater than 0!"
                                    raise ValueError
                                
                                total_memory_size = val
                                # Initialize total memory pool as one single free segment
                                memory_map = [{'start': 0, 'size': total_memory_size, 'status': 'FREE'}]
                                state = 1
                                error_message = ""
                                log_message = f"System initialized with {total_memory_size} units."
                            except ValueError:
                                if not error_message:
                                    error_message = "Enter a valid positive integer!"
                        else:
                            error_message = "Input cannot be empty!"
                    elif event.key == pygame.K_BACKSPACE:
                        total_mem_input = total_mem_input[:-1]
                    else:
                        if event.unicode.isdigit():
                            total_mem_input += event.unicode

                # STEP 2: Input Process Size, Allocate via Best-Fit or Trigger Compaction
                elif state == 1:  
                    if event.key == pygame.K_RETURN:
                        raw_size = proc_size_input.strip()
                        if raw_size != "":
                            try:
                                requested_size = int(raw_size)
                                if requested_size <= 0:
                                    raise ValueError

                                p_name = f"P{process_counter}"
                                allocated = False
                                
                                # loop to handle potential retry after compaction
                                while True:
                                    best_idx = -1
                                    smallest_fit = float('inf')

                                    # Scan for Best-Fit block
                                    for i, block in enumerate(memory_map):
                                        if block['status'] == 'FREE' and block['size'] >= requested_size:
                                            if block['size'] < smallest_fit:
                                                smallest_fit = block['size']
                                                best_idx = i

                                    # Allocate if found
                                    if best_idx != -1:
                                        target = memory_map[best_idx]
                                        if target['size'] == requested_size:
                                            target['status'] = p_name
                                        else:
                                            # Dynamically slice the variable partition
                                            new_block = {'start': target['start'], 'size': requested_size, 'status': p_name}
                                            target['start'] += requested_size
                                            target['size'] -= requested_size
                                            memory_map.insert(best_idx, new_block)
                                        
                                        log_message = f"Allocated {p_name} ({requested_size} units) using Best-Fit."
                                        process_counter += 1
                                        allocated = True
                                        error_message = ""
                                        break
                                    
                                    # If Best-Fit fails, calculate total combined free space remaining
                                    total_free = sum(b['size'] for b in memory_map if b['status'] == 'FREE')
                                    if total_free >= requested_size:
                                        # Compaction Logic: Shift all allocated segments contiguously up to the top
                                        log_message = "No single block fits. Compacting memory segments..."
                                        allocated_blocks = [b for b in memory_map if b['status'] != 'FREE']
                                        
                                        new_map = []
                                        current_addr = 0
                                        for b in allocated_blocks:
                                            b['start'] = current_addr
                                            new_map.append(b)
                                            current_addr += b['size']
                                            
                                        if total_free > 0:
                                            new_map.append({'start': current_addr, 'size': total_free, 'status': 'FREE'})
                                            
                                        memory_map = new_map
                                        # Loop executes again to drop the process into the freshly compacted bottom block
                                        continue 
                                    else:
                                        error_message = f"Out of memory! {p_name} is too large."
                                        log_message = f"Allocation failed for {p_name}."
                                        break

                                proc_size_input = ""
                            except ValueError:
                                error_message = "Enter a valid positive process size!"
                        else:
                            error_message = "Please enter a process size!"
                    
                    # Manual Deallocation hotkey for simulation versatility
                    elif event.key == pygame.K_d:
                        # Deallocates the earliest active process found to simulate fragmented space holes
                        for block in memory_map:
                            if block['status'] != 'FREE':
                                target_p = block['status']
                                block['status'] = 'FREE'
                                log_message = f"Deallocated {target_p} manually."
                                break
                        
                        # Dynamic MVT merging: combine adjacent free blocks immediately
                        i = 0
                        while i < len(memory_map) - 1:
                            if memory_map[i]['status'] == 'FREE' and memory_map[i+1]['status'] == 'FREE':
                                memory_map[i]['size'] += memory_map[i+1]['size']
                                memory_map.pop(i+1)
                            else:
                                i += 1
                                
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

        # Header Title
        title_surface = font_title.render("MEMORY MANAGEMENT: Best-Fit MVT (Variable Partitions)", True, BLACK if background else NEON_GREEN)
        screen.blit(title_surface, (20, 10))

        # Render Content States
        if state == 0:
            txt1 = "Initialize Variable Partition Total Memory Capacity"
            txt2 = "Enter total system memory units available"
            txt3 = "(e.g., 500 or 1000):"
            txt4 = f"[{total_mem_input}]"

            surf1 = font_input.render(txt1, True, NEON_GREEN)
            surf2 = font_input.render(txt2, True, NEON_GREEN)
            surf3 = font_input.render(txt3, True, NEON_GREEN)
            surf4 = font_input.render(txt4, True, WHITE)

            screen.blit(surf1, surf1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120)))
            screen.blit(surf2, surf2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)))
            screen.blit(surf3, surf3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))
            screen.blit(surf4, surf4.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)))
            
            if error_message:
                err_surf = font_title.render(error_message, True, RED)
                screen.blit(err_surf, err_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160)))

        elif state == 1:
            txt1 = f"Total System Memory Managed: {total_memory_size} Units"
            txt2 = f"Enter Incoming Process Size:  [{proc_size_input}]"
            txt3 = "Press [ENTER] to Allocate | Press [D] to Deallocate Oldest Process"
            
            surf1 = font_input.render(txt1, True, NEON_GREEN)
            surf2 = font_input.render(txt2, True, WHITE)
            surf3 = font_table.render(txt3, True, NEON_GREEN)
            log_surf = font_table.render(f"System Log: {log_message}", True, NEON_GREEN)

            screen.blit(surf1, surf1.get_rect(center=(SCREEN_WIDTH // 2, 75)))
            screen.blit(surf2, surf2.get_rect(center=(SCREEN_WIDTH // 2, 125)))
            screen.blit(surf3, surf3.get_rect(center=(SCREEN_WIDTH // 2, 170)))
            screen.blit(log_surf, log_surf.get_rect(center=(SCREEN_WIDTH // 2, 210)))

            if error_message:
                err_surf = font_title.render(error_message, True, RED)
                screen.blit(err_surf, err_surf.get_rect(center=(SCREEN_WIDTH // 2, 245)))

            # --- DYNAMIC SCALE RENDERING OF VARIABLE MEMORY MAP ---
            map_width = 400
            total_render_height = 320
            start_x = (SCREEN_WIDTH - map_width) // 2
            start_y = 280
            
            for block in memory_map:
                # Proportional scaling calculations for clean variable box rendering
                pixel_y = start_y + int((block['start'] / total_memory_size) * total_render_height)
                pixel_h = int((block['size'] / total_memory_size) * total_render_height)
                
                # Minimum height safety check so thin partitions remain readable
                if pixel_h < 25: 
                    pixel_h = 25
                    
                block_rect = pygame.Rect(start_x, pixel_y, map_width, pixel_h)
                
                if block['status'] != 'FREE':
                    # Active process styling (RED box with cross lines matching template styling)
                    pygame.draw.rect(screen, RED, block_rect, 2)
                    pygame.draw.line(screen, RED, (start_x, pixel_y), (start_x + map_width, pixel_y + pixel_h), 1)
                    pygame.draw.line(screen, RED, (start_x, pixel_y + pixel_h), (start_x + map_width, pixel_y), 1)
                    
                    info_text = f"{block['status']} ({block['size']} units)"
                    info_surf = font_table.render(info_text, True, RED)
                    screen.blit(info_surf, info_surf.get_rect(center=block_rect.center))
                    
                    # MVT tracking variables on right side margins
                    loc_text = f"Range: {block['start']}-{block['start']+block['size']}"
                    loc_surf = font_table.render(loc_text, True, RED)
                    screen.blit(loc_surf, (start_x + map_width + 15, pixel_y + (pixel_h // 2) - 12))
                else:
                    # Available Segment Hole styling (NEON_GREEN layout boundaries)
                    pygame.draw.rect(screen, NEON_GREEN, block_rect, 2)
                    info_surf = font_table.render(f"FREE HOLE ({block['size']} units)", True, NEON_GREEN)
                    screen.blit(info_surf, info_surf.get_rect(center=block_rect.center))
                    
                    loc_text = f"Start Addr: {block['start']}"
                    loc_surf = font_table.render(loc_text, True, NEON_GREEN)
                    screen.blit(loc_surf, (start_x - 220, pixel_y + (pixel_h // 2) - 12))

        # Navigation Controls Panel Rendering
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
    baf_menu(test_screen)