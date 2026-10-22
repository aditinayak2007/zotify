# Deadlock Simulation System — Test Cases & Verification Report

**Project:** Week 4 Interactive Deadlock Simulation System in C and Python  
**Lead & Integration:** Aditi Nayak (Team Leader)  
**Modules:** Anas Ahmed (UI & Visualization), Nireeksha (Banker's Algorithm & Need Matrix), Yaseem (Deadlock Detection, RAG, Recovery)

---

## Overview

This document provides complete documentation of all nine verification test cases executed against the Deadlock Simulation System. It covers:
- **Deadlock Avoidance** (Banker's Algorithm, Need Matrix calculation, Safe State determination, Safe Sequence generation).
- **Resource Request Validation** (Boundary validation against Need and Available, tentative state evaluation, rollback).
- **Deadlock Detection** (Multi-instance resource deadlock detection algorithm, identification of deadlocked processes).
- **Differentiation between Unsafe State and Deadlock** (Preventing false-positive deadlock diagnosis).
- **Resource Allocation Graph (RAG)** (Allocation edges $R_j \to P_i$, Request edges $P_i \to R_j$, Wait-For cycle detection).
- **Deadlock Recovery** (Process termination, resource reclamation, and post-recovery state verification).

---

## Test Case 1: Standard Safe State Benchmark (Silberschatz $5 \times 3$)

### 1.1 Initial Matrices

**System Dimensions:** 5 Processes ($P_0$ to $P_4$), 3 Resource Types ($R_0, R_1, R_2$)  
**Available Vector:** $[3, 3, 2]$  
**Total Instances in System:** $E = [10, 5, 7]$

| Process | Allocation ($R_0, R_1, R_2$) | Max ($R_0, R_1, R_2$) | Calculated Need ($\text{Max} - \text{Alloc}$) |
|:---:|:---:|:---:|:---:|
| **P0** | $0, 1, 0$ | $7, 5, 3$ | $7, 4, 3$ |
| **P1** | $2, 0, 0$ | $3, 2, 2$ | $1, 2, 2$ |
| **P2** | $3, 0, 2$ | $9, 0, 2$ | $6, 0, 0$ |
| **P3** | $2, 1, 1$ | $2, 2, 2$ | $0, 1, 1$ |
| **P4** | $0, 0, 2$ | $4, 3, 3$ | $4, 3, 1$ |

### 1.2 Banker's Safety Algorithm Execution Trace
1. **Initial Work:** $[3, 3, 2]$. $\text{Finish} = [\text{False}, \text{False}, \text{False}, \text{False}, \text{False}]$
2. **Step 1:** Test $P_0$: $\text{Need}(7, 4, 3) \le \text{Work}(3, 3, 2) \implies$ False.  
   Test $P_1$: $\text{Need}(1, 2, 2) \le \text{Work}(3, 3, 2) \implies$ **True**.  
   $P_1$ finishes: $\text{Work} = [3, 3, 2] + [2, 0, 0] = [5, 3, 2]$. $\text{Finish}[1] = \text{True}$. Sequence: $[P_1]$
3. **Step 2:** Test $P_3$: $\text{Need}(0, 1, 1) \le \text{Work}(5, 3, 2) \implies$ **True**.  
   $P_3$ finishes: $\text{Work} = [5, 3, 2] + [2, 1, 1] = [7, 4, 3]$. $\text{Finish}[3] = \text{True}$. Sequence: $[P_1, P_3]$
4. **Step 3:** Test $P_4$: $\text{Need}(4, 3, 1) \le \text{Work}(7, 4, 3) \implies$ **True**.  
   $P_4$ finishes: $\text{Work} = [7, 4, 3] + [0, 0, 2] = [7, 4, 5]$. $\text{Finish}[4] = \text{True}$. Sequence: $[P_1, P_3, P_4]$
5. **Step 4:** Test $P_0$: $\text{Need}(7, 4, 3) \le \text{Work}(7, 4, 5) \implies$ **True**.  
   $P_0$ finishes: $\text{Work} = [7, 4, 5] + [0, 1, 0] = [7, 5, 5]$. $\text{Finish}[0] = \text{True}$. Sequence: $[P_1, P_3, P_4, P_0]$
6. **Step 5:** Test $P_2$: $\text{Need}(6, 0, 0) \le \text{Work}(7, 5, 5) \implies$ **True**.  
   $P_2$ finishes: $\text{Work} = [7, 5, 5] + [3, 0, 2] = [10, 5, 7]$. $\text{Finish}[2] = \text{True}$. Sequence: $[P_1, P_3, P_4, P_0, P_2]$
- **System State:** **SAFE**
- **Verified Safe Sequence:** `P1 -> P3 -> P4 -> P0 -> P2`
- **Status:** **PASSED**

---

## Test Case 2: Valid Safe Resource Request

### 2.1 Action
- **Requesting Process:** $P_1$
- **Request Vector:** $\text{Request}_1 = [1, 0, 2]$
- **Validation:**
  - $\text{Request}_1 [1, 0, 2] \le \text{Need}_1 [1, 2, 2]$ (Condition satisfied)
  - $\text{Request}_1 [1, 0, 2] \le \text{Available} [3, 3, 2]$ (Condition satisfied)
- **Tentative Allocation:**
  - $\text{Available} = [3, 3, 2] - [1, 0, 2] = [2, 3, 0]$
  - $\text{Alloc}_1 = [2, 0, 0] + [1, 0, 2] = [3, 0, 2]$
  - $\text{Need}_1 = [1, 2, 2] - [1, 0, 2] = [0, 2, 0]$
- **Safety Check:**
  - With $\text{Work} = [2, 3, 0]$, $P_1$ can complete immediately ($\text{Need}_1 [0, 2, 0] \le [2, 3, 0]$), releasing $[3, 0, 2] \to \text{Work} = [5, 3, 2]$.
  - System remains in a safe state with safe sequence: `P1 -> P3 -> P4 -> P0 -> P2`.
- **Result:** **GRANTED**
- **Status:** **PASSED**

---

## Test Case 3: Unsafe Resource Request Rejection & Rollback

### 3.1 Action
- **Requesting Process:** $P_0$
- **Request Vector:** $\text{Request}_0 = [0, 3, 0]$
- **Validation:**
  - $\text{Request}_0 [0, 3, 0] \le \text{Need}_0 [7, 4, 3]$ (Condition satisfied)
  - $\text{Request}_0 [0, 3, 0] \le \text{Available} [3, 3, 2]$ (Condition satisfied)
- **Tentative Allocation:**
  - $\text{Available} = [3, 3, 2] - [0, 3, 0] = [3, 0, 2]$
  - $\text{Alloc}_0 = [0, 1, 0] + [0, 3, 0] = [0, 4, 0]$
  - $\text{Need}_0 = [7, 4, 3] - [0, 3, 0] = [7, 1, 3]$
- **Safety Evaluation on Tentative State:**
  - Initial Work: $[3, 0, 2]$.
  - $P_0$ Need $[7, 1, 3] > [3, 0, 2]$ (Insufficient $R_0, R_1, R_2$)
  - $P_1$ Need $[1, 2, 2] > [3, 0, 2]$ (Needs 2 of $R_1$, available 0)
  - $P_2$ Need $[6, 0, 0] > [3, 0, 2]$ (Needs 6 of $R_0$, available 3)
  - $P_3$ Need $[0, 1, 1] > [3, 0, 2]$ (Needs 1 of $R_1$, available 0)
  - $P_4$ Need $[4, 3, 1] > [3, 0, 2]$ (Needs 3 of $R_1$, available 0)
  - **No process can run.** The system enters an **UNSAFE STATE**.
- **Rollback Verification:**
  - Request is **DENIED**.
  - State rolled back: $\text{Available}[1] = 3$, $\text{Alloc}_0[1] = 1$, $\text{Need}_0[1] = 4$.
- **Status:** **PASSED**

---

## Test Case 4: Request Exceeding Declared Need

### 4.1 Action
- **Requesting Process:** $P_1$
- **Declared Remaining Need:** $[1, 2, 2]$
- **Request Vector:** $[2, 0, 0]$ (Demanding 2 instances of $R_0$ when remaining claim is only 1).
- **Validation:** Rejected at Condition 1 ($\text{Request}_1[0] > \text{Need}_1[0]$).
- **Output:** `Denied: P1 asks for more R0 (2) than its Need (1).`
- **Status:** **PASSED**

---

## Test Case 5: Request Exceeding Available Resources

### 5.1 Action
- **Requesting Process:** $P_0$
- **Available Vector:** $[3, 3, 2]$
- **Request Vector:** $[4, 0, 0]$
- **Validation:** Rejected at Condition 2 ($\text{Request}_0[0] > \text{Available}[0]$).
- **Output:** `Denied: not enough R0 available (asked 4, have 3). P0 must wait.`
- **Status:** **PASSED**

---

## Test Case 6: Deadlock Detection (Active Circular Wait)

### 6.1 State Configuration
- **Processes:** 3 ($P_0, P_1, P_2$), **Resources:** 3 ($R_0, R_1, R_2$)
- **Available Vector:** $[0, 0, 0]$
- **Allocation Matrix:**
  - $P_0$ holds $1$ of $R_0$: $[1, 0, 0]$
  - $P_1$ holds $1$ of $R_1$: $[0, 1, 0]$
  - $P_2$ holds $1$ of $R_2$: $[0, 0, 1]$
- **Outstanding Request Matrix:**
  - $P_0$ waiting for $R_1$: $[0, 1, 0]$
  - $P_1$ waiting for $R_2$: $[0, 0, 1]$
  - $P_2$ waiting for $R_0$: $[1, 0, 0]$

### 6.2 Deadlock Detection Execution
- $\text{Work} = [0, 0, 0]$.
- All processes hold allocated resources $\implies \text{Finish} = [\text{False}, \text{False}, \text{False}]$.
- In iteration 1: No process has $\text{Request} \le \text{Work}$. Loop terminates.
- **Deadlocked Processes:** $P_0, P_1, P_2$.
- **Detection Output:** `[ALERT] DEADLOCK DETECTED! Processes involved: P0, P1, P2`.
- **Status:** **PASSED**

---

## Test Case 7: Unsafe State vs. Actively Deadlocked State

### 7.1 Concept Verification
- **System:** 2 processes ($P_0, P_1$), 1 resource ($R_0$).
- Total instances: 2. $\text{Alloc} = [1, 1]$, $\text{Available} = [0]$.
- $\text{Max} = [2, 2]$. $\text{Need} = [1, 1]$.
- **Pending Requests:** $\text{Request} = [0, 0]$ (neither process has made a request yet).
- **Banker's Algorithm Assessment:** **UNSAFE** (if both processes simultaneously request their remaining 1 instance, deadlock will occur).
- **Deadlock Detection Assessment:** **NO DEADLOCK** (neither process is currently blocked waiting; processes can release resources or continue execution).
- **Conclusion:** The simulator correctly distinguishes between an *unsafe state* (future risk) and an *active deadlock* (present circular stall).
- **Status:** **PASSED**

---

## Test Case 8: Deadlock Recovery via Process Abort

### 8.1 Action
- **Initial State:** Deadlocked circular wait system from Test Case 6 ($P_0 \to P_1 \to P_2 \to P_0$).
- **Victim Selection:** Terminate process $P_0$.
- **Reclamation:**
  - $P_0$'s allocated $R_0$ released to Available $\implies \text{Available} = [1, 0, 0]$.
  - $P_0$'s allocation and requests reset to 0.
- **Post-Recovery Deadlock Detection:**
  - With $\text{Work} = [1, 0, 0]$, $P_2$'s request for $R_0$ can now be satisfied ($\text{Request}_2 [1, 0, 0] \le \text{Work}$).
  - $P_2$ finishes and releases $R_2 \implies \text{Work} = [1, 0, 1]$.
  - $P_1$'s request for $R_2$ can now be satisfied.
  - $P_1$ finishes and releases $R_1 \implies \text{Work} = [1, 1, 1]$.
  - All processes finish!
- **Output:** `>>> [SUCCESS] System successfully RECOVERED from deadlock after aborting P0!`
- **Status:** **PASSED**

---

## Test Case 9: Resource Allocation Graph (RAG) Construction & Cycle Detection

### 9.1 Verification
- **Edges in System:**
  - Allocation Edges ($R \to P$): $R_0 \to P_0$ (1 instance), $R_1 \to P_1$ (1 instance).
  - Request Edges ($P \to R$): $P_0 \to R_1$ (1 instance), $P_1 \to R_0$ (1 instance).
- Total RAG Edges: 4.
- **Wait-For Graph Construction:**
  - $P_0$ requests $R_1$, which is held by $P_1 \implies P_0 \to P_1$.
  - $P_1$ requests $R_0$, which is held by $P_0 \implies P_1 \to P_0$.
- **DFS Cycle Detection:** Directed cycle detected: $P_0 \leftrightarrow P_1$.
- **Cycle Length:** 2 nodes.
- **Status:** **PASSED**

---

## Summary of Verification Results

| Test # | Test Description | Algorithm Module | Expected Result | Actual Result | Status |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | Silberschatz Safe State & Sequence | Banker's (`bankers.c`) | Safe, `P1->P3->P4->P0->P2` | Safe, `P1->P3->P4->P0->P2` | **PASSED** |
| 2 | Safe Request by P1 $[1, 0, 2]$ | Banker's (`bankers.c`) | Granted, State Safe | Granted, State Safe | **PASSED** |
| 3 | Unsafe Request by P0 $[0, 3, 0]$ | Banker's (`bankers.c`) | Denied, State Rolled Back | Denied, State Rolled Back | **PASSED** |
| 4 | Request Exceeding Max Need | Validation (`bankers.c`) | Denied with Error | Denied with Error | **PASSED** |
| 5 | Request Exceeding Available | Validation (`bankers.c`) | Denied, Must Wait | Denied, Must Wait | **PASSED** |
| 6 | Active Circular Wait Deadlock | Detection (`deadlock.c`) | Deadlock: P0, P1, P2 | Deadlock: P0, P1, P2 | **PASSED** |
| 7 | Unsafe vs. Deadlock Distinction | Detection (`deadlock.c`) | No Deadlock | No Deadlock | **PASSED** |
| 8 | Deadlock Recovery via Abort P0 | Recovery (`recovery.c`) | Recovered, 0 Deadlocked | Recovered, 0 Deadlocked | **PASSED** |
| 9 | RAG Edge Mapping & Cycle Detection | Graph Engine (`rag.c`) | 4 Edges, Cycle Detected | 4 Edges, Cycle Detected | **PASSED** |

**Overall Verification Result:** 9 of 9 test suites passed (100%).
