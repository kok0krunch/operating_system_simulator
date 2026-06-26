# Operating System Simulator 🖥️

A comprehensive, interactive, and visually striking desktop application that simulates and visualizes core Operating System (OS) algorithms in real-time. Built entirely in Python using the **PyGame** framework, this simulator transforms abstract low-level OS mechanics into clear, step-by-step visual graphics.

This project was developed as an educational tool to analyze performance and behavioral differences across foundational system scheduling, memory optimization, allocation, and hardware abstraction algorithms.

---

## 🎨 Visual Preview & UI Concept
The application utilizes a retro-futuristic, high-visibility **Neon Green and Terminal Black cyber-grid style**. All components—including input validation fields, real-time metrics trackers, and execution timelines—are balanced, responsive, and dynamically centered for an optimized $1280 \times 720$ HD visual experience.

---

## 🚀 Key Features & Simulated Algorithms

The simulator provides isolated state-machine playgrounds for **four core pillars** of operating system infrastructure:

### 1. CPU Scheduling Simulator
Visualizes how an operating system controls process execution orders via dynamic Gantt charts, tracking **Waiting Time (WT)** and **Turnaround Time (TAT)**:
* **First-Come, First-Served (FCFS):** Non-preemptive, strict FIFO queue handling.
* **Shortest Job First (SJF):** Non-Preemptive and Preemptive (Shortest Remaining Time First / SRTF) process states.
* **Priority Scheduling:** Non-Preemptive and Preemptive sorting algorithms handling external process constraints.
* **Round Robin (RR):** Time-sliced context switching with custom Quantum inputs.

### 2. Memory Management Simulator
Simulates memory allocation, monitoring external fragmentation across contiguous partition spaces:
* **MFT (Multiprogramming with a Fixed number of Tasks):** Fixed boundaries running:
    * *Best-Fit Placement*
    * *First-Fit Placement*
    * *Best Available Fit Placement*
* **MVT (Multiprogramming with a Variable number of Tasks):** Dynamic partitions evaluating allocation with and without **Memory Compaction**:
    * *First-Fit Placement*
    * *Best-Fit Placement*
    * *Worst-Fit Placement*

### 3. Virtual Memory (Page Replacement) Simulator
Visualizes logical-to-physical mapping anomalies, highlighting memory page snapshots and identifying execution memory **Hits** versus **Faults**:
* **First-In, First-Out (FIFO):** Replaces the oldest loaded memory frame.
* **Optimal Page Replacement:** Swaps the frame that will not be accessed for the longest future duration (ideal lookahead strategy).
* **Least Recently Used (LRU):** Tracks execution history backward to evict the oldest accessed item.
* **Most Recently Used (MRU):** Targets the frame modified closest to the current operational index.
* **Least Frequently Used (LFU):** Monitors and keeps highly-referenced pages while evicting rare access frames.
* **Most Frequently Used (MFU):** Evicts heavily counted page references under the heuristic that freshly loaded pages require preservation.

### 4. Disk Management (Disk Scheduling) Simulator
Plots hardware I/O optimization strategies by visualizing dynamic seek paths and tracking total **Cylinder Head Movement**:
* **FCFS (First-Come, First-Served):** Processes arm movements exactly in order of hardware request arrivals.
* **SSTF (Shortest Seek Time First):** Service the request closest to the active head position to minimize near-term displacement.
* **SCAN (Elevator Algorithm):** Moves back and forth across the full length of the disk cylinders, picking up items in path vector.
* **C-SCAN (Circular SCAN):** Sweeps in one directional vector to the absolute edge, then snaps straight back to start zero to restart a uniform track scan.
* **LOOK / C-LOOK:** Enhanced variants of SCAN/C-SCAN that reverse or reset direction immediately upon clearing the *highest/lowest requested bounds*, saving unnecessary track travels.

---

## ⌨️ Control & Interaction Guide

The simulator features a responsive interface designed to feel like a vintage command-line terminal while remaining intuitive and accessible. Use the following global mappings to control all module parameters:

* **`Mouse Click [Left]`**: Activates navigation buttons, transitions between system layers, and selects specific algorithmic playgrounds.
* **`Keyboard [0-9]`**: Numerically inputs custom variables such as frame capacities, initial disk head tracks, or time quantum slices.
* **`Keyboard [,] (Comma)`**: Acts as a delimiter string token when typing index arrays (e.g., page reference sequences or disk location requests).
* **`[BACKSPACE]`**: Deletes the last entered character inside the input strings.
* **`[ENTER] / [RETURN]`**: Submits validated configuration strings and transitions into the calculation/graph visualization screens.
* **`[SPACE]`**: Resets completed tracking output charts to the initial state machine loop to begin a new simulation instantly.

---

## 👥 Development Team

This project was built by **Group 3** as an engineering visualization suite. All core modules, graphic render pipelines, and math engines were programmed collaboratively.
### 🎓 Laboratory Section
* **Course/Year**: 2nd Year Computer Engineering
* **Class Section**: BSCpE 2-6
* **Group Number**: Group 3
* **Institution**: Polytechnic University of the Philippines - Sta. Mesa
### 🛠️ Developer Allocations
* **Marwilson A. Dela Cruz** *Core CPU Scheduling Simulator Developer*
* **Althea Mariell C. De Lara** *Core Memory Management Simulator Developer*
* **Amalia S. Kadoi** *Core Virtual Memory Simulator Developer*
* **Shella Mae M. Talamor** *Core Disk Scheduling Simulator Developer*
---

## 🛠️ Project Structure & Architecture
The software is organized using modular packaging principles. The global controller orchestrates navigation transitions through atomic function calls, keeping algorithmic computation cleanly decoupled from layout loops.
```text
os_simulator/
│
├── algorithms/
│   ├── cpu_scheduling/                      # CPU Scheduling Visualizers
│       ├── cpu_scheduling_pygame.py
│       ├── fcfs_cpu.py
│       ├── priority.py
│       ├── round_robin.py
│       └── sjf.py      
│
│   ├── disk_management/                     # Disk Management Visualizers
│       ├── c-scan.py
│       ├── clook.py
│       ├── dm_pygame.py
│       ├── fcfs_disk.py
│       ├── look.py 
│       ├── scan.py
│       └── sstf.py     
│
│   ├── memory_management/                   # Memory Management Visualizers
│       ├── best_available_fit.py
│       ├── best_fit_mft.py
│       ├── best_fit_mvt_compaction.py
│       ├── best_fit_mvt_no_compaction.py
│       ├── best_fit_mvt.py
│       ├── best_fit.py
│       ├── first_fit_mft.py
│       ├── first_fit_mvt_compaction.py
│       ├── first_fit_mvt_no_compaction.py
│       ├── first_fit_mvt.py
│       ├── first_fit.py
│       ├── mm_main_menu.py 
│       ├── worst_fit_compaction.py
│       ├── worst_fit_no_compaction.py
│       └── worst_fit.py          
│   
│   └── virtual_memory/                      # Page Replacement Phase visualizers
│       ├── fifo_pr.py
│       ├── lfu_pr.py
│       ├── lru_pr.py
│       ├── mfu_pr.py
│       ├── mru_pr.py
│       ├── optimal_pr.py
│       └── vm_pygame.py
│
├── components/                              # Shared Graphical UI Assets
│   ├── background.png                       # System Terminal Backdrop Image
│   └── VT323-Regular.ttf                    # Monospace Display Typography Font
│
├── meet_the_devs.py                 # Static Credits/Developer Profile Panel Module
└── main.py                          # Primary Core Application Launch Entry Point
