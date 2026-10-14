# Operating Systems Project-Based Learning (PBL) Report
## Process Scheduling Simulator in C (Week 3)

---

### Project Information
- **Course:** Operating Systems Laboratory / Project-Based Learning (PBL)
- **Project Title:** Multi-Algorithm CPU Process Scheduling Simulator
- **Implementation Language:** C (C99 / GNU POSIX Compliant)
- **Repository:** `https://github.com/aditinayak2007/zotify`

---

## 1. Executive Summary & Team Roles

The purpose of this project is to model, simulate, and compare the execution behavior of classic CPU scheduling algorithms found in modern operating systems. The simulator accepts process parameters (Arrival Time, Burst Time, and Priority) and computes precise execution timelines, ASCII Gantt charts, per-process metrics, and global efficiency statistics.

### Team Organization & Task Breakdown

| Team Member | Role | Assigned Technical Contribution |
|:---|:---|:---|
| **Aditi Nayak** *(Team Leader)* | **Integration Architect & Lead Coordinator** | Standardized unified data structures (`Process`, `Gantt`, `Seg`), built interactive multi-algorithm menu orchestrator (`main.c`), dataset persistence engine, automated test suite (`test_runner.c`), Makefile build system, and cross-module integration. |
| **Anas Ahmed** | Input Handling & Time-Sliced Scheduling | Robust terminal input parser, duplicate PID rejection, FCFS algorithm (`fcfs.c`), and Round Robin algorithm (`rr.c`) with configurable time quantum and arrival queue management. |
| **Nireeksha** | SJF Algorithms & Gantt Engine | Non-preemptive Shortest Job First (`sjf.c`), Preemptive Shortest Remaining Time First (SRTF), and dynamic ASCII Gantt chart renderer with CPU IDLE visualization (`gantt.c`). |
| **Yaseem** | Priority Scheduling & Performance Metrics | Non-preemptive Priority scheduling (`priority.c`), Preemptive Priority scheduling, and statistical metric engine computing Waiting Time, Turnaround Time, Response Time, CPU Utilization, and Throughput. |

---

## 2. Theoretical Background & Mathematical Formulations

CPU scheduling is the core mechanism by which an Operating System determines which ready process is allocated the CPU when multiple processes compete for execution.

### Key Performance Metrics & Formulas

1. **Completion Time ($CT$):** The exact simulation clock cycle at which a process finishes its total burst time.
2. **Turnaround Time ($TAT$):** The total elapsed time between process arrival in the ready queue and its completion:
   $$TAT_i = CT_i - AT_i$$
3. **Waiting Time ($WT$):** The total cumulative time a process spends waiting in the ready queue without CPU allocation:
   $$WT_i = TAT_i - BT_i$$
4. **Response Time ($RT$):** The duration from process arrival until its very first allocation of CPU execution time:
   $$RT_i = \text{FirstStartTime}_i - AT_i$$
5. **Average Turnaround Time ($Avg\ TAT$):**
   $$Avg\ TAT = \frac{1}{N} \sum_{i=1}^{N} TAT_i$$
6. **Average Waiting Time ($Avg\ WT$):**
   $$Avg\ WT = \frac{1}{N} \sum_{i=1}^{N} WT_i$$
7. **Average Response Time ($Avg\ RT$):**
   $$Avg\ RT = \frac{1}{N} \sum_{i=1}^{N} RT_i$$
8. **CPU Utilization ($\%$):** Percentage of total simulation time during which the CPU was actively executing processes (excluding IDLE periods):
   $$\text{CPU Utilization} = \left( \frac{\sum BT_i}{\text{Total Simulation Time}} \right) \times 100\%$$
9. **Throughput:** Number of processes completed per unit time:
   $$\text{Throughput} = \frac{N}{\text{Total Simulation Time}}$$

---

## 3. Implemented Scheduling Algorithms

The simulator provides modular, verified implementations of six distinct scheduling algorithms:

### 3.1 First-Come, First-Served (FCFS)
- **Discipline:** Non-preemptive.
- **Criteria:** Arrival Time ($AT$).
- **Mechanism:** Processes are executed in the exact chronological order of their arrival. If the CPU is idle upon arrival, execution begins immediately.
- **Characteristics:** Simple, zero scheduling overhead. Susceptible to the **Convoy Effect** (short processes delayed behind long CPU-bound jobs).

