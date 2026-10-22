# Operating Systems Project-Based Learning (PBL) Report
## Design and Implementation of an Interactive Deadlock Simulation System (Week 4)

---

### Project Information
- **Course:** Operating Systems Laboratory / Project-Based Learning (PBL)
- **Project Title:** Design and Implementation of an Interactive Deadlock Simulation System
- **Implementation Languages:** C (C99 / GNU POSIX Compliant) and Python (Tkinter Graphical User Interface)
- **Repository:** `https://github.com/aditinayak2007/zotify`

---

## 1. Executive Summary & Team Roles

The purpose of this project is to develop a complete, working, interactive Operating Systems simulation system that models and demonstrates:
1. **Deadlock Avoidance** using Dijkstra's Banker's Algorithm.
2. **Dynamic Resource Allocation and Request Handling** with boundary verification and rollback.
3. **Deadlock Detection** in systems with multiple instances of each resource type.
4. **Resource Allocation Graph (RAG)** visualization and Wait-For graph cycle detection.
5. **Deadlock Recovery** via victim process termination and resource preemption.

### Team Organization & Task Breakdown

| Team Member | Role | Assigned Technical Contribution |
|:---|:---|:---|
| **Aditi Nayak** *(Team Leader)* | **Integration Architect & Lead Delivery Engineer** | System integration across C and Python, common data modeling (`BankersState`, `DeadlockState`, `RAG`), C interactive CLI orchestrator (`main.c`), automated verification test suites (`test_runner.c` and `test_deadlock.py`), build automation (`Makefile`), and GitHub delivery. |
| **Anas Ahmed** | GUI & Graphical Visualization | Interactive Tkinter Graphical User Interface (`gui.py`), visual Resource Allocation Graph (RAG) canvas with circular process nodes, square resource nodes, directed allocation/request edges, live status banner, and diagnostic log. |
| **Nireeksha** | Banker's Algorithm & Deadlock Avoidance | Implementation of Banker's Algorithm (`bankers.c`), Need Matrix calculation ($\text{Need} = \text{Max} - \text{Alloc}$), safe/unsafe state identification, safe sequence generator, and safe resource request handling. |
| **Yaseem** | Deadlock Detection, RAG, and Recovery | Multi-instance Deadlock Detection algorithm (`deadlock.c`), Resource Allocation Graph representation (`rag.c`), Wait-For cycle detection, and Deadlock Recovery engine (`recovery.c`) supporting greedy and manual process termination. |

---

## 2. Theoretical Background & Mathematical Formulations

### 2.1 Coffman's Four Conditions for Deadlock
A deadlock occurs when a set of concurrent processes are permanently blocked because each process holds resources and waits for others to release resources. For deadlock to arise, four conditions must hold simultaneously:
1. **Mutual Exclusion:** At least one resource must be held in a non-shareable mode.
2. **Hold and Wait:** A process must currently hold at least one resource and be waiting to acquire additional resources held by other processes.
3. **No Preemption:** Resources cannot be forcibly preempted from a process; they can only be released voluntarily after the process completes its task.
4. **Circular Wait:** A closed chain of processes exists: $\langle P_0, P_1, \dots, P_n \rangle$, such that $P_0$ waits for a resource held by $P_1$, $P_1$ waits for $P_2$, $\dots$, and $P_n$ waits for $P_0$.

### 2.2 Mathematical Formulations

#### 1. Need Matrix Formulation
In Banker's Algorithm, each process declares its maximum resource claim in advance. The remaining resources each process may still request is represented by the Need Matrix:
$$\text{Need}[i][j] = \text{Max}[i][j] - \text{Allocation}[i][j] \quad \forall i \in [0, n-1], \, j \in [0, m-1]$$
- **Constraint:** $\text{Max}[i][j] \ge \text{Allocation}[i][j]$ and $\text{Allocation}[i][j] \ge 0$.

