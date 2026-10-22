/*
 * deadlock.h - Header for Deadlock Detection and Pending Request Management
 * Module Owner: Yaseem
 * Integrated by: Aditi Nayak (Team Leader)
 */

#ifndef DEADLOCK_H
#define DEADLOCK_H

#include "bankers.h"

/* Structure representing system state for Deadlock Detection */
typedef struct {
    int n;                          /* Number of processes */
    int m;                          /* Number of resource types */
    int alloc[MAX_P][MAX_R];        /* Allocation Matrix */
    int request[MAX_P][MAX_R];      /* Current Pending Request Matrix */
    int avail[MAX_R];               /* Available Vector */
} DeadlockState;

/* Function Prototypes */

/*
 * detect_deadlock:
 * Executes the multi-instance resource deadlock detection algorithm.
 * Returns 1 if deadlock is detected, 0 if no deadlock.
 * Fills deadlocked_procs[] with the PIDs of deadlocked processes and sets *deadlocked_count.
 */
int detect_deadlock(int n, int m,
                    const int alloc[MAX_P][MAX_R],
                    const int req[MAX_P][MAX_R],
                    const int avail[MAX_R],
                    int deadlocked_procs[],
                    int *deadlocked_count);

/* Convenience wrapper taking a DeadlockState pointer */
int run_deadlock_detection(const DeadlockState *ds, int deadlocked_procs[], int *deadlocked_count);

/* Formatted report printer */
void print_deadlock_report(int is_deadlocked, const int deadlocked_procs[], int count);

/* Immediate resource request without avoidance (updates allocation or records pending request) */
int submit_request(DeadlockState *ds, int p, const int req_vec[]);

#endif /* DEADLOCK_H */
