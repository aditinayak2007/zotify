# Page Replacement Algorithms — Test Cases & Verification Report

**Course:** Operating Systems Laboratory / Project-Based Learning (Week 5)  
**Project Title:** Simulation and Comparative Analysis of Page Replacement Algorithms  
**Lead & Integration:** Aditi Nayak (Team Leader)  
**Module Owners:** Anas Ahmed (GUI & Visualization), Nireeksha (FIFO & LRU), Yaseem (Optimal & Comparison)

---

## Overview

This report provides complete documentation of verified test cases, step-by-step frame contents, hit/fault tracking, and performance metrics across the three implemented page replacement algorithms:
1. **First-In, First-Out (FIFO)**
2. **Least Recently Used (LRU)**
3. **Optimal Page Replacement (OPT / MIN)**

---

## Test Case 1: Course Specification Benchmark

### Input Parameters
- **Page-Reference String:** `7 0 1 2 0 3 0 4 2 3`
- **Total References ($N$):** 10
- **Number of Frames ($M$):** 3

---

### 1.1 First-In, First-Out (FIFO) Simulation

| Step | Page Ref | Frame 0 | Frame 1 | Frame 2 | Result | Explanation |
|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | 7 | 7 | - | - | **FAULT** | Page 7 loaded into empty Frame 0. Pointer moves to Frame 1. |
| **2** | 0 | 7 | 0 | - | **FAULT** | Page 0 loaded into empty Frame 1. Pointer moves to Frame 2. |
| **3** | 1 | 7 | 0 | 1 | **FAULT** | Page 1 loaded into empty Frame 2. Pointer wraps to Frame 0. |
| **4** | 2 | 2 | 0 | 1 | **FAULT** | All frames full. Oldest page (7) at pointer 0 evicted for 2. Pointer moves to Frame 1. |
| **5** | 0 | 2 | 0 | 1 | **HIT** | Page 0 is already present in Frame 1. Pointer remains at Frame 1. |
| **6** | 3 | 2 | 3 | 1 | **FAULT** | Page 0 at pointer 1 evicted for 3. Pointer moves to Frame 2. |
| **7** | 0 | 2 | 3 | 0 | **FAULT** | Page 1 at pointer 2 evicted for 0. Pointer wraps to Frame 0. |
| **8** | 4 | 4 | 3 | 0 | **FAULT** | Page 2 at pointer 0 evicted for 4. Pointer moves to Frame 1. |
| **9** | 2 | 4 | 2 | 0 | **FAULT** | Page 3 at pointer 1 evicted for 2. Pointer moves to Frame 2. |
| **10** | 3 | 4 | 2 | 3 | **FAULT** | Page 0 at pointer 2 evicted for 3. Pointer wraps to Frame 0. |

- **Total References:** 10
- **Total Hits:** 1 (at Step 5)
- **Total Faults:** 9
- **Hit Ratio:** $\frac{1}{10} \times 100\% = \mathbf{10.00\%}$
- **Fault Ratio:** $\frac{9}{10} \times 100\% = \mathbf{90.00\%}$
- **Invariant:** $\text{Hits} + \text{Faults} = 1 + 9 = 10 = \text{Total References}$.
- **Verification Status:** **100% PASSED** (Matches project specification).

---

### 1.2 Least Recently Used (LRU) Simulation

| Step | Page Ref | Frame 0 | Frame 1 | Frame 2 | Result | Explanation |
|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | 7 | 7 | - | - | **FAULT** | Loaded into empty Frame 0. Last used at step 1. |
| **2** | 0 | 7 | 0 | - | **FAULT** | Loaded into empty Frame 1. Last used at step 2. |
| **3** | 1 | 7 | 0 | 1 | **FAULT** | Loaded into empty Frame 2. Last used at step 3. |
| **4** | 2 | 2 | 0 | 1 | **FAULT** | Frame full. Least recently used page is 7 (step 1). Evicted for 2. |
| **5** | 0 | 2 | 0 | 1 | **HIT** | Page 0 present in Frame 1. Timestamp updated to step 5. |
| **6** | 3 | 2 | 0 | 3 | **FAULT** | Recent usages: 2 (step 4), 0 (step 5), 1 (step 3). Page 1 is LRU! Evicted for 3. |
| **7** | 0 | 2 | 0 | 3 | **HIT** | Page 0 present in Frame 1. Timestamp updated to step 7. |
| **8** | 4 | 4 | 0 | 3 | **FAULT** | Recent usages: 0 (step 7), 3 (step 6), 2 (step 4). Page 2 is LRU! Evicted for 4. |
| **9** | 2 | 4 | 0 | 2 | **FAULT** | Recent usages: 4 (step 8), 0 (step 7), 3 (step 6). Page 3 is LRU! Evicted for 2. |
| **10** | 3 | 4 | 3 | 2 | **FAULT** | Recent usages: 2 (step 9), 4 (step 8), 0 (step 7). Page 0 is LRU! Evicted for 3. |

- **Total References:** 10
- **Total Hits:** 2 (at Steps 5 and 7)
- **Total Faults:** 8
- **Hit Ratio:** $\frac{2}{10} \times 100\% = \mathbf{20.00\%}$
- **Fault Ratio:** $\frac{8}{10} \times 100\% = \mathbf{80.00\%}$
- **Verification Status:** **100% PASSED**.

---

### 1.3 Optimal Page Replacement (OPT / MIN) Simulation

