import pygame
import sys
import os

NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def ff_no_compaction_logic(screen):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("First-Fit MVT Algorithm (No Compaction)")
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

    total_memory_size = 0
    memory_map = []
    
    state = 0 
    total_mem_input = ""
    proc_size_input = ""
    error_message = ""
    log_message = "Initialize system capacity to begin."
    process_counter = 1

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
                if event.button == 1 and back_rect.collidepoint(mouse_pos):
                    running = False
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return

                if state == 0:  
                    if event.key == pygame.K_RETURN:
                        raw = total_mem_input.strip()
                        if raw != "":
                            try:
                                val = int(raw)
                                if val <= 0: raise ValueError
                                total_memory_size = val
                                memory_map = [{'start': 0, 'size': total_memory_size, 'status': 'FREE'}]
                                state = 1
                                error_message = ""
                                log_message = f"System initialized with {total_memory_size} units."
                            except ValueError:
                                error_message = "Enter a valid positive integer!"
                        else:
                            error_message = "Input cannot be empty!"
                    elif event.key == pygame.K_BACKSPACE:
                        total_mem_input = total_mem_input[:-1]
                    elif event.unicode.isdigit():
                        total_mem_input += event.unicode

                elif state == 1:  
                    if event.key == pygame.K_RETURN:
                        raw_size = proc_size_input.strip()
                        if raw_size != "":
                            try:
                                requested_size = int(raw_size)
                                if requested_size <= 0: raise ValueError
                                p_name = f"P{process_counter}"
                                first_idx = -1

                                # Linearly find the absolute first hole available
                                for i, block in enumerate(memory_map):
                                    if block['status'] == 'FREE' and block['size'] >= requested_size:
                                        first_idx = i
                                        break

                                if first_idx != -1:
                                    target = memory_map[first_idx]
                                    if target['size'] == requested_size:
                                        target['status'] = p_name
                                    else:
                                        new_block = {'start': target['start'], 'size': requested_size, 'status': p_name}
                                        target['start'] += requested_size
                                        target['size'] -= requested_size
                                        memory_map.insert(first_idx, new_block)
                                    
                                    log_message = f"Allocated {p_name} ({requested_size} units) using First-Fit."
                                    process_counter += 1
                                    error_message = ""
                                else:
                                    # Dropping instantaneous rejection (No Compaction)
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
                        i = 0
                        while i < len(memory_map) - 1:
                            if memory_map[i]['status'] == 'FREE' and memory_map[i+1]['status'] == 'FREE':
                                memory_map[i]['size'] += memory_map[i+1]['size']
                                memory_map.pop(i+1)
                            else: i += 1
                                
                    elif event.key == pygame.K_BACKSPACE:
                        proc_size_input = proc_size_input[:-1]
                    elif event.unicode.isdigit():
                        proc_size_input += event.unicode

        if background: screen.blit(background, (0, 0))
        else: screen.fill(BLACK)

        title_surface = font_title.render("MEMORY MANAGEMENT: First-Fit MVT (No Compaction)", True, BLACK if background else NEON_GREEN)
        screen.blit(title_surface, (20, 10))

        if state == 0:
            txt1, txt2, txt3 = "Initialize Variable Partition Total Memory Capacity", "Enter total system memory units available", "(e.g., 500 or 1000):"
            txt4 = f"[{total_mem_input}]"
            surf1, surf2, surf3, surf4 = font_input.render(txt1, True, NEON_GREEN), font_input.render(txt2, True, NEON_GREEN), font_input.render(txt3, True, NEON_GREEN), font_input.render(txt4, True, NEON_GREEN)
            screen.blit(surf1, surf1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120)))
            screen.blit(surf2, surf2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)))
            screen.blit(surf3, surf3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))
            screen.blit(surf4, surf4.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)))
            if error_message:
                err_surf = font_title.render(error_message, True, RED)
                screen.blit(err_surf, err_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160)))

        elif state == 1:
            txt1, txt2, txt3 = f"Total System Memory Managed: {total_memory_size} Units", f"Enter Incoming Process Size:  [{proc_size_input}]", "Press [ENTER] to Allocate | Press [D] to Deallocate Oldest Process"
            surf1, surf2, surf3 = font_input.render(txt1, True, NEON_GREEN), font_input.render(txt2, True, NEON_GREEN), font_table.render(txt3, True, NEON_GREEN)
            log_surf = font_table.render(f"System Log: {log_message}", True, NEON_GREEN)
            screen.blit(surf1, surf1.get_rect(center=(SCREEN_WIDTH // 2, 75)))
            screen.blit(surf2, surf2.get_rect(center=(SCREEN_WIDTH // 2, 125)))
            screen.blit(surf3, surf3.get_rect(center=(SCREEN_WIDTH // 2, 170)))
            screen.blit(log_surf, log_surf.get_rect(center=(SCREEN_WIDTH // 2, 210)))

            if error_message:
                err_surf = font_title.render(error_message, True, RED)
                screen.blit(err_surf, err_surf.get_rect(center=(SCREEN_WIDTH // 2, 245)))

            map_width, total_render_height, start_x, start_y = 400, 320, (SCREEN_WIDTH - 400) // 2, 280
            for block in memory_map:
                pixel_y = start_y + int((block['start'] / total_memory_size) * total_render_height)
                pixel_h = int((block['size'] / total_memory_size) * total_render_height)
                if pixel_h < 12: pixel_h = 12
                block_rect = pygame.Rect(start_x, pixel_y, map_width, pixel_h)
                
                dynamic_size = max(10, min(32, int(pixel_h * 0.6)))
                block_font = pygame.font.Font(font_path, dynamic_size) if font_exists else pygame.font.SysFont("monospace", dynamic_size)
                
                if block['status'] != 'FREE':
                    pygame.draw.rect(screen, RED, block_rect, 2)
                    pygame.draw.line(screen, RED, (start_x, pixel_y), (start_x + map_width, pixel_y + pixel_h), 1)
                    pygame.draw.line(screen, RED, (start_x, pixel_y + pixel_h), (start_x + map_width, pixel_y), 1)
                    info_text = f"{block['status']} ({block['size']} units)"
                    info_surf = block_font.render(info_text, True, RED)
                    screen.blit(info_surf, info_surf.get_rect(center=block_rect.center))
                    loc_surf = font_table.render(f"Range: {block['start']}-{block['start']+block['size']}", True, RED)
                    screen.blit(loc_surf, (start_x + map_width + 15, pixel_y + (pixel_h // 2) - 12))
                else:
                    pygame.draw.rect(screen, NEON_GREEN, block_rect, 2)
                    info_text = f"FREE HOLE ({block['size']} units)"
                    info_surf = block_font.render(info_text, True, NEON_GREEN)
                    screen.blit(info_surf, info_surf.get_rect(center=block_rect.center))
                    loc_surf = font_table.render(f"Start Addr: {block['start']}", True, NEON_GREEN)
                    screen.blit(loc_surf, (start_x - 220, pixel_y + (pixel_h // 2) - 12))

        if back_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, NEON_GREEN, back_rect.inflate(10, 5), 0, 4)
            back_surface = font_setup.render("< BACK", True, BLACK)
        else: back_surface = font_setup.render("< BACK", True, NEON_GREEN)
        screen.blit(back_surface, back_rect.topleft)
        pygame.display.flip()
        clock.tick(30)