# Disk Scheduling Menu Simulator using Pygame
import pygame
import sys
import os

# Import algorithm paths
# Ipinapalagay nito na ang iyong mga file ay pinangalanang fcfs, sstf, scan, cscan, look, at clook
try:
    from .fcfs_disk import fcfs_menu
    from .sstf import sstf_menu
    from .scan import scan_menu
    from .cscan import cscan_menu
    from .look import look_menu
    from .clook import clook_menu
except ImportError:
    from fcfs_disk import fcfs_menu
    from sstf import sstf_menu
    from scan import scan_menu
    from cscan import cscan_menu
    from look import look_menu
    from clook import clook_menu

# Constants & Configurations
NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def main_disk_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Disk Scheduling Algorithms Simulator")
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

    # Menu Options Mapping para sa Disk Scheduling
    menu_options = [
        ("[1] First-Come, First-Served (FCFS)", fcfs_menu),
        ("[2] Shortest Seek Time First (SSTF)", sstf_menu),
        ("[3] SCAN Scheduling (Elevator)", scan_menu),
        ("[4] Circular SCAN Scheduling (C-SCAN)", cscan_menu),
        ("[5] LOOK Scheduling Algorithm", look_menu),
        ("[6] Circular LOOK Scheduling (C-LOOK)", clook_menu)
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
                            # Ipapasa ang kasalukuyang screen para hindi mag-flicker o mag-reopen ang window
                            func(screen)
                            # Ibalik ang orihinal na pamagat pagbalik galing sa sub-algorithm modules
                            pygame.display.set_caption("Disk Scheduling Algorithms Simulator")

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
        title_surf = font_header.render("DISK SCHEDULING", True, NEON_GREEN)
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
    main_disk_menu()