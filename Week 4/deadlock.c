/*
 * deadlock.c - Deadlock Detection Algorithm Implementation
 * Module Owner: Yaseem
 * Integrated by: Aditi Nayak (Team Leader)
 */

#include "deadlock.h"
#include <stdio.h>

/*
 * Multi-Resource Deadlock Detection Algorithm:
 * 1. Work = Available
 * 2. For i = 0 to n-1:
 *      If Alloc[i] != 0: Finish[i] = 0
 *      Else: Finish[i] = 1 (process has no allocated resources)
 * 3. Find an i such that Finish[i] == 0 and Request[i] <= Work
 *      If found:
 *          Work += Alloc[i]
 *          Finish[i] = 1
 *          Repeat step 3
 * 4. If Finish[i] == 0 for any i, process i is deadlocked.
 */
int detect_deadlock(int n, int m,
                    const int alloc[MAX_P][MAX_R],
                    const int req[MAX_P][MAX_R],
                    const int avail[MAX_R],
                    int deadlocked_procs[],
                    int *deadlocked_count)
{
    int work[MAX_R];
    int finish[MAX_P];
    int i, j;

    /* Initialize Work = Available */
    for (j = 0; j < m; j++) {
        work[j] = avail[j];
    }

    /* Initialize Finish vector */
    for (i = 0; i < n; i++) {
        int has_allocation = 0;
        for (j = 0; j < m; j++) {
            if (alloc[i][j] > 0) {
                has_allocation = 1;
                break;
            }
        }
        if (has_allocation) {
            finish[i] = 0;
        } else {
            finish[i] = 1;
        }
    }

    /* Progress loop */
    int found = 1;
    while (found) {
        found = 0;
        for (i = 0; i < n; i++) {
            if (finish[i] == 0) {
                int can_satisfy = 1;
                for (j = 0; j < m; j++) {
                    if (req[i][j] > work[j]) {
                        can_satisfy = 0;
                        break;
                    }
                }

                if (can_satisfy) {
                    /* Process can finish and release its allocated resources */
                    for (j = 0; j < m; j++) {
                        work[j] += alloc[i][j];
                    }
                    finish[i] = 1;
                    found = 1;
                }
            }
        }
    }

    /* Collect deadlocked processes */
    int count = 0;
    for (i = 0; i < n; i++) {
        if (finish[i] == 0) {
            deadlocked_procs[count++] = i;
        }
    }

    *deadlocked_count = count;
    return (count > 0) ? 1 : 0;
}

int run_deadlock_detection(const DeadlockState *ds, int deadlocked_procs[], int *deadlocked_count)
{
    return detect_deadlock(ds->n, ds->m, ds->alloc, ds->request, ds->avail, deadlocked_procs, deadlocked_count);
}

void print_deadlock_report(int is_deadlocked, const int deadlocked_procs[], int count)
{
    if (is_deadlocked) {
        printf("\n==================================================\n");
        printf(" [ALERT] DEADLOCK DETECTED IN THE SYSTEM!\n");
        printf(" Number of deadlocked processes: %d\n", count);
        printf(" Processes involved in deadlock: ");
        for (int i = 0; i < count; i++) {
            printf("P%d%s", deadlocked_procs[i], (i < count - 1) ? ", " : "\n");
        }
        printf(" Recommendation: Initiate Deadlock Recovery.\n");
        printf("==================================================\n");
    } else {
        printf("\n==================================================\n");
        printf(" [OK] NO DEADLOCK DETECTED.\n");
        printf(" All processes can proceed to completion.\n");
        printf("==================================================\n");
    }
}

int submit_request(DeadlockState *ds, int p, const int req_vec[])
{
    if (p < 0 || p >= ds->n) {
        printf("Error: Process P%d does not exist.\n", p);
        return 0;
    }

    int can_allocate = 1;
    for (int j = 0; j < ds->m; j++) {
        if (req_vec[j] < 0) {
            printf("Error: Negative request for R%d.\n", j);
            return 0;
        }
        if (req_vec[j] > ds->avail[j]) {
            can_allocate = 0;
        }
    }

    if (can_allocate) {
        /* Allocate immediately */
        for (int j = 0; j < ds->m; j++) {
            ds->avail[j] -= req_vec[j];
            ds->alloc[p][j] += req_vec[j];
            ds->request[p][j] = 0; /* Request satisfied */
        }
        printf("Request for P%d granted immediately.\n", p);
        return 1;
    } else {
        /* Cannot allocate immediately; record as pending request */
        for (int j = 0; j < ds->m; j++) {
            ds->request[p][j] += req_vec[j];
        }
        printf("Request for P%d cannot be granted immediately. Marked as pending.\n", p);
        return 2; /* 2 indicates pending */
    }
}
