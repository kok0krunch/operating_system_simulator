import pygame
import sys
import os

NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def bf_no_compaction_logic(screen):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Best Fit Simulator (MVT - Without Compaction)")
    clock = pygame.time.Clock()

    try:
        background = pygame.image.load("os_simulator\\components\\background.png").convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        background = None

    font_path = "os_simulator\\components\\VT323-Regular.ttf"
    font_exists = os.path.exists(font_path)

    if not font_exists:
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

                # STEP 1: Input Total Memory Capacity
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

                # STEP 2: Input Process Size & Allocation (Without Compaction)
                elif state == 1:  
                    if event.key == pygame.K_RETURN:
                        raw_size = proc_size_input.strip()
                        if raw_size != "":
                            try:
                                requested_size = int(raw_size)
                                if requested_size <= 0:
                                    raise ValueError

                                p_name = f"P{process_counter}"
                                best_idx = -1
                                smallest_fit = float('inf')

                                # Scan for Best-Fit block
                                for i, block in enumerate(memory_map):
                                    if block['status'] == 'FREE' and block['size'] >= requested_size:
                                        if block['size'] < smallest_fit:
                                            smallest_fit = block['size']
                                            best_idx = i

                                # Allocate if a single block fits
                                if best_idx != -1:
                                    target = memory_map[best_idx]
                                    if target['size'] == requested_size:
                                        target['status'] = p_name
                                    else:
                                        new_block = {'start': target['start'], 'size': requested_size, 'status': p_name}
                                        target['start'] += requested_size
                                        target['size'] -= requested_size
                                        memory_map.insert(best_idx, new_block)
                                    
                                    log_message = f"Allocated {p_name} ({requested_size} units) using Best-Fit."
                                    process_counter += 1
                                    error_message = ""
                                else:
                                    # No Compaction: Fail instantly when no single block fits
                                    error_message = f"Out of memory! {p_name} does not fit any hole."
                                    log_message = f"Allocation failed for {p_name} due to fragmentation."

                                proc_size_input = ""
                            except ValueError:
                                error_message = "Enter a valid positive process size!"
                        else:
                            error_message = "Please enter a process size!"
                    
                    elif event.key == pygame.K_d:
                        for block in memory_map:
                            if block['status'] != 'FREE':
                                target_p = block['status']
                                block['status'] = 'FREE'
                                log_message = f"Deallocated {target_p} manually."
                                break
                        
                        # Merge adjacent free blocks
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

        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)

        title_surface = font_title.render("MEMORY MANAGEMENT: Best Fit (MVT - Without Compaction)", True, BLACK if background else NEON_GREEN)
        screen.blit(title_surface, (20, 10))

        if state == 0:
            txt1 = "Initialize Variable Partition Total Memory Capacity"
            txt2 = "Enter total system memory units available"
            txt3 = "(e.g., 500 or 1000):"
            txt4 = f"[{total_mem_input}]"

            surf1 = font_input.render(txt1, True, NEON_GREEN)
            surf2 = font_input.render(txt2, True, NEON_GREEN)
            surf3 = font_input.render(txt3, True, NEON_GREEN)
            surf4 = font_input.render(txt4, True, NEON_GREEN) # Brackets and value entirely NEON_GREEN

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
            surf2 = font_input.render(txt2, True, NEON_GREEN) # Brackets and value entirely NEON_GREEN
            surf3 = font_table.render(txt3, True, NEON_GREEN)
            log_surf = font_table.render(f"System Log: {log_message}", True, NEON_GREEN)

            screen.blit(surf1, surf1.get_rect(center=(SCREEN_WIDTH // 2, 75)))
            screen.blit(surf2, surf2.get_rect(center=(SCREEN_WIDTH // 2, 125)))
            screen.blit(surf3, surf3.get_rect(center=(SCREEN_WIDTH // 2, 170)))
            screen.blit(log_surf, log_surf.get_rect(center=(SCREEN_WIDTH // 2, 210)))

            if error_message:
                err_surf = font_title.render(error_message, True, RED)
                screen.blit(err_surf, err_surf.get_rect(center=(SCREEN_WIDTH // 2, 245)))

            # --- DYNAMIC MEMORY RENDERING ---
            map_width = 400
            total_render_height = 320
            start_x = (SCREEN_WIDTH - map_width) // 2
            start_y = 280
            
            for block in memory_map:
                pixel_y = start_y + int((block['start'] / total_memory_size) * total_render_height)
                pixel_h = int((block['size'] / total_memory_size) * total_render_height)
                
                if pixel_h < 12: 
                    pixel_h = 12
                    
                block_rect = pygame.Rect(start_x, pixel_y, map_width, pixel_h)
                
                # Dynamic text scaling inside small memory partitions
                dynamic_size = max(10, min(32, int(pixel_h * 0.6)))
                
                if font_exists:
                    block_font = pygame.font.Font(font_path, dynamic_size)
                else:
                    block_font = pygame.font.SysFont("monospace", dynamic_size)
                
                if block['status'] != 'FREE':
                    pygame.draw.rect(screen, RED, block_rect, 2)
                    pygame.draw.line(screen, RED, (start_x, pixel_y), (start_x + map_width, pixel_y + pixel_h), 1)
                    pygame.draw.line(screen, RED, (start_x, pixel_y + pixel_h), (start_x + map_width, pixel_y), 1)
                    
                    info_text = f"{block['status']} ({block['size']} units)"
                    info_surf = block_font.render(info_text, True, RED)
                    screen.blit(info_surf, info_surf.get_rect(center=block_rect.center))
                    
                    loc_text = f"Range: {block['start']}-{block['start']+block['size']}"
                    loc_surf = font_table.render(loc_text, True, RED)
                    screen.blit(loc_surf, (start_x + map_width + 15, pixel_y + (pixel_h // 2) - 12))
                else:
                    pygame.draw.rect(screen, NEON_GREEN, block_rect, 2)
                    info_text = f"FREE HOLE ({block['size']} units)"
                    info_surf = block_font.render(info_text, True, NEON_GREEN)
                    screen.blit(info_surf, info_surf.get_rect(center=block_rect.center))
                    
                    loc_text = f"Start Addr: {block['start']}"
                    loc_surf = font_table.render(loc_text, True, NEON_GREEN)
                    screen.blit(loc_surf, (start_x - 220, pixel_y + (pixel_h // 2) - 12))

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
    bf_no_compaction_logic(test_screen)