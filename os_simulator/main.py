# Main entry point for the OS Simulator application
# Main menu scene loop

import pygame
import sys
import os

# Import Developer Credits Screen Panel
from meet_the_devs import show_devs

# Import the topic-specific algorithm menu modules for the simulator
from algorithms.virtual_memory.vm_pygame import main_vm_menu
from algorithms.memory_management.mm_main_menu import mm_main_menu
from algorithms.cpu_scheduling.cpu_scheduling_pygame import main_cpu_menu
from algorithms.disk_management.dm_pygame import main_disk_menu
# Constants & Configurations
NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Operating System Simulator")
    clock = pygame.time.Clock()

    # Load shared system background canvas asset
    try:
        background = pygame.image.load("os_simulator\\components\\background.png").convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        background = None

    # Load system retro font face
    font_path = "os_simulator\\components\\VT323-Regular.ttf"
    if not os.path.exists(font_path):
        print(f"CRITICAL ERROR: Font asset '{font_path}' was not found.")
        pygame.quit()
        sys.exit()

    font_header = pygame.font.Font(font_path, 95)
    font_button = pygame.font.Font(font_path, 60)
    font_back = pygame.font.Font(font_path, 46)

    # State controller engine: 0 = Main Menu, 1 = Topic Selector Dashboard
    current_menu_state = 0

    # UI Mapping Collections
    main_menu_options = [
        ("[1] Start", 1), 
        ("[2] Meet the Devs", "DEVS"),
        ("[3] Exit", "EXIT")
    ]

    topic_menu_options = [
        ("[1] CPU Scheduling", "CPU"),
        ("[2] Memory Management", "MM"),
        ("[3] Virtual Memory", "VM"),
        ("[4] Disk Management", "DISK")
    ]

    def build_buttons(options_list, base_y, gap_y=62, width=600):
        rects = []
        center_x = SCREEN_WIDTH // 2 - width // 2
        for i, (text, action) in enumerate(options_list):
            rect = pygame.Rect(center_x, base_y + (i * gap_y), width, 55)
            rects.append((rect, text, action))
        return rects

    main_buttons = build_buttons(main_menu_options, base_y=340, width=400)
    topic_buttons = build_buttons(topic_menu_options, base_y=320, width=550)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        back_surf_idle = font_back.render("< BACK", True, NEON_GREEN)
        back_rect = back_surf_idle.get_rect(topleft=(30, 650))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left Click
                    if current_menu_state == 0:
                        for rect, text, action in main_buttons:
                            if rect.collidepoint(mouse_pos):
                                if action == 1:
                                    current_menu_state = 1
                                elif action == "DEVS":
                                    show_devs(screen)
                                elif action == "EXIT":
                                    pygame.quit()
                                    sys.exit()
                    
                    elif current_menu_state == 1:
                        if back_rect.collidepoint(mouse_pos):
                            current_menu_state = 0
                        
                        for rect, text, action in topic_buttons:
                            if rect.collidepoint(mouse_pos):
                                if action == "CPU":
                                    main_cpu_menu()
                                    pygame.display.set_caption("Operating System Simulator")
                                    
                                elif action == "MM":
                                    mm_main_menu(screen)
                                    pygame.display.set_caption("Operating System Simulator")
                                    
                                elif action == "VM":
                                    main_vm_menu()
                                    pygame.display.set_caption("Operating System Simulator")
                                    
                                elif action == "DISK":
                                    main_disk_menu()
                                    pygame.display.set_caption("Operating System Simulator")


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_menu_state == 1:
                        current_menu_state = 0
                    else:
                        pygame.quit()
                        sys.exit()

        # Render Core Screen Graphics Layer
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)

        # Draw Dynamic Component Context Headers
        title_text = "OPERATING SYSTEM SIMULATOR"
        title_surf = font_header.render(title_text, True, NEON_GREEN)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 170))
        screen.blit(title_surf, title_rect)

        # Draw Screen Layout Title Separation Line Rule
        pygame.draw.line(screen, NEON_GREEN, (150, 240), (SCREEN_WIDTH - 150, 240), 3)

        # Draw State Machine Buttons Views
        if current_menu_state == 0:
            for rect, text, action in main_buttons:
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, NEON_GREEN, rect, 0, 4)
                    txt_surf = font_button.render(text, True, BLACK)
                else:
                    txt_surf = font_button.render(text, True, NEON_GREEN)
                screen.blit(txt_surf, txt_surf.get_rect(center=rect.center))

        elif current_menu_state == 1:
            for rect, text, action in topic_buttons:
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, NEON_GREEN, rect, 0, 4)
                    txt_surf = font_button.render(text, True, BLACK)
                else:
                    txt_surf = font_button.render(text, True, NEON_GREEN)
                screen.blit(txt_surf, txt_surf.get_rect(center=rect.center))

            # Render Dashboard Back Button Option
            if back_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, NEON_GREEN, back_rect.inflate(10, 5), 0, 4)
                back_surf = font_back.render("< BACK", True, BLACK)
            else:
                back_surf = font_back.render("< BACK", True, NEON_GREEN)
            screen.blit(back_surf, back_rect.topleft)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()