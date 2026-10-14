# Process Scheduling Simulator — Test Cases & Verification Report

**Project:** Week 3 Process Scheduling Simulator in C  
**Lead & Integration:** Aditi Nayak (Team Leader)  
**Modules:** Anas Ahmed (FCFS, Round Robin, Input), Nireeksha (SJF, Gantt Chart), Yaseem (Priority, Metrics)  

---

## Overview

This document records the exact test scenarios and verified execution outputs for all six CPU process scheduling algorithms:
1. **First-Come, First-Served (FCFS)**
2. **Shortest Job First (Non-preemptive SJF)**
3. **Shortest Remaining Time First (Preemptive SJF / SRTF)**
4. **Non-preemptive Priority Scheduling**
5. **Preemptive Priority Scheduling**
6. **Round Robin (RR)**

---

## Test Case 1: Standard Mixed Workload (Equal & Staggered Arrivals)

### Process Dataset

| Process | Arrival Time (AT) | Burst Time (BT) | Priority (1 = Highest) |
|:---:|:---:|:---:|:---:|
| **P1** | 0 | 5 | 2 |
| **P2** | 1 | 3 | 1 |
| **P3** | 2 | 1 | 3 |
| **P4** | 3 | 2 | 4 |

---

### 1.1 First-Come, First-Served (FCFS)

- **Execution Order:** `P1 → P2 → P3 → P4`
- **Gantt Chart:**
```text
+----------+------+----+----+
|    P1    |  P2  | P3 | P4 |
+----------+------+----+----+
0          5      8    9    11
```
- **Process Metrics:**

| PID | AT | BT | Priority | CT | TAT | WT | RT |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **P1** | 0 | 5 | 2 | 5 | 5 | 0 | 0 |
| **P2** | 1 | 3 | 1 | 8 | 7 | 4 | 4 |
| **P3** | 2 | 1 | 3 | 9 | 7 | 6 | 6 |
| **P4** | 3 | 2 | 4 | 11 | 8 | 6 | 6 |

- **Summary Statistics:**
  - Average Waiting Time (WT): **4.00**
  - Average Turnaround Time (TAT): **6.75**
  - Average Response Time (RT): **4.00**
  - CPU Utilization: **100.00%**
  - Total Time: **11**

---

### 1.2 Non-preemptive Shortest Job First (SJF)

- **Execution Order:** At $t=0$, only P1 is available and runs to completion ($t=5$). At $t=5$, P2, P3, and P4 have all arrived. Among them, P3 has the shortest burst ($BT=1$), then P4 ($BT=2$), then P2 ($BT=3$).  
  Order: `P1 → P3 → P4 → P2`
- **Gantt Chart:**
```text
+----------+----+----+------+
|    P1    | P3 | P4 |  P2  |
+----------+----+----+------+
0          5    6    8      11
```
- **Process Metrics:**

| PID | AT | BT | Priority | CT | TAT | WT | RT |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **P1** | 0 | 5 | 2 | 5 | 5 | 0 | 0 |
| **P2** | 1 | 3 | 1 | 11 | 10 | 7 | 7 |
| **P3** | 2 | 1 | 3 | 6 | 4 | 3 | 3 |
| **P4** | 3 | 2 | 4 | 8 | 5 | 3 | 3 |

- **Summary Statistics:**
  - Average Waiting Time (WT): **3.25**
  - Average Turnaround Time (TAT): **6.00**
  - Average Response Time (RT): **3.25**
  - CPU Utilization: **100.00%**

---

### 1.3 Preemptive Shortest Job First (SRTF)

- **Execution Order:**  
  - $t=0$: P1 runs ($BT=5$).
  - $t=1$: P2 arrives ($BT=3 < \text{P1 rem } 4$). P1 is **preempted**.
  - $t=2$: P3 arrives ($BT=1 < \text{P2 rem } 2$). P2 is **preempted**.
  - $t=3$: P3 completes. P4 arrives ($BT=2$). Ready: P2 (rem 2), P4 (rem 2), P1 (rem 4). P2 runs (earlier arrival).
  - $t=5$: P2 completes. P4 runs ($BT=2$).
  - $t=7$: P4 completes. P1 finishes its remaining 4 units.  
  Order: `P1 → P2 → P3 → P2 → P4 → P1`
- **Gantt Chart:**
```text
+----+----+----+----+----+--------+
| P1 | P2 | P3 | P2 | P4 |   P1   |
+----+----+----+----+----+--------+
0    1    2    3    5    7        11
```
- **Process Metrics:**

| PID | AT | BT | Priority | CT | TAT | WT | RT |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **P1** | 0 | 5 | 2 | 11 | 11 | 6 | 0 |
| **P2** | 1 | 3 | 1 | 5 | 4 | 1 | 0 |
| **P3** | 2 | 1 | 3 | 3 | 1 | 0 | 0 |
| **P4** | 3 | 2 | 4 | 7 | 4 | 2 | 2 |

- **Summary Statistics:**
  - Average Waiting Time (WT): **2.25**
  - Average Turnaround Time (TAT): **5.00**
  - Average Response Time (RT): **0.50**
  - CPU Utilization: **100.00%**

---

### 1.4 Non-preemptive Priority Scheduling (1 = Highest)

- **Execution Order:** At $t=0$, P1 runs to completion ($t=5$). At $t=5$, P2 (Pri 1), P3 (Pri 3), and P4 (Pri 4) are ready. P2 has highest priority, then P3, then P4.  
  Order: `P1 → P2 → P3 → P4`
- **Gantt Chart:**
```text
+----------+------+----+----+
|    P1    |  P2  | P3 | P4 |
+----------+------+----+----+
0          5      8    9    11
```
- **Summary Statistics:**
  - Average Waiting Time (WT): **4.00**
  - Average Turnaround Time (TAT): **6.75**
  - Average Response Time (RT): **4.00**