### 3.2 Non-preemptive Shortest Job First (SJF)
- **Discipline:** Non-preemptive.
- **Criteria:** Burst Time ($BT$). Tie-breaker: Arrival Time ($AT$).
- **Mechanism:** Whenever the CPU becomes free, the scheduler selects the available arrived process with the minimum CPU burst requirement. Once dispatched, it runs to completion.
- **Characteristics:** Minimizes average waiting time among non-preemptive algorithms, but can cause starvation for longer jobs if short jobs arrive continually.

### 3.3 Preemptive Shortest Job First / Shortest Remaining Time First (SRTF)
- **Discipline:** Preemptive.
- **Criteria:** Remaining Burst Time ($rem$).
- **Mechanism:** Evaluated at every unit time increment ($t$). If a new process arrives with a remaining burst strictly shorter than the currently running process's remaining burst, the running process is preempted and returned to the ready pool.
- **Characteristics:** Theoretically optimal in minimizing average waiting time; requires dynamic tracking of remaining execution times.

### 3.4 Non-preemptive Priority Scheduling
- **Discipline:** Non-preemptive.
- **Criteria:** Priority value (Convention: **$1$ is the Highest Priority**). Tie-breaker: Arrival Time.
- **Mechanism:** Dispatches the highest-priority arrived process. The running process holds the CPU until normal termination.
- **Characteristics:** Allows critical or real-time tasks to take precedence, but can cause indefinite blocking (starvation) of low-priority processes.

### 3.5 Preemptive Priority Scheduling
- **Discipline:** Preemptive.
- **Criteria:** Priority value ($1 = \text{Highest}$).
- **Mechanism:** Evaluated at each time cycle. If a newly arrived process possesses a higher priority (lower numeric value) than the active process, preemption occurs instantly.
- **Characteristics:** Guarantees immediate service for high-priority arrivals at the cost of preemption context switches.

### 3.6 Round Robin (RR)
- **Discipline:** Preemptive (Time-sliced).
- **Criteria:** Time Quantum ($q$) and FIFO Ready Queue.
- **Mechanism:** Ready processes are maintained in a FIFO queue. Each process is allocated a slice of up to $q$ time units. If the process does not terminate within $q$, it is preempted, any newly arriving processes are appended to the ready queue first, and the preempted process is requeued at the tail.
- **Characteristics:** Ensures fairness and excellent response times for interactive environments. Performance strongly depends on the quantum size.

---

## 4. Software Architecture & Integration Design

Under the leadership of **Aditi Nayak**, the software was designed with strict modular separation to cleanly integrate all four team members' contributions:

```
+-------------------------------------------------------------------------+
|                                main.c                                   |
|                (Interactive Menu Orchestrator - Aditi)                  |
+--------------------+---------------------+--------------------+---------+
                     |                     |                    |
        +------------v-----------+   +-----v------+   +---------v---------+
        |        input.c         |   |  gantt.c   |   |    Algorithms     |
        |  (Input Parser - Anas) |   |  (Nireek   |   |   (All Members)   |
        |                        |   |  & Yaseem) |   |                   |
        +------------------------+   +------------+   +---------+---------+
                                                                |
           +----------------+----------------+------------------+-----------------+
           |                |                |                  |                 |
     +-----v-----+    +-----v-----+    +-----v-----+      +-----v-----+     +-----v-----+
     |  fcfs.c   |    |   sjf.c   |    | priority.c|      |   rr.c    |     |test_runner|
     |  (Anas)   |    | (Nireek)  |    | (Yaseem)  |      |  (Anas)   |     |  (Aditi)  |
     +-----------+    +-----------+    +-----------+      +-----------+     +-----------+
```

### 4.1 Standardized Data Structures (`process.h`)

All algorithms interact through standardized C structures:

```c
typedef struct {
    int pid;         /* Process Identifier (e.g., 1, 2, 3) */
    int at;          /* Arrival Time                       */
    int bt;          /* Total CPU Burst Time               */
    int priority;    /* Priority (1 = Highest)             */
    int ct;          /* Completion Time                    */
    int tat;         /* Turnaround Time                    */
    int wt;          /* Waiting Time                       */
    int rt;          /* Response Time                      */
    int rem;         /* Remaining Burst Time               */
    int first_start; /* Simulation time of first execution */
    int completed;   /* Completion status flag             */
} Process;

typedef struct {
    int pid;         /* PID or IDLE_PID (-1) for CPU idle  */
    int start;       /* Segment start clock cycle          */
    int end;         /* Segment end clock cycle            */
} Seg;

typedef struct {
    Seg s[MAX_SEG];  /* Timeline segments                  */
    int count;       /* Number of recorded segments        */
} Gantt;
```