#### 2. Banker's Safety Algorithm
Let $\text{Work}$ be a vector of length $m$ initialized to $\text{Available}$, and $\text{Finish}$ be a boolean vector of length $n$ initialized to $\text{False}$.
1. Find an index $i$ such that:
   $$\text{Finish}[i] == \text{False} \quad \text{and} \quad \text{Need}[i] \le \text{Work}$$
2. If such an $i$ exists:
   $$\text{Work} = \text{Work} + \text{Allocation}[i]$$
   $$\text{Finish}[i] = \text{True}$$
   Repeat step 1.
3. If $\text{Finish}[i] == \text{True}$ for all $i \in [0, n-1]$, the system is in a **SAFE STATE**. The order in which processes finished constitutes a **Safe Sequence**.

#### 3. Resource-Request Algorithm
When process $P_i$ makes a request vector $\text{Request}_i$:
- **Rule 1 (Claim Limit):** If $\text{Request}_i[j] > \text{Need}_i[j]$ for any $j$, raise an error (process has exceeded its maximum declared claim).
- **Rule 2 (Availability Check):** If $\text{Request}_i[j] > \text{Available}[j]$ for any $j$, $P_i$ must wait (insufficient available resources).
- **Rule 3 (Safety Verification):** Pretend to allocate the requested resources:
  $$\text{Available} = \text{Available} - \text{Request}_i$$
  $$\text{Allocation}_i = \text{Allocation}_i + \text{Request}_i$$
  $$\text{Need}_i = \text{Need}_i - \text{Request}_i$$
  Execute the Safety Algorithm on the resulting state:
  - If **Safe**: Grant the request permanently.
  - If **Unsafe**: Roll back the allocation to the previous state; $P_i$ must wait.

#### 4. Multi-Instance Deadlock Detection Algorithm
Unlike Banker's Algorithm (which evaluates hypothetical future claims), Deadlock Detection evaluates the *current* state:
- Let $\text{Work} = \text{Available}$.
- For all $i$: if $\text{Allocation}[i] \ne \mathbf{0}$, then $\text{Finish}[i] = \text{False}$; else $\text{Finish}[i] = \text{True}$.
- Find $i$ such that $\text{Finish}[i] == \text{False}$ and $\text{Request}[i] \le \text{Work}$.
  If found: $\text{Work} = \text{Work} + \text{Allocation}[i]$; $\text{Finish}[i] = \text{True}$; repeat.
- If $\text{Finish}[i] == \text{False}$ for any $i$, **DEADLOCK EXISTS**, and process $P_i$ is deadlocked.

---

## 3. System Architecture & Component Integration

Under the technical leadership of **Aditi Nayak**, the simulator was integrated across two complementary presentation modes:
1. **Interactive Tkinter Desktop GUI (`gui.py`)**: Designed for visual demonstration during presentations, featuring a live Resource Allocation Graph canvas, editable matrix grids, color-coded state indicators, and step-by-step diagnostic traces.
2. **Native C Simulator (`main.c`)**: Designed for standard terminal operation and evaluation, compiling cleanly under MinGW GCC with automated build scripts (`Makefile`).

```
+-----------------------------------------------------------------------------------+
|               Interactive Deadlock Simulation System (Week 4)                      |
+-----------------------------------------+-----------------------------------------+
|        Desktop GUI (Anas / Aditi)       |         CLI Engine (Aditi Nayak)        |
|                gui.py                   |                 main.c                  |
+-----------------------------------------+-----------------------------------------+
                                          |
        +---------------------------------+---------------------------------+
        |                                 |                                 |
+-------v---------+             +---------v-------+                 +-------v-------+
|    bankers.c    |             |   deadlock.c    |                 |  recovery.c   |
| (Nireeksha)     |             |    (Yaseem)     |                 |   (Yaseem)    |
| - Need Matrix   |             | - Multi-Instance|                 | - Greedy Abort|
| - Safety Check  |             |   Detection     |                 | - Single Abort|
| - Safe Request  |             | - Deadlock Procs|                 | - Reclaim Res |
+-----------------+             +-----------------+                 +---------------+
        |                                 |                                 |
        +---------------------------------+---------------------------------+
                                          |
                                +---------v-------+
                                |      rag.c      |
                                |    (Yaseem)     |
                                | - Edge Mapping  |
                                | - Cycle Detect  |
                                +-----------------+
```