---

### 1.5 Preemptive Priority Scheduling (1 = Highest)

- **Execution Order:**  
  - $t=0$: P1 starts (Pri 2).
  - $t=1$: P2 arrives with Pri 1 (strictly higher). P1 is **preempted**.
  - $t=1 \dots 4$: P2 runs to completion.
  - $t=4$: Ready processes: P1 (Pri 2, rem 4), P3 (Pri 3), P4 (Pri 4). P1 has highest priority and resumes.
  - $t=8$: P1 finishes. P3 (Pri 3) runs until $t=9$.
  - $t=9$: P4 (Pri 4) runs until $t=11$.  
  Order: `P1 → P2 → P1 → P3 → P4`
- **Gantt Chart:**
```text
+----+------+----------+----+----+
| P1 |  P2  |    P1    | P3 | P4 |
+----+------+----------+----+----+
0    1      4          8    9    11
```
- **Process Metrics:**

| PID | AT | BT | Priority | CT | TAT | WT | RT |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **P1** | 0 | 5 | 2 | 8 | 8 | 3 | 0 |
| **P2** | 1 | 3 | 1 | 4 | 3 | 0 | 0 |
| **P3** | 2 | 1 | 3 | 9 | 7 | 6 | 6 |
| **P4** | 3 | 2 | 4 | 11 | 8 | 6 | 6 |

- **Summary Statistics:**
  - Average Waiting Time (WT): **3.75**
  - Average Turnaround Time (TAT): **6.50**
  - Average Response Time (RT): **3.00**

---

### 1.6 Round Robin (Time Quantum $q = 2$)

- **Execution Order:**  
  - $t=0$: P1 runs for $q=2$ (rem 3). During this, P2 arrives ($t=1$) and P3 arrives ($t=2$). Queue: `[P2, P3, P1]`.
  - $t=2$: P2 runs for $q=2$ (rem 1). During this, P4 arrives ($t=3$). Queue: `[P3, P1, P4, P2]`.
  - $t=4$: P3 runs for 1 unit (finishes at $t=5$). Queue: `[P1, P4, P2]`.
  - $t=5$: P1 runs for $q=2$ (rem 1). Queue: `[P4, P2, P1]`.
  - $t=7$: P4 runs for $q=2$ (finishes at $t=9$). Queue: `[P2, P1]`.
  - $t=9$: P2 runs for 1 unit (finishes at $t=10$). Queue: `[P1]`.
  - $t=10$: P1 runs for 1 unit (finishes at $t=11$).  
  Order: `P1 → P2 → P3 → P1 → P4 → P2 → P1`
- **Gantt Chart:**
```text
+----+----+----+----+----+----+----+
| P1 | P2 | P3 | P1 | P4 | P2 | P1 |
+----+----+----+----+----+----+----+
0    2    4    5    7    9    10   11
```
- **Process Metrics:**

| PID | AT | BT | Priority | CT | TAT | WT | RT |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **P1** | 0 | 5 | 2 | 11 | 11 | 6 | 0 |
| **P2** | 1 | 3 | 1 | 10 | 9 | 6 | 1 |
| **P3** | 2 | 1 | 3 | 5 | 3 | 2 | 2 |
| **P4** | 3 | 2 | 4 | 9 | 6 | 4 | 4 |

- **Summary Statistics:**
  - Average Waiting Time (WT): **4.50**
  - Average Turnaround Time (TAT): **7.25**
  - Average Response Time (RT): **1.75**

---

## Test Case 2: CPU Idle Periods & Sparse Arrivals

### Process Dataset

| Process | Arrival Time (AT) | Burst Time (BT) | Priority |
|:---:|:---:|:---:|:---:|
| **P1** | 2 | 3 | 2 |
| **P2** | 8 | 2 | 1 |

### Execution & Gantt Chart (Both Preemptive and Non-preemptive)
- $t=0 \dots 2$: No process in ready queue $\rightarrow$ **IDLE**.
- $t=2 \dots 5$: P1 executes to completion ($CT=5$).
- $t=5 \dots 8$: No process in ready queue $\rightarrow$ **IDLE**.
- $t=8 \dots 10$: P2 executes to completion ($CT=10$).

```text
+------+------+------+----+
| IDLE |  P1  | IDLE | P2 |
+------+------+------+----+
0      2      5      8    10
```

- **Results:**
  - Total Simulation Time: **10 units**
  - Total Idle Time: **5 units**
  - CPU Utilization: **50.00%**
  - Both P1 and P2 have Waiting Time = **0.00** and Response Time = **0.00**.

---

## Test Case 3: Priority Preemption Stress Test

### Process Dataset

| Process | Arrival Time (AT) | Burst Time (BT) | Priority (1 = Highest) |
|:---:|:---:|:---:|:---:|
| **P1** | 0 | 6 | 3 |
| **P2** | 2 | 2 | 1 |

### Execution & Verification
- At $t=0$: P1 begins executing with lower priority (3).
- At $t=2$: P2 arrives with higher priority (1). P1 is **preempted** immediately with remaining burst 4.
- At $t=2 \dots 4$: P2 executes and completes.
- At $t=4 \dots 8$: P1 resumes and completes.

```text
+------+------+--------+
|  P1  |  P2  |   P1   |
+------+------+--------+
0      2      4        8
```

- **Metrics Verification:**
  - P2 Waiting Time: $4 - 2 - 2 = 0$
  - P1 Waiting Time: $8 - 0 - 6 = 2$ (interrupted for 2 units while P2 ran)
  - P1 Response Time: $0 - 0 = 0$ (got CPU immediately at $t=0$)
  - Status: **PASSED**
