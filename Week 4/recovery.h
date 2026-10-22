/*
 * recovery.h - Header for Deadlock Recovery Strategies
 * Module Owner: Yaseem
 * Integrated by: Aditi Nayak (Team Leader)
 */

#ifndef RECOVERY_H
#define RECOVERY_H

#include "deadlock.h"

/* Recovery Strategy Types */
typedef enum {
    RECOVERY_ABORT_SINGLE,  /* Abort a specific victim process */
    RECOVERY_ABORT_GREEDY,  /* Automatically abort the process holding the most resources */
    RECOVERY_ABORT_ALL,     /* Abort all deadlocked processes */
    RECOVERY_PREEMPT        /* Preempt specific resources from a process */
} RecoveryStrategy;

/* Function Prototypes */

/*
 * recover_abort_process:
 * Aborts process `victim_pid`, releases all its held resources back to Available,
 * resets its requests, and re-checks for remaining deadlock.
 * Returns 1 if system is now completely free of deadlock, 0 if deadlock still persists.
 */
int recover_abort_process(DeadlockState *ds, int victim_pid, int remaining_deadlock[], int *rem_count);

/*
 * recover_greedy_auto:
 * Automatically selects and aborts deadlocked processes one by one (prioritizing the
 * one holding the largest total allocation) until the system is completely recovered.
 * Records the list of aborted PIDs in aborted_pids[] and sets *aborted_count.
 */
int recover_greedy_auto(DeadlockState *ds, int aborted_pids[], int *aborted_count);

/*
 * recover_preempt_resource:
 * Preempts `amount` of resource `res_type` from process `pid`, returning them to Available.
 */
int recover_preempt_resource(DeadlockState *ds, int pid, int res_type, int amount);

#endif /* RECOVERY_H */
