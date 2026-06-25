# First-Fit Memory Management Algorithm
import pygame
import sys
import os

# Constants & Configurations
NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen Size Dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def ff_menu(screen):
    pygame.init()
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
        title_surface = font_title.render("MEMORY MANAGEMENT: First-Fit Algorithm", True, BLACK)
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
    pygame.display.set_caption("Memory Management First Fit Algorithm")
    ff_menu(main_screen)

class FirstFit:
    def __init__(self):
        self.memory_size = None
        self.jobs=[]


    def add_process(self, process_size_input, burst_time_input):
        process_number = len(self.jobs) + 1
        process_data = {
                        "process_id": f"P{process_number}",
                        "size": int(process_size_input),
                        "burst_time": int(burst_time_input),
                        "allocated_partition": None,
                        "fragmentation": 0}
        
        self.jobs.append(process_data)


    def mft_settings(self):
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
    

    def mft_logic(self):
        print("\nMFT Allocation Simulation\n")
        partition_occupied = [False] * len(self.memory_size)
        
        for job in self.jobs:
            allocated = False
            for index, part_size in enumerate(self.memory_size):
                if part_size >= job["size"] and not partition_occupied[index]:
                    internal_frag = part_size - job["size"]
                    job["allocated_partition"] = f"Partition {index + 1} ({part_size})"
                    job["fragmentation"] = internal_frag
                    partition_occupied[index] = True
                    allocated = True
                    print(f"{job['process_id']} (Size {job['size']}) allocated to Partition {index + 1} (Size {part_size}). Fragmentation: {internal_frag}")
                    break  # Stop searching for this job; move to the next one
        
            if not allocated:
                job["allocated_partition"] = "Wait / Unallocated"
                job["fragmentation"] = "N/A"
                print(f"{job['process_id']} (Size {job['size']}) must WAIT. No matching free partition available.")

        print("\n" + "="*60)
        print(f"{'Job ID':<10}{'Size':<10}{'Burst':<10}{'Allocated To':<22}{'Frag':<10}")
        print("="*60)
        for job in self.jobs:
            print(f"{job['process_id']:<10}{job['size']:<10}{job['burst_time']:<10}{str(job['allocated_partition']):<22}{str(job['fragmentation']):<10}")
        print("="*60)


    def mvt_settings(self):
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
                process_size_input= input("enter process size: ").strip()
                burst_time_input= input("enter burst time: ").strip()

                if int(process_size_input) > 0 and int(burst_time_input) > 0:
                    self.add_process(process_size_input, burst_time_input)
                    
                elif int(process_size_input) <= 0 or int(burst_time_input) <= 0:
                    raise ValueError
                
            except:
                print("Process size and burst time should be positive integers. Please input valid numbers.")  


    def mvt_logic(self, compaction_enabled=False):
        print(f"\nMVT Allocation Simulation (Compaction Enabled: {compaction_enabled})\n")
        
        total_memory_capacity = self.memory_size
        # Tracks memory dynamically: [start_address, block_size, status]
        memory_map = [[0, total_memory_capacity, "FREE"]]
        
        for job in self.jobs:
            allocated = False
            for index, block in enumerate(memory_map):
                start_address, block_size, status = block
                if status == "FREE" and block_size >= job["size"]:
                    job["allocated_partition"] = f"Address {start_address}"
                    job["fragmentation"] = 0
                    memory_map[index] = [start_address, job["size"], job["process_id"]]
                    leftover_space = block_size - job["size"]

                    if leftover_space > 0:
                        new_free_start = start_address + job["size"]
                        memory_map.insert(index + 1, [new_free_start, leftover_space, "FREE"])

                    allocated = True
                    print(f" {job['process_id']} allocated at Address {start_address} (Carved {job['size']} KB)")
                    break 

            if not allocated and compaction_enabled:
                print(f"Space for {job['process_id']} is not contiguous. Triggering Compaction...")
                
                current_address = 0
                new_memory_map = []
                total_free_space = 0

                for start, size, status in memory_map:
                    if status != "FREE":
                        new_memory_map.append([current_address, size, status])
                        
                        # Update the specific job's address in our tracking ledger since it just moved
                        for target_job in self.jobs:
                            if target_job["process_id"] == status:
                                target_job["allocated_partition"] = f"Address {current_address}"
                        
                        current_address += size
                    else:
                        total_free_space += size

                if total_free_space > 0:
                    new_memory_map.append([current_address, total_free_space, "FREE"])
                
                memory_map = new_memory_map

                for index, block in enumerate(memory_map):
                    start_address, block_size, status = block
                    if status == "FREE" and block_size >= job["size"]:
                        job["allocated_partition"] = f"Address {start_address}"
                        job["fragmentation"] = 0
                        memory_map[index] = [start_address, job["size"], job["process_id"]]
                        leftover_space = block_size - job["size"]

                        if leftover_space > 0:
                            new_free_start = start_address + job["size"]
                            memory_map.insert(index + 1, [new_free_start, leftover_space, "FREE"])

                        allocated = True
                        print(f"{job['process_id']} successfully allocated at Address {start_address} AFTER compaction!")
                        break

            if not allocated:
                job["allocated_partition"] = "Wait (External Frag)"
                job["fragmentation"] = "N/A"
                print(f" {job['process_id']} (Size {job['size']}) must WAIT. No free block is large enough.")

        print("\n" + "="*60)
        print(f"{'Job ID':<10}{'Size':<10}{'Burst':<10}{'Allocated To':<22}{'Internal Frag':<10}")
        print("="*60)
        for job in self.jobs:
            print(f"{job['process_id']:<10}{job['size']:<10}{job['burst_time']:<10}{str(job['allocated_partition']):<22}{str(job['fragmentation']):<10}")
        print("="*60)

# definitions
def user_input(first_fit):
    while True:
        try:
            memory_type_input=input("Enter memory type (MFT/MVT):").strip()
            if memory_type_input.upper()=="MFT":
                first_fit.mft_settings()
            elif memory_type_input.upper()=="MVT":
                first_fit.mvt_settings()
            else:
                raise ValueError

        except:
            print("Invalid input. Please enter 'MFT' or 'MVT'")
            continue

# main program
if __name__ == "__main__":
    first_fit = FirstFit()
    print("Welcome to the First-Fit Memory Management Algorithm Simulator!")
    user_input(first_fit)