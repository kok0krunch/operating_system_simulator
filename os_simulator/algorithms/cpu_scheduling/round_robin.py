# Round Robin Scheduling Algorithm

import pygame
import sys
import os

NEON_GREEN = (57, 255, 20)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid  
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

def run_round_robin(process_list, time_quantum):
    unarrived = [Process(p.pid, p.arrival_time, p.burst_time) for p in process_list]
    ready_queue = []
    completed = []
    gantt_log = [] 
    
    current_time = 0
    
    # Sort unarrived processes initially by arrival time
    unarrived.sort(key=lambda x: x.arrival_time)
    
    while unarrived or ready_queue:
        # Move arrived processes to the ready queue
        arrived = [p for p in unarrived if p.arrival_time <= current_time]
        for p in arrived:
            ready_queue.append(p)
            unarrived.remove(p)
            
        if not ready_queue:
            # CPU Idle block handles gaps between arrivals
            next_arrival = min([p.arrival_time for p in unarrived])
            gantt_log.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue
            
        curr = ready_queue.pop(0)
        start_t = current_time
        
        # Determine execution duration based on remaining time and quantum slice
        exec_time = min(curr.remaining_time, time_quantum)
        
        # Run execution step by step to allow new arrivals to jump in properly mid-slice
        for _ in range(exec_time):
            current_time += 1
            curr.remaining_time -= 1
            
            # Check for any new processes arriving during this clock unit tick
            mid_arrived = [p for p in unarrived if p.arrival_time <= current_time]
            for p in mid_arrived:
                ready_queue.append(p)
                unarrived.remove(p)
                
        gantt_log.append((f"P{curr.pid}", start_t, current_time))
        
        if curr.remaining_time > 0:
            # If the process isn't done, it goes back to the tail of the queue
            ready_queue.append(curr)
        else:
            # Process completes execution
            curr.completion_time = current_time
            curr.turnaround_time = curr.completion_time - curr.arrival_time
            curr.waiting_time = curr.turnaround_time - curr.burst_time
            completed.append(curr)
            
    return completed, gantt_log

