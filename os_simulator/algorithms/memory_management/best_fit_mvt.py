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
    pygame.display.set_caption("Best-Fit Algorithm (MVT)")
    clock = pygame.time.Clock()

    # Load resources with fallbacks
    try:
        background = pygame.image.load("os_simulator\\components\\background.png").convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        background = None

    # Load the uploaded VT323-Regular.ttf font file explicitly
    font_path = "os_simulator\\components\\VT323-Regular.ttf"
    if not os.path.exists(font_path):
        print(f"CRITICAL ERROR: The font file '{font_path}' was not found in the directory.")
        pygame.quit()
        sys.exit()

    # Define font instances
    font_title = pygame.font.Font(font_path, 36) 
    font_setup = pygame.font.Font(font_path, 46) 
    font_input = pygame.font.Font(font_path, 48) 
    font_table = pygame.font.Font(font_path, 32) 

    # Main UI loop
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Pre-create the < BACK button interaction area at the bottom left coordinates
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

        # Rendering Background Graphics
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)

        # 1. Top Left Header Panel
        title_surface = font_title.render("MEMORY MANAGEMENT: Best-Fit Algorithm (MVT)", True, BLACK)
        screen.blit(title_surface, (20, 10))

        # 2. Setup Screen Interactions 
       
        # 3. Output
           
        # 4. Render the Interactive < BACK Button (Visible on ALL states/outputs)
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
