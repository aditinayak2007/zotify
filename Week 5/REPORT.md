# Operating Systems Project-Based Learning (PBL) Report
## Simulation and Comparative Analysis of Page Replacement Algorithms (Week 5)

---

### Project Information
- **Course:** Operating Systems Laboratory / Project-Based Learning (PBL)
- **Project Title:** Simulation and Comparative Analysis of Page Replacement Algorithms
- **Implementation Languages:** C (C99 / GNU POSIX Compliant) and Python (Tkinter Graphical User Interface)
- **Repository:** `https://github.com/aditinayak2007/zotify`

---

## 1. Executive Summary & Team Roles

Virtual memory systems allow modern operating systems to execute processes whose address spaces exceed physical memory capacity. When a process accesses a logical page not currently loaded into physical memory frames, the memory management unit (MMU) generates a **Page Fault** trap, requiring the operating system to load the requested page from secondary storage. If all allocated physical frames are full, the OS page replacement policy must select an existing resident page to evict.

The objective of this project is to model, simulate, and comparatively evaluate the three fundamental page replacement policies:
1. **First-In, First-Out (FIFO)**
2. **Least Recently Used (LRU)**
3. **Optimal Page Replacement (OPT / MIN)**

### Team Organization & Task Breakdown

| Team Member | Role | Assigned Technical Contribution |
|:---|:---|:---|
| **Aditi Nayak** *(Team Leader)* | **Integration Architect & Delivery Engineer** | System integration across C backend and Python GUI, standardized data structures (`SimulationResult`, `PageStep`), C interactive CLI orchestrator (`main.c`), automated C verification harness (`test_runner.c`), Python unit test suite (`test_page_replacement.py`), build automation (`Makefile`), and GitHub delivery. |
| **Anas Ahmed** | GUI & Graphical Interface | Presentation-ready Tkinter Desktop GUI (`gui.py`), input validation, step-by-step frame contents table, dynamic comparison matrix, performance metric summary cards, and best-performing algorithm banner. |
| **Nireeksha** | FIFO and LRU Algorithms | Implementation of First-In First-Out (`fifo.c`) with circular pointer eviction and Least Recently Used (`lru.c`) using timestamp-based reference tracking. |
| **Yaseem** | Optimal Algorithm & Comparison Engine | Implementation of Bélády's Optimal Algorithm (`optimal.c`) with lookahead future inspection, performance metrics calculator (`metrics.c`), and multi-algorithm comparative analyzer. |

---

## 2. Theoretical Background & Mathematical Foundations

### 2.1 Demand Paging & Page Fault Mechanism
In a demand-paged virtual memory architecture:
1. Memory is partitioned into fixed-size units called **Pages** (logical) and **Frames** (physical).
2. The page table maintains a **Valid/Invalid Bit** for each entry.
3. When an instruction references an invalid page, a **Page Fault Interrupt** occurs:
   - The OS traps to kernel mode, saving process state.
   - The OS checks if the reference is valid within the process's virtual address space.
   - A free frame is located in physical memory.
   - If no frame is free, a **Page Replacement Algorithm** is invoked to select a victim frame.
   - If the victim page was modified (dirty bit set), it is written back to disk.
   - The requested page is read from disk into the freed frame.
   - The page table and valid bit are updated.
   - The instruction that triggered the page fault is restarted.

### 2.2 Mathematical Formulations

Let:
- $N$ = Total number of logical page references in the sequence.
- $H$ = Number of page references that were already resident in memory (**Page Hits**).
- $F$ = Number of page references that required page loading (**Page Faults**).
- $M$ = Number of physical frames allocated to the process.

The fundamental system invariant is:
$$H + F = N$$

#### 1. Page Hit Ratio ($HR$)
The fraction of memory references satisfied from physical memory without accessing secondary storage:
$$HR = \left( \frac{H}{N} \right) \times 100\%$$

#### 2. Page Fault Ratio ($FR$)
The fraction of memory references that resulted in page faults:
$$FR = \left( \frac{F}{N} \right) \times 100\%$$
- Relationship: $HR + FR = 100\%$.

#### 3. Effective Access Time ($EAT$)
Let $m_t$ be physical memory access time (e.g. 100 ns) and $p_{fault}$ be page fault service time (e.g. 8 ms). The effective memory access time is:
$$EAT = (1 - P) \times m_t + P \times p_{fault}$$
where $P = \frac{F}{N}$ is the page fault probability. Minimizing $F$ directly maximizes system performance.

---

## 3. Implemented Page Replacement Algorithms

### 3.1 First-In, First-Out (FIFO)
- **Discipline:** Pure queue-based (First-In, First-Out).
- **Selection Criterion:** Evicts the page that has resided in physical memory for the longest time.
- **Implementation:** Maintained via a circular pointer index ($0 \le \text{ptr} < M$) pointing to the next replacement slot. When a fault occurs on full frames, $\text{frames}[\text{ptr}] = \text{page}$, and $\text{ptr} = (\text{ptr} + 1) \bmod M$.
- **Complexity:** $O(1)$ replacement time, $O(M)$ hit search.
- **Characteristics:** Simple with low overhead, but disregards page usage frequency or recency. Susceptible to **Bélády's Anomaly** (increasing frame capacity can paradoxically increase page faults).