def rr_menu(screen):
    pygame.init()
    clock = pygame.time.Clock()
    
    # Try Loading Background Component
    try:
        background = pygame.image.load("os_simulator\\components\\background.png").convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        background = None
    
    # Verify Font Asset Integrity
    font_path = "os_simulator\\components\\VT323-Regular.ttf"
    if not os.path.exists(font_path):
        print(f"CRITICAL ERROR: The font file '{font_path}' was not found in the directory.")
        pygame.quit()
        sys.exit()
    
    # Initialize UI elements with custom TTF asset
    font_title = pygame.font.Font(font_path, 36) 
    font_setup = pygame.font.Font(font_path, 46) 
    font_input = pygame.font.Font(font_path, 48) 
    font_table = pygame.font.Font(font_path, 32) 
    
    # Navigation & Logic Variables
    state = 0  # 0: Process Count Input, 1: Time Quantum Input, 2: Process Specifications Entry, 3: Analytics Dashboard
    process_count = 0
    time_quantum = 1
    process_data = [] 
    
    # Structural Input Buffers
    count_input = ""
    quantum_input = ""
    specs_input = ""
    current_entry_index = 0 
    input_field_index = 0   # 0: Arrival Time, 1: Burst Time
    temp_specs = [None, None] 
    error_message = ""
    
    # Simulation Output Registers
    completed_jobs = []
    gantt_timeline = []
    avg_tat = 0.0
    avg_wt = 0.0

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Render Background Layer
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)
        
        # Top Left Header Panel
        title_surface = font_title.render("CPU SCHEDULING: Round-Robin Algorithm", True, BLACK)
        screen.blit(title_surface, (20, 10))
        
        # Pre-create the < BACK button interaction area
        back_surf_idle = font_setup.render("< BACK", True, NEON_GREEN)
        back_rect = back_surf_idle.get_rect(topleft=(30, 650))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left Click
                    if back_rect.collidepoint(mouse_pos):
                        if state == 0:
                            running = False
                            return
                        else:
                            # Step rewind logic
                            if state == 3:
                                state = 2
                            elif state == 2:
                                if len(process_data) == process_count:
                                    process_data = []
                                current_entry_index = 0
                                input_field_index = 0
                                temp_specs = [None, None]
                                state = 1
                                quantum_input = str(time_quantum)
                            elif state == 1:
                                state = 0
                                count_input = str(process_count)
                            error_message = ""
                            continue
                            
                    if state == 2 and len(process_data) == process_count:
                        # Calculation trigger boundary box
                        eval_rect = pygame.Rect(490, 240, 300, 50)
                        if eval_rect.collidepoint(mouse_pos):
                            completed_jobs, gantt_timeline = run_round_robin(process_data, time_quantum)
                            
                            avg_tat = sum([p.turnaround_time for p in completed_jobs]) / len(completed_jobs)
                            avg_wt = sum([p.waiting_time for p in completed_jobs]) / len(completed_jobs)
                            state = 3

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return

                if state == 0:  # Process Count Input
                    if event.key == pygame.K_RETURN:
                        raw = count_input.strip()
                        if raw != "":
                            try:
                                count = int(raw)
                                if count <= 0 or count > 6: 
                                    raise ValueError
                                process_count = count
                                count_input = ""
                                state = 1
                                error_message = ""
                            except ValueError:
                                error_message = "Invalid Count (1 - 6)!"
                        else:
                            error_message = "Input cannot be empty!"
                    elif event.key == pygame.K_BACKSPACE:
                        count_input = count_input[:-1]
                    else:
                        if event.unicode.isdigit():
                            count_input += event.unicode

                elif state == 1:  # Time Quantum Input
                    if event.key == pygame.K_RETURN:
                        raw = quantum_input.strip()
                        if raw != "":
                            try:
                                quant = int(raw)
                                if quant <= 0:
                                    raise ValueError
                                time_quantum = quant
                                quantum_input = ""
                                process_data = []
                                current_entry_index = 0
                                input_field_index = 0
                                temp_specs = [None, None]
                                state = 2
                                error_message = ""
                            except ValueError:
                                error_message = "Time Quantum must be greater than 0!"
                        else:
                            error_message = "Input cannot be empty!"
                    elif event.key == pygame.K_BACKSPACE:
                        quantum_input = quantum_input[:-1]
                    else:
                        if event.unicode.isdigit():
                            quantum_input += event.unicode

                elif state == 2 and current_entry_index < process_count:  # Process Matrix Row Population
                    if event.key == pygame.K_RETURN:
                        raw = specs_input.strip()
                        if raw != "":
                            try:
                                val = int(raw)
                                if val < 0:
                                    raise ValueError
                                temp_specs[input_field_index] = val
                                specs_input = ""
                                error_message = ""
                                
                                if input_field_index < 1:
                                    input_field_index += 1
                                else:
                                    process_data.append(Process(current_entry_index + 1, temp_specs[0], temp_specs[1]))
                                    current_entry_index += 1
                                    input_field_index = 0
                                    temp_specs = [None, None]
                            except ValueError:
                                error_message = "Values must be valid positive integers!"
                        else:
                            error_message = "Value cannot be empty!"
                    elif event.key == pygame.K_BACKSPACE:
                        specs_input = specs_input[:-1]
                    else:
                        if event.unicode.isdigit():
                            specs_input += event.unicode
                            
                elif state == 3:  # End Evaluation Reset
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        state = 0
                        count_input = ""
                        quantum_input = ""
                        specs_input = ""
                        process_data = []
                        completed_jobs = []
                        gantt_timeline = []

        # State Rendering Engine
        if state == 0:
            txt1 = "Initialize the CPU Scheduling Workspace Parameters"
            txt2 = "Enter the number of active processes to evaluate (Max 6):"
            txt3 = f"[ {count_input} ]"

            surf1 = font_input.render(txt1, True, NEON_GREEN)
            surf2 = font_input.render(txt2, True, NEON_GREEN)
            surf3 = font_input.render(txt3, True, NEON_GREEN) 

            screen.blit(surf1, surf1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 110)))
            screen.blit(surf2, surf2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
            screen.blit(surf3, surf3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 95)))

            if error_message:
                err_surf = font_title.render(error_message, True, RED)
                screen.blit(err_surf, err_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180)))
                
        elif state == 1:
            # Set up Time Quantum Field Input View
            hdr_str = f"WORKSPACE CAPACITY SIZE: {process_count} JOBS"
            hdr_surf = font_table.render(hdr_str, True, RED)
            screen.blit(hdr_surf, (50, 75))

            txt1 = "Set Global Round-Robin Execution Time Slice"
            txt2 = "Enter Time Quantum (TQ) parameter value:"
            txt3 = f"[ {quantum_input} ]"

            surf1 = font_input.render(txt1, True, NEON_GREEN)
            surf2 = font_input.render(txt2, True, NEON_GREEN)
            surf3 = font_input.render(txt3, True, NEON_GREEN)

            screen.blit(surf1, surf1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 110)))
            screen.blit(surf2, surf2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
            screen.blit(surf3, surf3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 95)))

            if error_message:
                err_surf = font_title.render(error_message, True, RED)
                screen.blit(err_surf, err_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180)))

        elif state == 2:
            # Table Input View: Populate Configuration Rows
            fields = ["Arrival Time", "Burst Time"]
            hdr_str = f"ALGORITHM: ROUND-ROBIN | TQ: {time_quantum} | JOBS COUNT: {process_count}"
            hdr_surf = font_table.render(hdr_str, True, RED)
            screen.blit(hdr_surf, (50, 75))
            
            if current_entry_index < process_count:
                txt1 = f"Enter {fields[input_field_index]} for Process [ P{current_entry_index + 1} ]:"
                txt2 = f"[ {specs_input} ]"
                
                surf1 = font_input.render(txt1, True, NEON_GREEN)
                surf2 = font_input.render(txt2, True, NEON_GREEN)
                screen.blit(surf1, (50, 120))
                screen.blit(surf2, (50, 175))
            else:
                eval_rect = pygame.Rect(490, 240, 300, 50)
                if eval_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, NEON_GREEN, eval_rect, 0, 4)
                exec_txt = font_setup.render("SEE GANTT CHART", True, BLACK if eval_rect.collidepoint(mouse_pos) else NEON_GREEN)
                exec_rect = exec_txt.get_rect(center=eval_rect.center)
                screen.blit(exec_txt, exec_rect)
                
            if error_message:
                err_surf = font_table.render(error_message, True, RED)
                screen.blit(err_surf, (50, 225))
                
            # Dynamic Data Grid Layout Configuration
            start_x, start_y = 240, 320
            col_widths = [240, 280, 280]
            row_height = 40
            
            headers = ["Process ID", "Arrival Time", "Burst Time"]
            for idx, h in enumerate(headers):
                h_surf = font_table.render(h, True, NEON_GREEN)
                screen.blit(h_surf, (start_x + sum(col_widths[:idx]), start_y))
                
            pygame.draw.line(screen, NEON_GREEN, (start_x, start_y + 30), (SCREEN_WIDTH - start_x, start_y + 30), 1)
            
            for r_idx in range(process_count):
                curr_y = start_y + 40 + (r_idx * row_height)
                pid_lbl = f"P{r_idx + 1}"
                row_color = WHITE if r_idx == current_entry_index else (NEON_GREEN if r_idx < current_entry_index else DARK_GRAY)
                
                p_surf = font_table.render(pid_lbl, True, row_color)
                screen.blit(p_surf, (start_x, curr_y))
                
                if r_idx < len(process_data):
                    val_at = str(process_data[r_idx].arrival_time)
                    val_bt = str(process_data[r_idx].burst_time)
                elif r_idx == current_entry_index:
                    val_at = str(temp_specs[0]) if temp_specs[0] is not None else ("?" if input_field_index == 0 else "")
                    val_bt = str(temp_specs[1]) if temp_specs[1] is not None else ("?" if input_field_index == 1 else "")
                else:
                    val_at, val_bt = "-", "-"
                    
                screen.blit(font_table.render(val_at, True, row_color), (start_x + col_widths[0], curr_y))
                screen.blit(font_table.render(val_bt, True, row_color), (start_x + col_widths[0] + col_widths[1], curr_y))

        elif state == 3:
            # Diagram Simulation Grid Map Layout (Gantt Chart View)
            gantt_y = 100
            gantt_box_height = 50
            chart_max_width = 1100
            chart_start_x = 90
            
            total_duration = gantt_timeline[-1][2] if gantt_timeline else 1
            lbl_g = font_table.render("GANTT TIMELINE CHART SIMULATION BLOCK:", True, NEON_GREEN)
            screen.blit(lbl_g, (chart_start_x, gantt_y))
            
            box_start_y = gantt_y + 35
            
            for pid, start_t, end_t in gantt_timeline:
                seg_pct = (end_t - start_t) / total_duration
                box_width = int(seg_pct * chart_max_width)
                box_x = chart_start_x + int((start_t / total_duration) * chart_max_width)
                
                block_rect = pygame.Rect(box_x, box_start_y, box_width, gantt_box_height)
                pygame.draw.rect(screen, RED if pid == "IDLE" else NEON_GREEN, block_rect, 2)
                
                id_surf = font_table.render(pid, True, RED if pid == "IDLE" else NEON_GREEN)
                screen.blit(id_surf, id_surf.get_rect(center=block_rect.center))
                
                t_surf = font_table.render(str(start_t), True, NEON_GREEN)
                screen.blit(t_surf, (box_x, box_start_y + gantt_box_height + 2))
                
            if gantt_timeline:
                last_t_surf = font_table.render(str(gantt_timeline[-1][2]), True, NEON_GREEN)
                screen.blit(last_t_surf, (chart_start_x + chart_max_width - 15, box_start_y + gantt_box_height + 2))
                
            # Analytics Metric Computations Table Layout
            calc_start_y = 265
            col_c_widths = [160, 160, 160, 220, 220, 200]
            calc_x = 90
            
            headers_c = ["Job ID", "Arrival", "Burst", "Completion", "Turnaround", "Waiting"]
            for idx, hc in enumerate(headers_c):
                hc_surf = font_table.render(hc, True, NEON_GREEN)
                screen.blit(hc_surf, (calc_x + sum(col_c_widths[:idx]), calc_start_y))
                
            pygame.draw.line(screen, NEON_GREEN, (calc_x, calc_start_y + 30), (SCREEN_WIDTH - calc_x, calc_start_y + 30), 1)
            
            completed_jobs.sort(key=lambda x: x.pid)
            for r_idx, job in enumerate(completed_jobs):
                row_y = calc_start_y + 40 + (r_idx * 35)
                metrics_text = [f"P{job.pid}", str(job.arrival_time), str(job.burst_time), str(job.completion_time), str(job.turnaround_time), str(job.waiting_time)]
                
                for c_idx, text in enumerate(metrics_text):
                    color = RED if job.turnaround_time > 15 else NEON_GREEN
                    m_surf = font_table.render(text, True, color)
                    screen.blit(m_surf, (calc_x + sum(col_c_widths[:c_idx]), row_y))
                    
            # Averages Summary Metrics Panel
            base_summary_y = calc_start_y + 40 + (len(completed_jobs) * 35) + 20
            pygame.draw.line(screen, RED, (calc_x, base_summary_y - 10), (SCREEN_WIDTH - calc_x, base_summary_y - 10), 1)
            
            avg_tat_str = f"Average Turnaround Time (TAT): {avg_tat:.2f} ms"
            avg_wt_str  = f"Average Waiting Time (WT):     {avg_wt:.2f} ms"
            
            screen.blit(font_table.render(avg_tat_str, True, NEON_GREEN), (calc_x, base_summary_y))
            screen.blit(font_table.render(avg_wt_str, True, NEON_GREEN), (calc_x, base_summary_y + 30))
            
            prompt_txt = "Press [SPACE] or [ENTER] to start a new calculation"
            prompt_surf = font_title.render(prompt_txt, True, NEON_GREEN)
            screen.blit(prompt_surf, prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, 620)))

        # Interactive < BACK Button
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
    pygame.display.set_caption("Round-Robin Framework Component")
    rr_menu(main_screen)