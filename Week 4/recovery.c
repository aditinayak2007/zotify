/*
 * recovery.c - Implementation of Deadlock Recovery Strategies
 * Module Owner: Yaseem
 * Integrated by: Aditi Nayak (Team Leader)
 */

#include "recovery.h"
#include <stdio.h>

int recover_abort_process(DeadlockState *ds, int victim_pid, int remaining_deadlock[], int *rem_count)
{
    if (victim_pid < 0 || victim_pid >= ds->n) {
        printf("Error: Invalid victim PID P%d\n", victim_pid);
        return 0;
    }

    printf("\n[RECOVERY ACTION]: Aborting Process P%d...\n", victim_pid);
    printf("Reclaiming allocated resources from P%d: ", victim_pid);

    /* Release all allocated resources to Available */
    for (int j = 0; j < ds->m; j++) {
        int freed = ds->alloc[victim_pid][j];
        if (freed > 0) {
            ds->avail[j] += freed;
            ds->alloc[victim_pid][j] = 0;
            printf("R%d (+%d)  ", j, freed);
        }
        /* Clear pending requests */
        ds->request[victim_pid][j] = 0;
    }
    printf("\nUpdated Available Resources Vector: ");
    for (int j = 0; j < ds->m; j++) {
        printf("R%d=%d ", j, ds->avail[j]);
    }
    printf("\n");

    /* Re-evaluate system state for deadlocks */
    int has_deadlock = run_deadlock_detection(ds, remaining_deadlock, rem_count);
    if (!has_deadlock) {
        printf(">>> [SUCCESS] System successfully RECOVERED from deadlock after aborting P%d!\n", victim_pid);
        return 1;
    } else {
        printf(">>> [NOTICE] Deadlock still persists with %d processes remaining.\n", *rem_count);
        return 0;
    }
}

int recover_greedy_auto(DeadlockState *ds, int aborted_pids[], int *aborted_count)
{
    int deadlocked[MAX_P];
    int count = 0;
    *aborted_count = 0;

    int has_deadlock = run_deadlock_detection(ds, deadlocked, &count);
    if (!has_deadlock) {
        printf("No deadlock present. No recovery needed.\n");
        return 1;
    }

    printf("\n>>> Commencing Greedy Deadlock Recovery...\n");
    while (has_deadlock && count > 0) {
        /* Find deadlocked process holding the most total resources */
        int best_victim = -1;
        int max_held = -1;

        for (int i = 0; i < count; i++) {
            int p = deadlocked[i];
            int total_held = 0;
            for (int j = 0; j < ds->m; j++) {
                total_held += ds->alloc[p][j];
            }
            if (total_held > max_held) {
                max_held = total_held;
                best_victim = p;
            }
        }

        if (best_victim == -1) {
            /* Fallback to first deadlocked process */
            best_victim = deadlocked[0];
        }

        aborted_pids[(*aborted_count)++] = best_victim;
        int rem_deadlock[MAX_P];
        int rem_cnt = 0;
        int recovered = recover_abort_process(ds, best_victim, rem_deadlock, &rem_cnt);
        if (recovered) {
            printf(">>> Greedy recovery completed with %d process(es) aborted.\n", *aborted_count);
            return 1;
        }

        /* Update deadlock list for next iteration */
        has_deadlock = run_deadlock_detection(ds, deadlocked, &count);
    }

    return 1;
}

int recover_preempt_resource(DeadlockState *ds, int pid, int res_type, int amount)
{
    if (pid < 0 || pid >= ds->n || res_type < 0 || res_type >= ds->m) {
        printf("Error: Invalid PID or Resource Type.\n");
        return 0;
    }

    if (amount <= 0 || amount > ds->alloc[pid][res_type]) {
        printf("Error: Cannot preempt %d of R%d from P%d (holds %d).\n",
               amount, res_type, pid, ds->alloc[pid][res_type]);
        return 0;
    }

    ds->alloc[pid][res_type] -= amount;
    ds->avail[res_type] += amount;
    /* Process will now request this resource back */
    ds->request[pid][res_type] += amount;

    printf("[PREEMPTION]: Preempted %d of R%d from P%d. Added to Available.\n",
           amount, res_type, pid);
    return 1;
}