### 3.2 Least Recently Used (LRU)
- **Discipline:** Temporal locality-based heuristic.
- **Selection Criterion:** Evicts the page that has not been accessed for the longest period of time in the past.
- **Implementation:** Each frame maintains a timestamp or reference counter updated on every access. When replacement occurs, the frame with the minimum timestamp is evicted.
- **Complexity:** $O(M)$ replacement search.
- **Characteristics:** Approximates optimal replacement by exploiting the principle of locality. Belonging to the class of **Stack Algorithms**, LRU never exhibits Bélády's Anomaly.

### 3.3 Optimal Page Replacement (OPT / MIN)
- **Discipline:** Theoretical benchmark (Bélády's Algorithm).
- **Selection Criterion:** Evicts the page that will not be referenced for the longest period of time in the future.
- **Implementation:** Scans forward in the reference string from $i + 1$ to $N - 1$. The page whose next access is furthest in the future (or never accessed again, represented by distance $\infty$) is chosen as victim. If multiple pages have infinite distance, tie-breaking chooses the first one encountered.
- **Characteristics:** Mathematically guarantees the lowest possible page fault rate for a given reference string and frame capacity. Because it requires advance knowledge of future references, it serves as an unattainable standard against which practical algorithms are benchmarked.

---

## 4. Software Architecture & Modular Design

Under the leadership of **Aditi Nayak**, the software was designed with dual presentation layers (Desktop GUI and Native C CLI):

```
+-----------------------------------------------------------------------------------+
|               Page Replacement Algorithms Simulator (Week 5)                      |
+-----------------------------------------+-----------------------------------------+
|        Desktop GUI (Anas / Aditi)       |         CLI Engine (Aditi Nayak)        |
|                gui.py                   |                 main.c                  |
+-----------------------------------------+-----------------------------------------+
                                          |
        +---------------------------------+---------------------------------+
        |                                 |                                 |
+-------v---------+             +---------v-------+                 +-------v-------+
|     fifo.c      |             |      lru.c      |                 |   optimal.c   |
|  (Nireeksha)    |             |  (Nireeksha)    |                 |   (Yaseem)    |
| - Circular Ptr  |             | - Timestamps    |                 | - Lookahead   |
| - Queue Policy  |             | - Recency Evict |                 | - Dist. Evict |
+-----------------+             +-----------------+                 +---------------+
        |                                 |                                 |
        +---------------------------------+---------------------------------+
                                          |
                                +---------v-------+
                                |    metrics.c    |
                                |    (Yaseem)     |
                                | - Hit/Fault Ratio|
                                | - Comparison    |
                                | - Best Selection|
                                +-----------------+
```

---

## 5. Experimental Results & Comparative Analysis

### Benchmark Dataset
- **Page-Reference String:** `7 0 1 2 0 3 0 4 2 3` ($N = 10$)
- **Frame Capacity:** $M = 3$

### Performance Results Table

| Algorithm | Total References | Page Hits | Page Faults | Hit Ratio (%) | Fault Ratio (%) | Outcome |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **FIFO** | 10 | 1 | 9 | 10.00% | 90.00% | Lowest hit rate; evicts early pages repeatedly |
| **LRU** | 10 | 2 | 8 | 20.00% | 80.00% | 100% improvement in hits over FIFO |
| **Optimal** | 10 | **4** | **6** | **40.00%** | **60.00%** | **★ Optimal Benchmark (Lowest Faults: 6)** |

### Step-by-Step State Transitions for Optimal

```text
Step 1  (Page 7): [ 7  -  - ]  FAULT
Step 2  (Page 0): [ 7  0  - ]  FAULT
Step 3  (Page 1): [ 7  0  1 ]  FAULT
Step 4  (Page 2): [ 2  0  1 ]  FAULT  (Page 7 never used again, evicted)
Step 5  (Page 0): [ 2  0  1 ]  HIT
Step 6  (Page 3): [ 2  0  3 ]  FAULT  (Page 1 never used again, evicted)
Step 7  (Page 0): [ 2  0  3 ]  HIT
Step 8  (Page 4): [ 2  4  3 ]  FAULT  (Page 0 never used again, evicted)
Step 9  (Page 2): [ 2  4  3 ]  HIT
Step 10 (Page 3): [ 2  4  3 ]  HIT
```

---

## 6. Verification and Automated Testing

The implementation was validated using two independent test harnesses:
- **C Test Runner (`test_runner.c`)**: 6 comprehensive test suites containing 34 assertions verifying course benchmarks, cyclic references, repeated references, single page boundary conditions, and invariant equations.
- **Python Unit Test Suite (`test_page_replacement.py`)**: 7 automated unit test methods validating GUI model logic, input parser error handling, and comparison matrix generation.

**Combined Test Results:** **41 of 41 assertions passed (100%)**.

---

## 7. How to Build and Run the Simulator

### Running the Desktop GUI (Python Tkinter)
```powershell
cd "Week 5"
py gui.py
```

### Compiling and Running the Native C Simulator (MinGW GCC)
```powershell
cd "Week 5"
gcc -Wall -Wextra -O2 -o page_sim.exe main.c fifo.c lru.c optimal.c metrics.c
.\page_sim.exe
```

### Running Automated Test Runners
```powershell
# C Test Runner
gcc -Wall -Wextra -O2 -o test_runner.exe test_runner.c fifo.c lru.c optimal.c metrics.c
.\test_runner.exe

# Python Unit Test Suite
py test_page_replacement.py
```

---

## 8. Conclusion

The Week 5 Page Replacement Simulator was successfully designed, developed, integrated, and verified. By combining clean modular backend logic in C with an interactive, presentation-ready Tkinter desktop GUI, the simulator provides an intuitive demonstration of virtual memory page management. All deliverables are complete, verified, and committed to the repository.
