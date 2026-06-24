# Most Recently Used (MRU) Page Replacement Algorithm

import pygame
import sys
import os

# Constants & Configurations
NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen Size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def mru_menu(screen):
    """
    Main GUI function for MRU Page Replacement.
    Can be imported and called from another script.
    """
    pygame.init()
    clock = pygame.time.Clock()

    # Load resources with fallbacks
    try:
        background = pygame.image.load("os_simulator\\components\\background.png").convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        background = None

    # STRICT REQUIREMENT: Load the uploaded VT323-Regular.ttf font file explicitly
    font_path = "os_simulator\\components\\VT323-Regular.ttf"
    if not os.path.exists(font_path):
        print(f"CRITICAL ERROR: The font file '{font_path}' was not found in the directory.")
        print("Please place the 'VT323-Regular.ttf' file in the same folder as this script.")
        pygame.quit()
        sys.exit()

    # Define font instances strictly using the uploaded TTF file
    font_title = pygame.font.Font(font_path, 36) 
    font_setup = pygame.font.Font(font_path, 46) 
    font_input = pygame.font.Font(font_path, 48) # Kept at size 48 per your PR instruction
    font_table = pygame.font.Font(font_path, 32) 

    # State machine variables
    # States: 0 = Input Capacity, 1 = Input Pages, 2 = Display Simulation Table
    state = 0
    capacity_input = ""
    pages_input = ""
    error_message = ""

    # Simulation data variables
    capacity = 3
    page_sequence = []
    simulation_steps = []
    total_page_faults = 0

    def find_mru_index(frames, seq, current_idx, cap):
        # MRU Strategy: Look backward into the past to find which currently loaded frame 
        # was accessed most recently (closest to current_idx)
        most_recent_idx = -1
        index_to_replace = 0
        
        for frame_idx in range(cap):
            current_frame_page = frames[frame_idx]
            
            # Scan backward starting right before the current access item position
            for past_index in range(current_idx - 1, -1, -1):
                if seq[past_index] == current_frame_page:
                    if past_index > most_recent_idx:
                        most_recent_idx = past_index
                        index_to_replace = frame_idx
                    break
                    
        return index_to_replace

    def run_mru_simulation(seq, cap):
        nonlocal total_page_faults, simulation_steps
        frames = [None] * cap
        faults = 0
        steps = []

        for i, page in enumerate(seq):
            status = ""
            replaced_index = -1
            
            if page in frames:
                status = "HIT"
            else:
                faults += 1
                status = "FAULT"
                
                # Case 1: Fill empty slots sequentially first if available
                if None in frames:
                    replaced_index = frames.index(None)
                    frames[replaced_index] = page
                # Case 2: Memory is full. Run the MRU backward-looking tracking algorithm.
                else:
                    replaced_index = find_mru_index(frames, seq, i, cap)
                    frames[replaced_index] = page
            
            readable_frames = [str(f) if f is not None else "" for f in frames]
            steps.append({
                "page": page,
                "frames": list(readable_frames),
                "status": status,
                "new_index": replaced_index
            })
        
        total_page_faults = faults
        simulation_steps = steps

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
                if event.button == 1:  # Left Click
                    if back_rect.collidepoint(mouse_pos):
                        running = False
                        return
                       
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return

                if state == 0:  # Capacity Input Mode
                    if event.key == pygame.K_RETURN:
                        raw = capacity_input.strip()
                        if raw == "" or raw == "3":
                            capacity = 3
                            state = 1
                            error_message = ""
                        else:
                            try:
                                capacity = int(raw)
                                if capacity <= 0 or capacity > 7:
                                    raise ValueError
                                state = 1
                                error_message = ""
                            except ValueError:
                                error_message = "Invalid Capacity (Max 7)! Defaulting to 3"
                                capacity = 3
                                state = 1
                    elif event.key == pygame.K_BACKSPACE:
                        capacity_input = capacity_input[:-1]
                    else:
                        if event.unicode.isdigit():
                            capacity_input += event.unicode

                elif state == 1:  # Sequence Input Mode
                    if event.key == pygame.K_RETURN:
                        raw = pages_input.strip()
                        try:
                            page_sequence = [int(p.strip()) for p in raw.split(',') if p.strip() != ""]
                            if not page_sequence:
                                error_message = "Please enter at least one page number."
                            elif len(page_sequence) > 20:
                                error_message = "Sequence is too long! Keep it under 20 pages."
                            else:
                                error_message = ""
                                run_mru_simulation(page_sequence, capacity)
                                state = 2
                        except ValueError:
                            error_message = "Invalid format! Use commas (e.g., 7,0,1,2)."
                    elif event.key == pygame.K_BACKSPACE:
                        pages_input = pages_input[:-1]
                    else:
                        if event.unicode.isdigit() or event.unicode == ',':
                            pages_input += event.unicode
                            
                elif state == 2:  # Table Output View Mode
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        state = 0
                        capacity_input = ""
                        pages_input = ""
                        simulation_steps = []
                        total_page_faults = 0

        # Rendering Background Graphics
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)

        # 1. Top Left Header Panel Title
        title_surface = font_title.render("VIRTUAL MEMORY: Most Recently Used (MRU) Page Replacement", True, BLACK)
        screen.blit(title_surface, (20, 10))

        # 2. Setup Screen Interactions (Perfect spacing constraints using size 48 text)
        if state == 0:
            txt1 = "The default capacity is set to 3. You can change it by"
            txt2 = "entering a new value or type '3' to keep the default."
            txt3 = f"Enter new capacity of the page frames: {capacity_input}"

            surf1 = font_input.render(txt1, True, NEON_GREEN)
            surf2 = font_input.render(txt2, True, NEON_GREEN)
            surf3 = font_input.render(txt3, True, NEON_GREEN) 

            screen.blit(surf1, surf1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140)))
            screen.blit(surf2, surf2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))
            screen.blit(surf3, surf3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 95)))

        elif state == 1:
            txt1 = "Enter a list of page numbers to access"
            txt2 = "separated by comma (e.g., 7,0,1,2):"
            txt3 = f"[{pages_input}]"

            surf1 = font_input.render(txt1, True, NEON_GREEN)
            surf2 = font_input.render(txt2, True, NEON_GREEN)
            surf3 = font_input.render(txt3, True, NEON_GREEN) 

            screen.blit(surf1, surf1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140)))
            screen.blit(surf2, surf2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))
            screen.blit(surf3, surf3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 95)))

            if error_message:
                err_surf = font_title.render(error_message, True, NEON_GREEN)
                screen.blit(err_surf, err_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180)))

        elif state == 2:
            # 3. Diagram Simulation Grid Map Layout
            num_pages = len(simulation_steps)
            box_width = 55   
            box_height = 50  
            
            total_grid_width = num_pages * box_width
            start_x = (SCREEN_WIDTH - total_grid_width) // 2
            start_y = 180

            for idx, step in enumerate(simulation_steps):
                col_x = start_x + (idx * box_width)
                
                # Render Row References Top Headers
                pygame.draw.rect(screen, NEON_GREEN, (col_x, start_y, box_width, box_height), 2) 
                p_surf = font_table.render(str(step.get("page", "")), True, NEON_GREEN)
                screen.blit(p_surf, p_surf.get_rect(center=(col_x + box_width // 2, start_y + box_height // 2)))

                # Frames Block Rendering (Skips drawing frame blocks on Hits)
                if step.get("status") == "FAULT":
                    step_frames = step.get("frames", [""] * capacity)
                    new_idx = step.get("new_index", -1)
                    
                    for f_idx in range(capacity):
                        cell_y = start_y + (box_height + 30) + (f_idx * box_height)
                        pygame.draw.rect(screen, NEON_GREEN, (col_x, cell_y, box_width, box_height), 2)
                        
                        if f_idx < len(step_frames):
                            val = step_frames[f_idx]
                            if val != "":
                                color = RED if f_idx == new_idx else NEON_GREEN
                                f_surf = font_table.render(val, True, color)
                                screen.blit(f_surf, f_surf.get_rect(center=(col_x + box_width // 2, cell_y + box_height // 2)))

            # Centered Analysis Readout Summaries
            base_summary_y = start_y + (box_height + 60) + (capacity * box_height)
            
            faults_txt = f"Total Page Faults: {total_page_faults}"
            faults_surf = font_setup.render(faults_txt, True, NEON_GREEN) 
            screen.blit(faults_surf, faults_surf.get_rect(center=(SCREEN_WIDTH // 2, base_summary_y)))
            
            prompt_txt = "Press [SPACE] or [ENTER] to start a new calculation"
            prompt_surf = font_title.render(prompt_txt, True, NEON_GREEN)
            screen.blit(prompt_surf, prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, base_summary_y + 70)))
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
    main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Virtual Memory MRU Page Replacement")
    mru_menu(main_screen)