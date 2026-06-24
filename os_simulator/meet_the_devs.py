# GUI Implementation of the "Meet the Developers" credits view pane for the OS Simulator.

import pygame
import sys
import os

# Constants & Configurations
NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def show_devs(screen):
    """
    Renders the credits view pane.
    Only the back button is interactive.
    """
    clock = pygame.time.Clock()

    # Load Background Asset
    try:
        background = pygame.image.load("os_simulator\\components\\background.png").convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        background = None

    # Load font path configuration limits
    font_path = "os_simulator\\components\\VT323-Regular.ttf"
    if not os.path.exists(font_path):
        print(f"CRITICAL ERROR: Font asset '{font_path}' was not found.")
        pygame.quit()
        sys.exit()

    font_header = pygame.font.Font(font_path, 100)
    font_name = pygame.font.Font(font_path, 35)
    font_role = pygame.font.Font(font_path, 28)
    font_footer = pygame.font.Font(font_path, 32)
    font_back = pygame.font.Font(font_path, 46)

    # Developer Bio Matrix Map
    dev_team = [
        {"name": "[1] Marwilson A. Dela Cruz", "role": "CPU Scheduling Simulator Developer", "col": 0, "row": 0},
        {"name": "[2] Althea Mariell C. De Lara", "role": "Memory Management Simulator Developer", "col": 0, "row": 1},
        {"name": "[3] Amalia S. Kadoi", "role": "Virtual Memory Simulator Developer", "col": 1, "row": 0},
        {"name": "[4] Shella Mae M. Talamor", "role": "Disk Scheduling Simulator Developer", "col": 1, "row": 1}
    ]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
 
        back_surf_idle = font_back.render("< BACK", True, NEON_GREEN)
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
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    running = False
                    return

        # Render Panel Canvas Graphics
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)

        # 1. Main Content Module Title
        title_surf = font_header.render("MEET THE DEVELOPERS", True, NEON_GREEN)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surf, title_rect)

        # Horizontal Divider bar
        pygame.draw.line(screen, NEON_GREEN, (150, 215), (SCREEN_WIDTH - 150, 215), 3)

        # 2. Map Developer Bio Grid Layout Positions
        col1_center_x = SCREEN_WIDTH // 4 + 40
        col2_center_x = (SCREEN_WIDTH // 4) * 3 - 40
        row_y_starts = [290, 410]

        for dev in dev_team:
            target_x = col1_center_x if dev["col"] == 0 else col2_center_x
            target_y = row_y_starts[dev["row"]]

            name_surf = font_name.render(dev["name"], True, NEON_GREEN)
            role_surf = font_role.render(dev["role"], True, NEON_GREEN)

            screen.blit(name_surf, name_surf.get_rect(center=(target_x, target_y)))
            screen.blit(role_surf, role_surf.get_rect(center=(target_x, target_y + 35)))

        # 3. Footer Class/Group Matrix Label Info
        f_line1 = font_footer.render("2nd Year Computer Engineering Students", True, NEON_GREEN)
        f_line2 = font_footer.render("BSCpE 2-6 | Group 3", True, NEON_GREEN)
        f_line3 = font_footer.render("Polytechnic University of the Philippines", True, NEON_GREEN)

        screen.blit(f_line1, f_line1.get_rect(center=(SCREEN_WIDTH // 2, 560)))
        screen.blit(f_line2, f_line2.get_rect(center=(SCREEN_WIDTH // 2, 600)))
        screen.blit(f_line3, f_line3.get_rect(center=(SCREEN_WIDTH // 2, 640)))

        # 4. Interactive Back Button Box Hover Settings
        if back_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, NEON_GREEN, back_rect.inflate(10, 5), 0, 4)
            back_surf = font_back.render("< BACK", True, BLACK)
        else:
            back_surf = font_back.render("< BACK", True, NEON_GREEN)
        screen.blit(back_surf, back_rect.topleft)

        pygame.display.flip()
        clock.tick(30)