---

## 4. Key Features Implemented and Verified

1. **Process and Resource Management:** Dynamic configuration of process count ($N \le 10$) and resource types ($M \le 10$), input dimension validation, non-negative bounds checking, and automatic computation of the Need Matrix.
2. **Banker's Algorithm (Deadlock Avoidance):** Correct identification of safe and unsafe states, step-by-step logging of Work vector updates, and safe execution sequence generation (`P1 -> P3 -> P4 -> P0 -> P2`).
3. **Safe Resource Request Validation:** Validation against remaining need and availability, tentative allocation, safety check, and automatic state rollback upon detecting an unsafe condition.
4. **Multi-Instance Deadlock Detection:** Detection of active deadlocks, extraction of deadlocked processes, and differentiation between unsafe future states and active present deadlocks.
5. **Interactive Resource Allocation Graph (RAG):** Graphical canvas rendering process nodes as circles, resource nodes as rounded boxes with instance counts, allocation edges ($R \to P$), request edges ($P \to R$), and visual highlighting of deadlocked cycles in red.
6. **Deadlock Recovery:** Implementation of both Auto-Greedy Abort (terminating the process holding the largest allocation) and Manual Victim Abort, followed by automatic resource reclamation and post-recovery state verification.

---

## 5. Verification & Automated Test Results

The system was verified using two automated test harnesses:
- **C Test Harness (`test_runner.c`)**: 9 test suites containing 21 assertions covering all edge cases, memory limits, and boundary conditions.
- **Python Test Harness (`test_deadlock.py`)**: 6 unit test methods validating the GUI models, matrix calculations, and recovery algorithms.

### Summary of Test Execution Results

```text
========================================================
 DEADLOCK SIMULATION SYSTEM - AUTOMATED TEST RUNNER
 Author: Aditi Nayak (Team Leader & Integration)
========================================================

[TEST 1] Banker's Algorithm - Safe State & Safe Sequence Detection: PASSED
[TEST 2] Banker's Algorithm - Valid Safe Request: PASSED
[TEST 3] Banker's Algorithm - Unsafe Request Rejection & Rollback: PASSED
[TEST 4] Banker's Algorithm - Request Exceeding Declared Need: PASSED
[TEST 5] Banker's Algorithm - Request Exceeding Available Resources: PASSED
[TEST 6] Deadlock Detection - Active Circular Wait Deadlock: PASSED
[TEST 7] Differentiation: Unsafe State vs Actively Deadlocked State: PASSED
[TEST 8] Deadlock Recovery - Aborting Victim Process & State Verification: PASSED
[TEST 9] Resource Allocation Graph - Edge Construction & Wait-For Cycle: PASSED

========================================================
 ALL TEST SUITES COMPLETED: 21 ASSERTIONS PASSED (100%)
========================================================
```

---

## 6. How to Build and Run the Simulator

### Running the Graphical User Interface (Python Tkinter)
```powershell
cd "Week 4"
py gui.py
```

### Compiling and Running the C CLI Simulator (MinGW GCC)
```powershell
cd "Week 4"
gcc -Wall -Wextra -O2 -o deadlock_sim.exe main.c bankers.c deadlock.c rag.c recovery.c
.\deadlock_sim.exe
```

### Running the Automated Test Suites
```powershell
# C Test Runner
gcc -Wall -Wextra -O2 -o test_runner.exe test_runner.c bankers.c deadlock.c rag.c recovery.c
.\test_runner.exe

# Python Test Suite
py test_deadlock.py
```

---

## 7. Conclusion

The Week 4 Interactive Deadlock Simulation System project was successfully designed, integrated, tested, and documented. The simulator bridges theoretical OS deadlock concepts with interactive visual simulation, providing students and evaluators with a hands-on tool for exploring deadlock avoidance, detection, Resource Allocation Graphs, and recovery strategies. All deliverables have been committed and verified in the GitHub repository.
