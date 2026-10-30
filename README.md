# Operating Systems PBL Simulators Repository

Welcome to the **Operating Systems Project-Based Learning (PBL)** repository developed by **Aditi Nayak** (Team Leader) and team members **Anas Ahmed**, **Nireeksha**, and **Yaseem**.

This repository contains four complete, verified OS simulation systems implemented in C and Python:
1. **Week 5: Simulation and Comparative Analysis of Page Replacement Algorithms** (FIFO, LRU, Optimal algorithms, step-by-step frame contents, performance metrics, and multi-algorithm comparative analysis with Tkinter GUI & C CLI).
2. **Week 4: Interactive Deadlock Simulation System** (Banker's Algorithm, Multi-Instance Deadlock Detection, Resource Allocation Graph canvas, and Deadlock Recovery).
3. **Week 3: Process Scheduling Simulator** (Six CPU scheduling algorithms, ASCII Gantt charts, per-process metrics, and automated test harness).
4. **Week 2: Multi-Process System Simulator** (Three independent processes communicating via POSIX Pipes IPC).

---

## Team Members & Responsibilities

| Team Member | Project Role | Week 2 Contribution | Week 3 Contribution | Week 4 Contribution | Week 5 Contribution |
|:---|:---|:---|:---|:---|:---|
| **Aditi Nayak** *(Team Leader)* | **Lead Architect & Integration Engineer** | **POSIX Pipes IPC** coordinator, descriptor hygiene, process lifecycle | **Unified Scheduling Architecture**, data structures, test suite (`test_runner.c`) | **Deadlock System Architecture**, C CLI runner, C & Python test harnesses | **Page Replacement Architecture**, C backend integration, automated verification harnesses (`test_runner.c` and `test_page_replacement.py`), documentation & GitHub delivery |
| **Anas Ahmed** | GUI & Visualization | **UI Process** (`ui.c`) terminal REPL | **Input Module**, **FCFS** & **Round Robin** algorithms | **Tkinter GUI** (`gui.py`), interactive RAG canvas | **Tkinter GUI** (`gui.py`), frame-by-frame result table, comparison matrix, summary cards |
| **Nireeksha** | Core Algorithms & Execution | **Core Process** (`core.c`) with CPU, memory, stack, queue | **Non-preemptive SJF**, **Preemptive SRTF**, Gantt chart | **Banker's Algorithm** (`bankers.c`), Need Matrix calculation | **FIFO Algorithm** (`fifo.c`) and **LRU Algorithm** (`lru.c`) |
| **Yaseem** | Algorithms & Analytics | **Logging Process** (`logger.c`), file logging daemon | **Priority Scheduling**, statistical metrics | **Deadlock Detection** (`deadlock.c`), RAG logic (`rag.c`), **Recovery** (`recovery.c`) | **Optimal Algorithm** (`optimal.c`), performance metrics engine (`metrics.c`), multi-algorithm comparative analyzer |

---

# Part 1: Week 5 — Page Replacement Algorithms Simulator

The Week 5 project simulates and comparatively analyzes page replacement policies in demand-paged virtual memory systems.

### Supported Algorithms
1. **FIFO (First-In, First-Out):** Evicts the oldest loaded page using a circular replacement pointer.
2. **LRU (Least Recently Used):** Evicts the page unreferenced for the longest period in the past using access timestamps.
3. **Optimal (OPT / MIN):** Evicts the page that will not be accessed for the longest period in the future (Bélády's optimal benchmark).

### Performance Metrics & Formulas
- **Total Page References ($N$):** Number of page requests in the sequence.
- **Total Page Hits ($H$):** References where the page was already resident in memory.
- **Total Page Faults ($F$):** References where the page was missing from memory frames.
- **Hit Ratio ($HR$):**
  $$\text{Hit Ratio} = \left( \frac{\text{Page Hits}}{\text{Total Page References}} \right) \times 100\%$$
- **Fault Ratio ($FR$):**
  $$\text{Fault Ratio} = \left( \frac{\text{Page Faults}}{\text{Total Page References}} \right) \times 100\%$$
- **Fundamental Invariant:** $\text{Page Hits} + \text{Page Faults} = \text{Total References}$.

### Course Specification Sample Benchmark
- **Page-Reference String:** `7 0 1 2 0 3 0 4 2 3`
- **Number of Frames:** 3

| Algorithm | Total References | Page Hits | Page Faults | Hit Ratio (%) | Fault Ratio (%) | Outcome |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **FIFO** | 10 | 1 | 9 | 10.00% | 90.00% | Highest fault count |
| **LRU** | 10 | 2 | 8 | 20.00% | 80.00% | 100% improvement over FIFO |
| **Optimal** | 10 | **4** | **6** | **40.00%** | **60.00%** | **★ Best Performance (Lowest Faults: 6)** |

### How to Run Week 5

#### 1. Interactive Desktop GUI (Python Tkinter)
```powershell
cd "Week 5"
py gui.py
```

#### 2. Native C CLI Simulator (MinGW GCC)
```powershell
cd "Week 5"
gcc -Wall -Wextra -O2 -o page_sim.exe main.c fifo.c lru.c optimal.c metrics.c
.\page_sim.exe
```

#### 3. Automated Test Suites
```powershell
# C Test Runner (34 assertions)
cd "Week 5"
gcc -Wall -Wextra -O2 -o test_runner.exe test_runner.c fifo.c lru.c optimal.c metrics.c
.\test_runner.exe

# Python Unit Test Suite (7 unit tests)
py test_page_replacement.py
```

---

# Part 2: Week 4 — Interactive Deadlock Simulation System

The Week 4 project models resource allocation, deadlock avoidance, detection, and recovery.

### Features
1. **Banker's Algorithm (Avoidance):** Need Matrix calculation ($\text{Need} = \text{Max} - \text{Alloc}$), safety sequence analysis, and request evaluation with rollback.
2. **Deadlock Detection:** Multi-instance resource deadlock detection algorithm.
3. **Resource Allocation Graph (RAG):** Interactive visual canvas with cycle detection.
4. **Deadlock Recovery:** Auto-Greedy and manual process termination with resource reclamation.

### Running Week 4
```powershell
cd "Week 4"
py gui.py          # Desktop GUI
.\deadlock_sim.exe # C CLI
```

---

# Part 3: Week 3 — Process Scheduling Simulator

Models 6 CPU scheduling algorithms: FCFS, SJF (Non-preemptive & Preemptive/SRTF), Priority (Non-preemptive & Preemptive), and Round Robin ($q$).

### Running Week 3
```powershell
cd "Week 3"
gcc -Wall -Wextra -O2 -o scheduler.exe main.c input.c gantt.c fcfs.c sjf.c priority.c rr.c
.\scheduler.exe
```

---

# Part 4: Week 2 — Multi-Process Simulator (Pipes IPC)

Models UI, Core, and Logger processes communicating via POSIX Pipes IPC.

### Running Week 2
```powershell
cd "Week 2"
gcc -static -Wall -Wextra -O2 main.c ui.c core.c logger.c -o simulator.exe
.\simulator.exe
```

---

## Repository Structure

```
zotify/
├── Makefile                       # Top-level build automation (all, week2, week3, week4, week5)
├── README.md                      # Comprehensive repository documentation
├── .gitignore                     # Build and binary exclusions
│
├── Week 5/                        # Page Replacement Simulator (Week 5)
│   ├── gui.py                     # Interactive Tkinter GUI (Anas Ahmed / Aditi Nayak)
│   ├── page_replacement.h        # Unified data structures and prototypes
│   ├── fifo.c                     # First-In, First-Out Algorithm (Nireeksha)
│   ├── lru.c                      # Least Recently Used Algorithm (Nireeksha)
│   ├── optimal.c                  # Optimal Page Replacement Algorithm (Yaseem)
│   ├── metrics.c                  # Performance Metrics & Comparison (Yaseem)
│   ├── main.c                     # Interactive C CLI Runner (Aditi Nayak)
│   ├── test_runner.c              # Automated C Verification Harness (Aditi Nayak)
│   ├── test_page_replacement.py   # Python Unit Test Suite (Aditi Nayak)
│   ├── Makefile                   # Week 5 Build Configuration
│   ├── TEST_CASES.md              # Detailed Test Cases & Execution Logs
│   └── REPORT.md                  # Comprehensive Academic Project Report
│
├── Week 4/                        # Deadlock Simulation System (Week 4)
├── Week 3/                        # Process Scheduling Simulator (Week 3)
└── Week 2/                        # Multi-Process Simulator (Week 2)
```