| Step | Page Ref | Frame 0 | Frame 1 | Frame 2 | Result | Explanation |
|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | 7 | 7 | - | - | **FAULT** | Loaded into Frame 0. |
| **2** | 0 | 7 | 0 | - | **FAULT** | Loaded into Frame 1. |
| **3** | 1 | 7 | 0 | 1 | **FAULT** | Loaded into Frame 2. |
| **4** | 2 | 2 | 0 | 1 | **FAULT** | Frames full. Future uses: 0 at step 5, 1 never, 7 never. First never-used page 7 evicted for 2. |
| **5** | 0 | 2 | 0 | 1 | **HIT** | Page 0 present in Frame 1. |
| **6** | 3 | 2 | 0 | 3 | **FAULT** | Future uses: 0 at step 7, 2 at step 9, 1 never. Page 1 never used again. Evicted for 3. |
| **7** | 0 | 2 | 0 | 3 | **HIT** | Page 0 present in Frame 1. |
| **8** | 4 | 2 | 4 | 3 | **FAULT** | Future uses: 2 at step 9, 3 at step 10, 0 never. Page 0 never used again. Evicted for 4. |
| **9** | 2 | 2 | 4 | 3 | **HIT** | Page 2 present in Frame 0. |
| **10** | 3 | 2 | 4 | 3 | **HIT** | Page 3 present in Frame 2. |

- **Total References:** 10
- **Total Hits:** 4 (at Steps 5, 7, 9, 10)
- **Total Faults:** 6
- **Hit Ratio:** $\frac{4}{10} \times 100\% = \mathbf{40.00\%}$
- **Fault Ratio:** $\frac{6}{10} \times 100\% = \mathbf{60.00\%}$
- **Verification Status:** **100% PASSED**.

---

### 1.4 Comparative Performance Summary

| Algorithm | Total References | Page Hits | Page Faults | Hit Ratio (%) | Fault Ratio (%) | Outcome |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **FIFO** | 10 | 1 | 9 | 10.00% | 90.00% | Highest fault count (Convoy / queue eviction) |
| **LRU** | 10 | 2 | 8 | 20.00% | 80.00% | Moderate improvement over FIFO |
| **Optimal** | 10 | **4** | **6** | **40.00%** | **60.00%** | **★ Best Performance (Minimum Page Faults: 6)** |

---

## Test Case 2: Increased Frame Capacity (4 Frames on Benchmark)

- **Input:** `7 0 1 2 0 3 0 4 2 3`, Capacity = 4
- **Observations:**
  - FIFO: Hits = 4, Faults = 6, Hit Ratio = 40.00%
  - LRU: Hits = 4, Faults = 6, Hit Ratio = 40.00%
  - Optimal: Hits = 4, Faults = 6, Hit Ratio = 40.00%
- **Status:** **PASSED**.

---

## Test Case 3: Repeated Identical Page References

- **Input:** `1 1 1 1 1`, Capacity = 3
- **Expected Result:**
  - Step 1: Compulsory fault (Page 1 loaded).
  - Steps 2 to 5: 4 consecutive hits.
  - Hits = 4, Faults = 1, Hit Ratio = 80.00%, Fault Ratio = 20.00%.
- **Status:** **PASSED** across all algorithms.

---

## Test Case 4: Single Page Reference

- **Input:** `5`, Capacity = 3
- **Expected Result:** Total References = 1, Hits = 0, Faults = 1, Hit Ratio = 0.00%, Fault Ratio = 100.00%.
- **Status:** **PASSED** across all algorithms.

---

## Test Case 5: Capacity Exceeding Unique Pages (No Replacement)

- **Input:** `1 2 3 1 2`, Capacity = 5
- **Expected Result:** 3 compulsory faults, 2 hits, 0 evictions.
- **Status:** **PASSED**.

---

## Test Case 6: Belady's Anomaly Demonstration (FIFO)

- **Reference String:** `1 2 3 4 1 2 5 1 2 3 4 5`
- **Result with 3 Frames:** 9 Page Faults.
- **Result with 4 Frames:** 10 Page Faults.
- **Observation:** FIFO exhibits Belady's Anomaly where increasing allocated frame capacity from 3 to 4 increases the total page faults from 9 to 10.
- **Contrast:** LRU and Optimal (stack algorithms) do not suffer from Belady's Anomaly.
- **Status:** **PASSED**.

---

## Test Suite Execution Summary

| Test Category | Test Case | Target Metric / Invariant | Status |
|:---|:---|:---|:---:|
| **Standard Spec** | FIFO 3 Frames | 10 refs, 1 hit, 9 faults, 10% hit ratio | **PASSED** |
| **Standard Spec** | LRU 3 Frames | 10 refs, 2 hits, 8 faults, 20% hit ratio | **PASSED** |
| **Standard Spec** | Optimal 3 Frames | 10 refs, 4 hits, 6 faults, 40% hit ratio | **PASSED** |
| **Comparison** | Best Algorithm Selection | Optimal identified with minimum faults (6) | **PASSED** |
| **Invariant** | Hit + Fault = Total | Validated across all test executions | **PASSED** |
| **Scale** | 4 Frames Benchmark | 4 hits, 6 faults across all algorithms | **PASSED** |
| **Edge Case** | Repeated Pages `1 1 1 1 1` | 4 hits, 1 fault | **PASSED** |
| **Edge Case** | Single Page `5` | 0 hits, 1 fault | **PASSED** |
| **Boundary** | Frames > Unique Pages | Empty slots preserved, no replacements | **PASSED** |
| **Anomaly** | Belady's Anomaly | 9 faults (3 frames) vs 10 faults (4 frames) | **PASSED** |

**Total Assertions Verified:** 34 in C test runner + 7 in Python test suite = **41 Total Passed Assertions (100%)**.
