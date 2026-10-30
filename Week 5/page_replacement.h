/*
 * page_replacement.h - Page Replacement Algorithms & Performance Evaluation
 * Operating Systems Project-Based Learning (Week 5)
 *
 * Team Roles:
 * - Aditi Nayak (Team Leader): Integration, Testing, Debugging, Documentation
 * - Anas Ahmed: GUI, Input Handling, Result Presentation
 * - Nireeksha: FIFO and LRU Algorithms
 * - Yaseem: Optimal Algorithm, Performance Calculations, Comparative Engine
 */

#ifndef PAGE_REPLACEMENT_H
#define PAGE_REPLACEMENT_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PAGES 200
#define MAX_FRAMES 50

/* Single step of simulation representing the state after a page request */
typedef struct {
    int page;                     /* Page requested at this step */
    int frames[MAX_FRAMES];       /* Frame contents (-1 indicates empty) */
    int capacity;                 /* Number of frames allocated */
    int is_hit;                   /* 1 = Page Hit, 0 = Page Fault */
} PageStep;

/* Comprehensive simulation result containing step history and performance metrics */
typedef struct {
    char algorithm_name[32];      /* "FIFO", "LRU", or "Optimal" */
    int total_references;         /* Total number of page requests */
    int hits;                     /* Total page hits */
    int faults;                   /* Total page faults */
    double hit_ratio;             /* (hits / total_references) * 100 */
    double fault_ratio;           /* (faults / total_references) * 100 */
    PageStep steps[MAX_PAGES];    /* Recorded step-by-step history */
    int step_count;               /* Number of steps recorded */
} SimulationResult;

/* Algorithm Prototypes */
void fifo_simulate(const int pages[], int n, int capacity, SimulationResult *result);
void lru_simulate(const int pages[], int n, int capacity, SimulationResult *result);
void optimal_simulate(const int pages[], int n, int capacity, SimulationResult *result);

/* Performance Calculation & Analysis */
void calculate_metrics(SimulationResult *res);
void compare_all_algorithms(const int pages[], int n, int capacity, SimulationResult results[3]);
int  find_best_algorithm(const SimulationResult results[3]); /* Returns index of algorithm with minimum faults */

/* Display Utilities */
void print_simulation_table(const SimulationResult *res);
void print_comparison_table(const SimulationResult results[3]);

#endif /* PAGE_REPLACEMENT_H */