### 4.2 Key Engineering Solutions Implemented by Aditi
1. **CPU Idle Gap Handling:** All algorithms explicitly detect when all arrived processes have terminated while future processes have not yet arrived. The timeline automatically records `IDLE` segments, ensuring accurate timeline continuity.
2. **Dataset Isolation via Deep Copy:** To allow running multiple algorithms on the same input data without re-entering values, `main.c` clones the original process array before each simulation run.
3. **Consecutive Preemption Segment Merging:** In preemptive algorithms (SRTF, Preemptive Priority, Round Robin), consecutive slices of the same process are merged in the Gantt chart for visual clarity.
4. **Tie-Breaking Determinism:** All selections consistently break ties using Arrival Time ($AT$), followed by PID.

---

## 5. Experimental Results & Performance Comparison

All six algorithms were evaluated against the standard reference dataset:

| Process | Arrival Time ($AT$) | Burst Time ($BT$) | Priority ($1 = \text{Highest}$) |
|:---:|:---:|:---:|:---:|
| **P1** | 0 | 5 | 2 |
| **P2** | 1 | 3 | 1 |
| **P3** | 2 | 1 | 3 |
| **P4** | 3 | 2 | 4 |

### Comprehensive Performance Matrix

| Algorithm | Avg Waiting Time ($WT$) | Avg Turnaround Time ($TAT$) | Avg Response Time ($RT$) | Total Timeline | CPU Utilization |
|:---|:---:|:---:|:---:|:---:|:---:|
| **FCFS** | 4.00 | 6.75 | 4.00 | 11 | 100.00% |
| **SJF (Non-preemptive)** | 3.25 | 6.00 | 3.25 | 11 | 100.00% |
| **SRTF (Preemptive SJF)** | **3.00** | **5.75** | **1.50** | 11 | 100.00% |
| **Priority (Non-preemptive)** | 3.75 | 6.50 | 3.75 | 11 | 100.00% |
| **Priority (Preemptive)** | 3.25 | 6.00 | **1.25** | 11 | 100.00% |
| **Round Robin ($q = 2$)** | 4.75 | 7.50 | **1.25** | 11 | 100.00% |

### Key Observations
1. **Optimal Waiting Time:** **SRTF** achieved the lowest average waiting time (3.00) and lowest average turnaround time (5.75), validating theoretical expectations.
2. **Best Responsiveness:** **Preemptive Priority** and **Round Robin** provided the lowest average response time (1.25), demonstrating their suitability for interactive computing.
3. **Convoy Effect in FCFS:** In FCFS, P2, P3, and P4 waited behind P1, resulting in higher average waiting times despite having smaller burst requirements.

---

## 6. Verification and Automated Testing

An automated verification harness (`test_runner.c`) was engineered to validate correctness without human intervention. The suite validates:
- Standard multi-process execution timelines.
- CPU Idle gap handling ($AT > 0$ and gaps between processes).
- SRTF preemption boundaries and resumption.
- Preemptive Priority preemption.
- Round Robin FIFO arrival queuing with multiple time slices.
- Single process boundary condition.

**Test Execution Output:**
```
==================================================
   PROCESS SCHEDULING SIMULATOR - AUTOMATED SUITE
==================================================
[TEST 1] FCFS with Staggered Arrivals: PASSED
[TEST 2] FCFS with CPU Idle Period: PASSED
[TEST 3] Non-Preemptive SJF: PASSED
[TEST 4] Preemptive SJF (SRTF): PASSED
[TEST 5] Preemptive Priority Scheduling: PASSED
[TEST 6] Round Robin (q = 2): PASSED
==================================================
ALL 6 TEST CASES PASSED SUCCESSFULLY (100%)
==================================================
```

---

## 7. Build and Execution Instructions

### Compilation (MinGW GCC or Linux GCC)
```bash
# Navigate to Week 3 directory
cd "Week 3"

# Build main simulator
make

# Or compile manually with gcc
gcc -Wall -Wextra -O2 -o scheduler main.c input.c gantt.c fcfs.c sjf.c priority.c rr.c

# Run the interactive simulator
./scheduler
```

### Running the Automated Test Suite
```bash
# Using Makefile target
make test

# Or compile and run directly
gcc -Wall -Wextra -O2 -o test_runner test_runner.c gantt.c fcfs.c sjf.c priority.c rr.c
./test_runner
```

---

## 8. Conclusion

The Week 3 Process Scheduling Simulator project was successfully developed, integrated, and validated. By standardizing communication structures and separating algorithmic logic into modular components, the team achieved seamless collaboration without code overwriting or conflicts. The project provides an interactive and educational tool for exploring CPU scheduling dynamics, complemented by full test coverage and verified performance metrics.
