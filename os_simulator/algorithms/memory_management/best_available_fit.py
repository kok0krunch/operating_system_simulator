import pygame
import sys
import os

class BestAvailableFit:
    def __init__(self):
        self.memory_size = None
        self.jobs=[]
        self.partition_busy = None

    def add_process(self, process_size_input, burst_time_input):
        process_number = len(self.jobs) + 1
        process_data = {
                        "process_id": f"P{process_number}",
                        "size": int(process_size_input),
                        "burst_time": int(burst_time_input),
                        "allocated_partition": None,
                        "fragmentation": 0}
        
        self.jobs.append(process_data)

    def best_available_fit_settings(self):
        if self.memory_size is None:
            while True:
                try:
                    memory_size_input = input("Enter partitions separated with comma (ex. 1,2,3): ").strip()
                    memory_size_list = [int(size.strip()) for size in memory_size_input.split(',')]
                    for size in memory_size_list:
                        if int(size) <= 0:
                            raise ValueError
                        
                    self.memory_size=memory_size_list
                    break

                except:
                    print("Memory sizes should only be positive integers. Voiding initial inputs")

        while True:
            try:
                process_size_input= input("enter process size: ").strip()
                burst_time_input= input("enter burst time: ").strip()

                if int(process_size_input) > 0 and int(burst_time_input) > 0:
                    self.add_process(process_size_input, burst_time_input)
                    
                elif int(process_size_input) <= 0 or int(burst_time_input) <= 0:
                    raise ValueError
                
            except:
                print("Process size and burst time should be positive integers. Please input valid numbers.")  
    

    def best_available_fit_logic(self):
        mft_partitions = list(self.memory_size)
        partition_count = len(mft_partitions)
        if self.partition_busy is None:
            self.partition_busy = [False] * partition_count

        for job_item in self.jobs:
            if job_item["allocated_partition"] is not None:
                continue

            optimal_index = -1
            for block_index in range(partition_count):
                if mft_partitions[block_index] >= job_item["size"] and not self.partition_busy[block_index]:
                    if optimal_index == -1 or mft_partitions[block_index] < mft_partitions[optimal_index]:
                        optimal_index = block_index
            
            if optimal_index != -1:
                job_item["allocated_partition"] = optimal_index + 1
                job_item["fragmentation"] = mft_partitions[optimal_index] - job_item["size"]
                self.partition_busy[optimal_index] = True
            
            else:
                available_swap_index = -1
                for block_index in range(partition_count):
                    if mft_partitions[block_index] >= job_item["size"]:
                        if available_swap_index == -1 or mft_partitions[block_index] < mft_partitions[available_swap_index]:
                            available_swap_index = block_index
                
                if available_swap_index != -1:
                    for old_job in self.jobs:
                        if old_job["allocated_partition"] == available_swap_index + 1:
                            old_job["allocated_partition"] = "Swapped Out / Suspended"
                            old_job["fragmentation"] = 0
                    
                    print(f"\n[!] Partition {available_swap_index + 1} is busy. Swapping out old process to make it AVAILABLE for {job_item['process_id']}.")
                    job_item["allocated_partition"] = available_swap_index + 1
                    job_item["fragmentation"] = mft_partitions[available_swap_index] - job_item["size"]
                    self.partition_busy[available_swap_index] = True
                else:
                    job_item["allocated_partition"] = "Not Allocated (Too Large)"

# Constants & Configurations
NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen Size Dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def baf_menu(screen):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Best-Available-Fit Algorithm")
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

    def run_worst_fit():
        pass

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
        title_surface = font_title.render("MEMORY MANAGEMENT: Best-Available-Fit Algorithm", True, BLACK)
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
    main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Memory Management Best-Avaialble Fit Algorithm")
    baf_menu(main_screen)