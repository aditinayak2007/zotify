# Operating Systems PBL Simulators Repository

Welcome to the **Operating Systems Project-Based Learning (PBL)** repository developed by **Aditi Nayak** (Team Leader) and team members **Anas Ahmed**, **Nireeksha**, and **Yaseem**.

This repository contains three complete, verified OS simulation systems implemented in C and Python:
1. **Week 4: Interactive Deadlock Simulation System** (Banker's Algorithm, Multi-Instance Deadlock Detection, Resource Allocation Graph canvas, and Deadlock Recovery with Tkinter GUI & C CLI).
2. **Week 3: Process Scheduling Simulator** (Six CPU scheduling algorithms, ASCII Gantt charts, per-process metrics, and automated test harness).
3. **Week 2: Multi-Process System Simulator** (Three independent processes communicating via POSIX Pipes IPC).

---

## Team Members & Responsibilities

| Team Member | Project Role | Week 2 Technical Contribution | Week 3 Technical Contribution | Week 4 Technical Contribution |
|:---|:---|:---|:---|:---|
| **Aditi Nayak** *(Team Leader)* | **Lead Architect & Integration Engineer** | **POSIX Pipes IPC** coordinator, pipe lifecycle management (`pipe()`, `fork()`, `close()`, `waitpid()`), descriptor hygiene, end-to-end integration | **Unified Scheduling Architecture**, data structures (`Process`, `Gantt`, `Seg`), interactive menu orchestrator (`main.c`), automated test suite (`test_runner.c`) | **Deadlock System Architecture**, cross-platform data modeling, C CLI orchestrator (`main.c`), C test harness (`test_runner.c`), Python test suite (`test_deadlock.py`), GitHub delivery |
| **Anas Ahmed** | GUI & Computational Scheduling | **UI Process** (`ui.c`) with interactive terminal REPL and command validation | **Input Module** (`input.c`), **FCFS** (`fcfs.c`), and **Round Robin** (`rr.c`) with configurable time quantum | **Graphical User Interface** (`gui.py`), interactive RAG canvas with animated nodes and edges, system status badge, diagnostic trace log |
| **Nireeksha** | Banker's Algorithm & Core Execution | **Core Process** (`core.c`) implementing CPU engine, Memory subsystem, Stack, and Queue | **Non-preemptive SJF**, **Preemptive SRTF** (`sjf.c`), and **ASCII Gantt Chart** renderer (`gantt.c`) | **Banker's Algorithm** (`bankers.c`), Need Matrix calculation ($\text{Need} = \text{Max} - \text{Alloc}$), safe/unsafe state analysis, safe sequence generation |
| **Yaseem** | Deadlock Detection, RAG, & Recovery | **Logging Process** (`logger.c`) with file persistence daemon (`yaseem.log`) | **Non-preemptive Priority**, **Preemptive Priority** (`priority.c`), and statistical metrics computation | **Deadlock Detection** (`deadlock.c`), Resource Allocation Graph logic (`rag.c`), Wait-For cycle detection, and **Deadlock Recovery** (`recovery.c`) |

---

# Part 1: Week 4 — Interactive Deadlock Simulation System

The Week 4 project models resource allocation, deadlock avoidance, detection, and recovery in modern multi-resource Operating Systems.

### Key Features
1. **Banker's Algorithm (Deadlock Avoidance):**
   - Automatically computes Need Matrix: $\text{Need}[i][j] = \text{Max}[i][j] - \text{Allocation}[i][j]$.
   - Validates system safety and displays complete safe execution sequence (e.g. $P_1 \to P_3 \to P_4 \to P_0 \to P_2$).
   - Validates resource requests against remaining need and available resources; rolls back unsafe requests.
2. **Multi-Instance Deadlock Detection:**
   - Evaluates current allocations and outstanding requests using the Work/Finish algorithm.
   - Accurately identifies all deadlocked processes.
   - Distinguishes between unsafe states (future risk) and active deadlocks (present circular wait).
3. **Resource Allocation Graph (RAG) Visualization:**
   - Visual Tkinter Canvas displaying processes as circles and resources as rounded rectangles with available counters.
   - Renders directed solid allocation edges ($R_j \to P_i$) and dashed request edges ($P_i \to R_j$).
   - Dynamically highlights deadlocked nodes and cycles in bright red.
4. **Deadlock Recovery:**
   - **Auto-Greedy Abort:** Automatically identifies and terminates the deadlocked process holding the largest allocation to maximize resource reclamation.
   - **Manual Abort:** Allows the operator to designate a specific victim process.
   - Automatically reclaims resources and re-runs deadlock detection to verify recovery.

### How to Run Week 4

#### 1. Interactive Desktop GUI (Python Tkinter)
```powershell
cd "Week 4"
py gui.py
```

#### 2. Native C CLI Simulator (MinGW GCC)
```powershell
cd "Week 4"
gcc -Wall -Wextra -O2 -o deadlock_sim.exe main.c bankers.c deadlock.c rag.c recovery.c
.\deadlock_sim.exe
```

#### 3. Automated Test Suites
```powershell
# Run C Verification Harness (9 Test Suites, 21 Assertions)
cd "Week 4"
gcc -Wall -Wextra -O2 -o test_runner.exe test_runner.c bankers.c deadlock.c rag.c recovery.c
.\test_runner.exe

# Run Python Unit Test Suite
py test_deadlock.py
```

---

# Part 2: Week 3 — Process Scheduling Simulator

The Week 3 simulator models CPU scheduling dynamics across six classic algorithms:
1. **First-Come, First-Served (FCFS)**
2. **Shortest Job First (Non-preemptive SJF)**
3. **Shortest Remaining Time First (Preemptive SRTF)**
4. **Non-preemptive Priority Scheduling** ($1 = \text{Highest Priority}$)
5. **Preemptive Priority Scheduling** ($1 = \text{Highest Priority}$)
6. **Round Robin (RR)** with configurable time quantum $q$

### Building and Running Week 3
```powershell
cd "Week 3"
gcc -Wall -Wextra -O2 -o scheduler.exe main.c input.c gantt.c fcfs.c sjf.c priority.c rr.c
.\scheduler.exe

# Automated Test Suite
gcc -Wall -Wextra -O2 -o test_runner.exe test_runner.c gantt.c fcfs.c sjf.c priority.c rr.c
.\test_runner.exe
```

---

# Part 3: Week 2 — Multi-Process Simulator (Pipes IPC)

The Week 2 simulator models a modular computer architecture separated into three concurrent processes communicating via POSIX Pipes:
$$\text{User} \longrightarrow \text{UI Process} \overset{\text{Pipe}}{\rightleftharpoons} \text{Core Process (CPU/Memory/Stack/Queue)} \overset{\text{Pipe}}{\longrightarrow} \text{Logging Process} \longrightarrow \text{yaseem.log}$$

### Building and Running Week 2
```powershell
cd "Week 2"
gcc -static -Wall -Wextra -O2 main.c ui.c core.c logger.c -o simulator.exe
.\simulator.exe
```

---

## Repository Structure

```
zotify/
├── Makefile                       # Top-level build automation (all, week2, week3, week4, test, clean)
├── README.md                      # Comprehensive repository documentation
├── .gitignore                     # Build and binary exclusions
├── Bankers Algorithm              # Teammate Nireeksha's original Banker's Algorithm upload
│
├── Week 4/                        # Interactive Deadlock Simulation System
│   ├── gui.py                     # Interactive Tkinter Graphical User Interface (Anas Ahmed)
│   ├── bankers.h / bankers.c      # Banker's Algorithm & Need Matrix Engine (Nireeksha)
│   ├── deadlock.h / deadlock.c    # Multi-Instance Deadlock Detection Algorithm (Yaseem)
│   ├── rag.h / rag.c              # Resource Allocation Graph Engine (Yaseem)
│   ├── recovery.h / recovery.c    # Deadlock Recovery Engine (Yaseem)
│   ├── main.c                     # Interactive C CLI Runner (Aditi Nayak)
│   ├── test_runner.c              # Automated C Verification Harness (Aditi Nayak)
│   ├── test_deadlock.py           # Automated Python Unit Test Suite (Aditi Nayak)
│   ├── Makefile                   # Week 4 Build Automation
│   ├── TEST_CASES.md              # Detailed Test Cases & Execution Logs
│   └── REPORT.md                  # Comprehensive Academic Project Report
│
├── Week 3/                        # Process Scheduling Simulator
│   ├── process.h                  # Common Process and Gantt data structures
│   ├── input.c / fcfs.c / rr.c    # Anas's scheduling algorithms
│   ├── sjf.c / gantt.c            # Nireeksha's SJF and Gantt chart
│   ├── priority.c                 # Yaseem's priority algorithms
│   ├── main.c / test_runner.c     # Aditi's orchestrator and test suite
│   ├── TEST_CASES.md / REPORT.md  # Week 3 Documentation
│   └── Makefile                   # Week 3 build configuration
│
└── Week 2/                        # Multi-Process Simulator (Pipes IPC)
    ├── main.c                     # IPC Coordinator & Process Management (Aditi Nayak)
    ├── pipe_ipc.h                 # POSIX Pipes abstraction
    ├── ui.c / core.c / logger.c   # Subsystem implementations
    └── Makefile                   # Week 2 build configuration
```
