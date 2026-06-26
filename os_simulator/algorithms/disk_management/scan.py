# SCAN Scheduling Algorithm - Elevator Algorithm
#import libraries
import pygame
import sys

pygame.init()

WIDTH = 1280
HEIGHT = 720

# Class for SCAN Scheduling
class SCANScheduling:
    def __init__(self, head, requests, disk_size, direction):
        self.head = head
        self.requests = requests
        self.disk_size = disk_size
        self.direction = direction.lower()

    def compute(self):
        total_movement = 0
        sequence = [self.head]
        current = self.head

        left = []
        right = []

        for request in self.requests:
            if request < current:
                left.append(request)
            else:
                right.append(request)

        left.sort()
        right.sort()

        if self.direction == "right":
            for request in right:
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

            total_movement += abs(current - (self.disk_size - 1))
            current = self.disk_size - 1
            sequence.append(current)

            for request in reversed(left):
                total_movement += abs(current - request)
                current = request
                sequence.append(current)
        else:
            for request in reversed(left):
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

            total_movement += abs(current - 0)
            current = 0
            sequence.append(current)

            for request in right:
                total_movement += abs(current - request)
                current = request
                sequence.append(current)

        return total_movement, sequence

# Draw arrow
def draw_arrow(surface, color, start, end):
    pygame.draw.line(surface, color, start, end, 1)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    
    if dx == 0 and dy == 0:
        return
        
    angle = pygame.math.Vector2(dx, dy).angle_to((1, 0))
    arrow_size = 10
    left = pygame.math.Vector2(arrow_size, 0).rotate(-angle + 150)
    right = pygame.math.Vector2(arrow_size, 0).rotate(-angle - 150)

    pygame.draw.line(surface, color, end, (end[0] + left.x, end[1] + left.y), 3)
    pygame.draw.line(surface, color, end, (end[0] + right.x, end[1] + right.y), 3)

