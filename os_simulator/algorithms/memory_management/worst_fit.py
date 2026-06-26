import pygame
import sys
import os
from worst_fit_compaction import wf_compaction_logic
from worst_fit_no_compaction import wf_no_compaction_logic

# Constants & Configurations
NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen Size Dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def wf_menu(screen):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Best-Fit Algorithm")
    clock = pygame.time.Clock()

    # Load Background Canvas
    try:
        background = pygame.image.load("os_simulator\\components\\background.png").convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        background = None

    # Load Font
    font_path = "os_simulator\\components\\VT323-Regular.ttf"
    if not os.path.exists(font_path):
        print(f"CRITICAL ERROR: Font asset '{font_path}' was not found.")
        pygame.quit()
        sys.exit()

    font_header = pygame.font.Font(font_path, 100)
    font_button = pygame.font.Font(font_path, 38)
    font_back = pygame.font.Font(font_path, 46)

    # Menu Options Mapping
    menu_options = [
        ("[1] With Compaction", wf_compaction_logic),
        ("[2] Without Compaction", wf_no_compaction_logic),
    ]

    # Pre-calculate positions to create clean hover/click boundaries
    button_rects = []
    start_y = 260
    gap_y = 65
    button_width = 800
    button_height = 45
    center_x = SCREEN_WIDTH // 2 - button_width // 2

    for idx, (text, func) in enumerate(menu_options):
        rect = pygame.Rect(center_x, start_y + (idx * gap_y), button_width, button_height)
        button_rects.append((rect, text, func))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        back_surf_idle = font_back.render("< BACK", True, NEON_GREEN)
        back_rect = back_surf_idle.get_rect(topleft=(30, 650))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left Click Action Node
                    if back_rect.collidepoint(mouse_pos):
                        running = False
                        return

                    for rect, text, func in button_rects:
                        if rect.collidepoint(mouse_pos):
                            # Pass the screen variable into your standalone module loops
                            func(screen)
                            # Restore window caption limits after returning from sub-modules
                            pygame.display.set_caption("Worst Fit (MVT)")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return

        # Render Background Graphics
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)

        # 1. Main Title Header Render
        title_surf = font_header.render("Best-Fit Algorithm", True, NEON_GREEN)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surf, title_rect)

        # Draw Title Horizontal Divider Line
        pygame.draw.line(screen, NEON_GREEN, (150, 210), (SCREEN_WIDTH - 150, 210), 3)

        # 2. Interactive Highlights Loop Mapping
        for rect, text, func in button_rects:
            is_hovered = rect.collidepoint(mouse_pos)

            if is_hovered:
                # Hovered State: Solid Neon Green container box, text becomes Black
                pygame.draw.rect(screen, NEON_GREEN, rect, 0, 4)
                text_surf = font_button.render(text, True, BLACK)
            else:
                # Idle State: Transparent box background, text stays Neon Green
                text_surf = font_button.render(text, True, NEON_GREEN)

            # Center text perfectly inside the target box boundaries
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        # Render Back Button Option
        if back_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, NEON_GREEN, back_rect.inflate(10, 5), 0, 4)
            back_surf = font_back.render("< BACK", True, BLACK)
        else:
            back_surf = font_back.render("< BACK", True, NEON_GREEN)
        screen.blit(back_surf, back_rect.topleft)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    test_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    wf_menu(test_screen)



    def mvt_settings(self):
         if self.memory_size is None:
             while True:
                try:
                    memory_size_input = input("Enter total memory block size: ").strip()
                    if int(memory_size_input) <= 0:
                        raise ValueError
                    
                    else:
                        self.memory_size=int(memory_size_input)
                        break
                except:
                    print("Memory size should only be positive integers. Please input a valid number.")
        
         while True:
            try:
                process_size_input = input("enter process size: ").strip()
                burst_time_input = input("enter burst time: ").strip()

                if int(process_size_input) > 0 and int(burst_time_input) > 0:
                    self.add_process(process_size_input, burst_time_input)
                    break
                    
                elif int(process_size_input) <= 0 or int(burst_time_input) <= 0:
                    raise ValueError
                
            except:
                print("Process size and burst time should be positive integers. Please input valid numbers.")  


    def mvt_logic(self, compaction_enabled=False):
        if self.mvt_free_segments is None:
            self.mvt_free_segments = [[0, self.memory_size]]

        for dynamic_job in self.jobs:
            if dynamic_job["allocated_partition"] is not None:
                continue

            best_segment_pos = -1
            for seg_idx, target_segment in enumerate(self.mvt_free_segments):
                if target_segment[1] >= dynamic_job["size"]:
                    if best_segment_pos == -1 or target_segment[1] < self.mvt_free_segments[best_segment_pos][1]:
                        best_segment_pos = seg_idx
            

            if best_segment_pos == -1 and compaction_enabled:
                total_free_space = sum(segment[1] for segment in self.mvt_free_segments)
                if total_free_space >= dynamic_job["size"]:
                    print(f"\n[Compaction Triggered for {dynamic_job['process_id']}]")
                    
                    used_space_boundary = self.memory_size - total_free_space
                    self.mvt_free_segments = [[used_space_boundary, total_free_space]]
                    
                    best_segment_pos = 0

            if best_segment_pos != -1:
                matched_seg = self.mvt_free_segments[best_segment_pos]
                dynamic_job["allocated_partition"] = f"Address Range {matched_seg[0]} to {matched_seg[0] + dynamic_job['size']}"
                dynamic_job["fragmentation"] = 0
                
                if matched_seg[1] == dynamic_job["size"]:
                    self.mvt_free_segments.pop(best_segment_pos)
                else:
                    matched_seg[0] += dynamic_job["size"] # Increment starting address
                    matched_seg[1] -= dynamic_job["size"] # Reduce chunk capacity 
            else:
                dynamic_job["allocated_partition"] = "Not Allocated"