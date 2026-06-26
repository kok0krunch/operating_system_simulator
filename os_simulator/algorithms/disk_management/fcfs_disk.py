# First-Come, First-Served (FCFS) Disk Scheduling Algorithm
import pygame
import sys


pygame.init()

WIDTH = 1280
HEIGHT = 720

#class FCFS
class FCFSDiskScheduling:

    def __init__(self, head, requests):
        self.head = head
        self.requests = requests

    def compute(self):

        total_movement = 0
        sequence = [self.head]

        current = self.head

        for request in self.requests:
            total_movement += abs(current - request)
            current = request
            sequence.append(current)

        return total_movement, sequence

#Draw arrow
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

#Main Program
def fcfs_menu(screen):
    pygame.display.set_caption("FCFS Disk Scheduling")
    clock = pygame.time.Clock()

    NEON_GREEN = (57, 255, 20)
    BLACK = (0, 0, 0)

    # Assets
    try:
        background = pygame.image.load("os_simulator\\components\\background.png")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        font_title = pygame.font.Font("os_simulator\\components\\VT323-Regular.ttf", 36)
        font_large = pygame.font.Font("os_simulator\\components\\VT323-Regular.ttf", 46)
        font_small = pygame.font.Font("os_simulator\\components\\VT323-Regular.ttf", 28)
    except pygame.error:
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill((20, 20, 20))
        font_title = pygame.font.SysFont("Courier", 36)
        font_large = pygame.font.SysFont("Courier", 46)
        font_small = pygame.font.SysFont("Courier", 28)

    # Screens
    HEAD_INPUT = 0
    REQUEST_INPUT = 1
    RESULT_SCREEN = 2

    current_screen = HEAD_INPUT

    head_text = ""
    request_text = ""

    head = 0
    requests = []
    sequence = []
    total_head_movement = 0

    # Static back button bounding box
    back_rect = pygame.Rect(30, 650, 130, 40)

    # interactive back button
    def draw_interactive_back(mouse_pos):
        if back_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, NEON_GREEN, back_rect.inflate(10, 5), 0, 4)
            back_surf = font_large.render("< BACK", True, BLACK)
        else:
            back_surf = font_large.render("< BACK", True, NEON_GREEN)
        screen.blit(back_surf, back_rect.topleft)

    # Draw head screen
    def draw_head_screen(mouse_pos):
        screen.blit(background, (0, 0))
        title = font_title.render("DISK SCHEDULING: First-Come, First-Serve", True, BLACK)
        screen.blit(title, (20, 10))
        label = font_large.render("Input initial head position:", True, NEON_GREEN)
        screen.blit(label, (380, 280))
        value = font_large.render(head_text, True, NEON_GREEN)
        text_rect = value.get_rect(center=(WIDTH // 2, 360))
        screen.blit(value, text_rect)
        draw_interactive_back(mouse_pos)

    # Draw request screen
    def draw_request_screen(mouse_pos):
        screen.blit(background, (0, 0))
        title = font_title.render("DISK SCHEDULING: First-Come, First-Serve", True, BLACK)
        screen.blit(title, (20, 10))
        label = font_large.render("Input disk requests (comma separated):", True, NEON_GREEN)
        screen.blit(label, label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        
        display_text = f"{request_text}"
        value = font_large.render(display_text, True, NEON_GREEN)
        screen.blit(value, value.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
        draw_interactive_back(mouse_pos)

    #Draw graph
    def draw_graph():
        if len(sequence) == 0:
            return

        graph_width = 1000
        start_x = (WIDTH - graph_width) // 2
        end_x = start_x + graph_width
        axis_y = 120

        pygame.draw.line(screen, NEON_GREEN, (start_x, axis_y), (end_x, axis_y), 3)

        max_value = max(sequence) if max(sequence) > 0 else 1

        #Draw cylinder markers
        for value in sequence:
            x = start_x + (value / max_value) * (end_x - start_x)
            pygame.draw.line(screen, NEON_GREEN, (x, 105), (x, 135), 4)

            label = font_small.render(str(value), True, NEON_GREEN)
            screen.blit(label, label.get_rect(center=(x, 70)))

        #Draw head movement
        base_y = 200
        step_y = 40

        for i in range(len(sequence) - 1):
            current = sequence[i]
            nxt = sequence[i + 1]

            x1 = start_x + (current / max_value) * (end_x - start_x)
            x2 = start_x + (nxt / max_value) * (end_x - start_x)

            y1 = base_y + i * step_y
            y2 = base_y + (i + 1) * step_y

            draw_arrow(screen, NEON_GREEN, (x1, y1), (x2, y2))

    # Draw result screen
    def draw_result_screen():
        screen.blit(background, (0, 0))
        title = font_title.render("DISK SCHEDULING: First-Come, First-Serve", True, BLACK)
        screen.blit(title, (20, 10))

        draw_graph()

        total = font_large.render(f"Total Head Movement: {total_head_movement}", True, NEON_GREEN)
        screen.blit(total, total.get_rect(center=(WIDTH // 2, 630)))

        prompt = font_title.render("Press [ESCAPE] to start a new calculation", True, NEON_GREEN)
        screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, 675)))

    # Game loop
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_rect.collidepoint(mouse_pos):
                        if current_screen == HEAD_INPUT:
                            running = False
                            return
                        elif current_screen in [REQUEST_INPUT]:
                            current_screen -= 1


            elif event.type == pygame.KEYDOWN:
                # Head input screen
                if current_screen == HEAD_INPUT:
                    if event.key == pygame.K_RETURN:
                        if head_text.strip() != "":
                            try:
                                head = int(head_text)
                                current_screen = REQUEST_INPUT
                            except ValueError:
                                pass
                    elif event.key == pygame.K_BACKSPACE:
                        head_text = head_text[:-1]
                    elif event.unicode.isdigit():
                        head_text += event.unicode

                # Request input screen
                elif current_screen == REQUEST_INPUT:
                    if event.key == pygame.K_RETURN:
                        try:
                            requests = [int(x.strip()) for x in request_text.split(",") if x.strip() != ""]
                            if len(requests) > 0:
                                fcfs = FCFSDiskScheduling(head, requests)
                                total_head_movement, sequence = fcfs.compute()
                                current_screen = RESULT_SCREEN
                        except ValueError:
                            pass
                    elif event.key == pygame.K_BACKSPACE:
                        request_text = request_text[:-1]
                    else:
                        allowed = "0123456789, "
                        if event.unicode in allowed:
                            request_text += event.unicode

                # Result Screen
                elif current_screen == RESULT_SCREEN:
                    if event.key == pygame.K_ESCAPE:
                        head_text = ""
                        request_text = ""
                        sequence = []
                        total_head_movement = 0
                        current_screen = HEAD_INPUT

        if current_screen == HEAD_INPUT:
            draw_head_screen(mouse_pos)
        elif current_screen == REQUEST_INPUT:
            draw_request_screen(mouse_pos)
        elif current_screen == RESULT_SCREEN:
            draw_result_screen()

        pygame.display.flip()
        clock.tick(60)

# entry point
if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    fcfs_menu(screen)