# Main Program
def scan_menu(screen):
    clock = pygame.time.Clock()

    NEON_GREEN = (57, 255, 20)
    BLACK = (0, 0, 0)
    try:
        background = pygame.image.load("os_simulator\\components\\background.png")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        font_title = pygame.font.Font("os_simulator\\components\\VT323-Regular.ttf", 36)
        font_large = pygame.font.Font("os_simulator\\components\\VT323-Regular.ttf", 46)
        font_marker = pygame.font.Font("os_simulator\\components\\VT323-Regular.ttf", 18)
    except pygame.error:
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill((20, 20, 20))
        font_title = pygame.font.SysFont("Courier", 36)
        font_large = pygame.font.SysFont("Courier", 46)
        font_marker = pygame.font.SysFont("Courier", 18)

    # Screens
    HEAD_INPUT = 0
    REQUEST_INPUT = 1
    DISK_SIZE_INPUT = 2
    DIRECTION_INPUT = 3
    RESULT_SCREEN = 4

    current_screen = HEAD_INPUT

    # Variables
    head_text = ""
    request_text = ""
    disk_size_text = ""
    direction_text = ""

    head = 0
    requests = []
    disk_size = 0
    direction = ""

    sequence = []
    total_head_movement = 0

    back_rect = pygame.Rect(30, 650, 130, 40)

    def draw_interactive_back(mouse_pos):
        if back_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, NEON_GREEN, back_rect.inflate(10, 5), 0, 4)
            back_surf = font_large.render("< BACK", True, BLACK)
        else:
            back_surf = font_large.render("< BACK", True, NEON_GREEN)
        screen.blit(back_surf, back_rect.topleft)

    def draw_head_screen(mouse_pos):
        screen.blit(background, (0, 0))
        title = font_title.render("DISK SCHEDULING: SCAN", True, BLACK)
        screen.blit(title, (20, 10))
        label = font_large.render("Input initial head position:", True, NEON_GREEN)
        screen.blit(label, (380, 280))
        value = font_large.render(head_text, True, NEON_GREEN)
        text_rect = value.get_rect(center=(WIDTH // 2, 360))
        screen.blit(value, text_rect)
        draw_interactive_back(mouse_pos)

    def draw_request_screen(mouse_pos):
        screen.blit(background, (0, 0))
        title = font_title.render("DISK SCHEDULING: SCAN", True, BLACK)
        screen.blit(title, (20, 10))
        label = font_large.render("Input disk requests (comma separated):", True, NEON_GREEN)
        screen.blit(label, (250, 280))
        value = font_large.render(request_text, True, NEON_GREEN)
        screen.blit(value, (260, 340))
        draw_interactive_back(mouse_pos)

    def draw_disk_size_screen(mouse_pos):
        screen.blit(background, (0, 0))
        title = font_title.render("DISK SCHEDULING: SCAN", True, BLACK)
        screen.blit(title, (20, 10))
        label = font_large.render("Input Disk Size (e.g., 200):", True, NEON_GREEN)
        label_rect = label.get_rect(center=(WIDTH // 2, 280))
        screen.blit(label, label_rect)
        value = font_large.render(disk_size_text, True, NEON_GREEN)
        rect = value.get_rect(center=(WIDTH // 2, 360))
        screen.blit(value, rect)
        draw_interactive_back(mouse_pos)

    def draw_direction_screen(mouse_pos):
        screen.blit(background, (0, 0))
        title = font_title.render("DISK SCHEDULING: SCAN ", True, BLACK)
        screen.blit(title, (20, 10))
        label = font_large.render("Direction (left/right):", True, NEON_GREEN)
        screen.blit(label, (400, 280))
        value = font_large.render(direction_text, True, NEON_GREEN)
        rect = value.get_rect(center=(WIDTH // 2, 360))
        screen.blit(value, rect)
        draw_interactive_back(mouse_pos)

    def draw_graph():
        if len(sequence) == 0:
            return

        start_x = 100
        end_x = 1050
        axis_y = 120

        pygame.draw.line(screen, NEON_GREEN, (start_x, axis_y), (end_x, axis_y), 3)
        
        # Mas accurate gamitin ang disk_size para sa scaling ng disk graph
        max_val = disk_size if disk_size > 0 else max(sequence)

        for value in sequence:
            x = start_x + (value / max_val) * (end_x - start_x)
            pygame.draw.line(screen, NEON_GREEN, (x, 90), (x, 150), 4)
            # Pinalitan ang font_small ng font_marker
            label = font_marker.render(str(value), True, NEON_GREEN)
            screen.blit(label, (x - 10, 55))

        base_y = 200
        step_y = 40

        for i in range(len(sequence) - 1):
            current = sequence[i]
            nxt = sequence[i + 1]
            x1 = start_x + (current / max_val) * (end_x - start_x)
            x2 = start_x + (nxt / max_val) * (end_x - start_x)
            y1 = base_y + i * step_y
            y2 = base_y + (i + 1) * step_y
            draw_arrow(screen, NEON_GREEN, (x1, y1), (x2, y2))

    def draw_result_screen():
        screen.blit(background, (0, 0))
        title = font_title.render("DISK SCHEDULING: SCAN", True, BLACK)
        screen.blit(title, (20, 10))
        draw_graph()
        total = font_large.render(f"Total Head Movement: {total_head_movement}", True, NEON_GREEN)
        screen.blit(total, total.get_rect(center=(WIDTH // 2, 630)))
        prompt = font_title.render("Press [ESCAPE] to start a new calculation", True, NEON_GREEN)
        screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, 675)))

    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # MOUSE BUTTON DOWN Events (Ihiwalay sa Keyboard Events)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_rect.collidepoint(mouse_pos):
                        if current_screen == HEAD_INPUT:
                            running = False
                            return
                        elif current_screen in [REQUEST_INPUT, DISK_SIZE_INPUT, DIRECTION_INPUT]:
                            current_screen -= 1

            # KEYDOWN Events (Ito ang naging sanhi ng bug sa dating code)
            elif event.type == pygame.KEYDOWN:
                # Head input screen
                if current_screen == HEAD_INPUT:
                    if event.key == pygame.K_RETURN:
                        if head_text.strip() != "":
                            head = int(head_text)
                            current_screen = REQUEST_INPUT
                    elif event.key == pygame.K_BACKSPACE:
                        head_text = head_text[:-1]
                    elif event.unicode.isdigit():
                        head_text += event.unicode

                # Request input screen
                elif current_screen == REQUEST_INPUT:
                    if event.key == pygame.K_RETURN:
                        try:
                            requests = [int(x.strip()) for x in request_text.split(",") if x.strip() != ""]
                            current_screen = DISK_SIZE_INPUT
                        except ValueError:
                            pass
                    elif event.key == pygame.K_BACKSPACE:
                        request_text = request_text[:-1]
                    else:
                        allowed = "0123456789, "
                        if event.unicode in allowed:
                            request_text += event.unicode

                # Disk size input screen
                elif current_screen == DISK_SIZE_INPUT:
                    if event.key == pygame.K_RETURN:
                        if disk_size_text.strip() != "":
                            disk_size = int(disk_size_text)
                            current_screen = DIRECTION_INPUT
                    elif event.key == pygame.K_BACKSPACE:
                        disk_size_text = disk_size_text[:-1]
                    elif event.unicode.isdigit():
                        disk_size_text += event.unicode

                # Direction input screen
                elif current_screen == DIRECTION_INPUT:
                    if event.key == pygame.K_RETURN:
                        direction = direction_text.lower().strip()
                        if direction in ["left", "right"]:
                            scan = SCANScheduling(head, requests, disk_size, direction)
                            total_head_movement, sequence = scan.compute()
                            current_screen = RESULT_SCREEN
                    elif event.key == pygame.K_BACKSPACE:
                        direction_text = direction_text[:-1]
                    elif event.unicode.isalpha():
                        direction_text += event.unicode

                # Result screen
                elif current_screen == RESULT_SCREEN:
                    if event.key == pygame.K_ESCAPE:
                        head_text = ""
                        request_text = ""
                        disk_size_text = ""
                        direction_text = ""
                        sequence = []
                        total_head_movement = 0
                        current_screen = HEAD_INPUT

        # Render Screens
        if current_screen == HEAD_INPUT:
            draw_head_screen(mouse_pos)
        elif current_screen == REQUEST_INPUT:
            draw_request_screen(mouse_pos)
        elif current_screen == DISK_SIZE_INPUT:
            draw_disk_size_screen(mouse_pos)
        elif current_screen == DIRECTION_INPUT:
            draw_direction_screen(mouse_pos)
        elif current_screen == RESULT_SCREEN:
            draw_result_screen()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    scan_menu(screen)