/*
 * main.c - Interactive Deadlock Simulation System (Console / CLI Runner)
 * Team: Aditi Nayak (Leader & Integration), Anas (UI), Nireeksha (Banker's), Yaseem (Deadlock & Recovery)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bankers.h"
#include "deadlock.h"
#include "rag.h"
#include "recovery.h"

/* Helper to load standard Silberschatz benchmark (5 processes, 3 resource types) */
void load_silberschatz_preset(BankersState *bs, DeadlockState *ds)
{
    bs->n = 5;
    bs->m = 3;
    memset(bs->alloc, 0, sizeof(bs->alloc));
    memset(bs->max, 0, sizeof(bs->max));
    memset(bs->avail, 0, sizeof(bs->avail));

    int alloc[5][3] = {
        {0, 1, 0},
        {2, 0, 0},
        {3, 0, 2},
        {2, 1, 1},
        {0, 0, 2}
    };

    int max[5][3] = {
        {7, 5, 3},
        {3, 2, 2},
        {9, 0, 2},
        {2, 2, 2},
        {4, 3, 3}
    };

    int avail[3] = {3, 3, 2};

    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 3; j++) {
            bs->alloc[i][j] = alloc[i][j];
            bs->max[i][j] = max[i][j];
        }
    }
    for (int j = 0; j < 3; j++) {
        bs->avail[j] = avail[j];
    }
    calculate_need(bs);

    ds->n = 5;
    ds->m = 3;
    memset(ds->alloc, 0, sizeof(ds->alloc));
    memset(ds->avail, 0, sizeof(ds->avail));
    memset(ds->request, 0, sizeof(ds->request));

    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 3; j++) {
            ds->alloc[i][j] = alloc[i][j];
        }
    }
    for (int j = 0; j < 3; j++) {
        ds->avail[j] = avail[j];
    }

    printf("\n>>> [PRESET LOADED]: Silberschatz Safe State Benchmark (5 Processes, 3 Resources)\n");
}

/* Helper to load an actively deadlocked system preset */
void load_deadlocked_preset(BankersState *bs, DeadlockState *ds)
{
    /* 3 processes, 3 resources in circular wait */
    bs->n = 3;
    bs->m = 3;
    memset(bs->alloc, 0, sizeof(bs->alloc));
    memset(bs->max, 0, sizeof(bs->max));
    memset(bs->avail, 0, sizeof(bs->avail));

    int alloc[3][3] = {
        {1, 0, 0}, /* P0 holds R0 */
        {0, 1, 0}, /* P1 holds R1 */
        {0, 0, 1}  /* P2 holds R2 */
    };

    int max[3][3] = {
        {1, 1, 0}, /* P0 needs R1 */
        {0, 1, 1}, /* P1 needs R2 */
        {1, 0, 1}  /* P2 needs R0 */
    };

    int avail[3] = {0, 0, 0}; /* All instances allocated */

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            bs->alloc[i][j] = alloc[i][j];
            bs->max[i][j] = max[i][j];
        }
    }
    for (int j = 0; j < 3; j++) {
        bs->avail[j] = avail[j];
    }
    calculate_need(bs);

    ds->n = 3;
    ds->m = 3;
    memset(ds->alloc, 0, sizeof(ds->alloc));
    memset(ds->avail, 0, sizeof(ds->avail));
    memset(ds->request, 0, sizeof(ds->request));

    /* Outstanding Requests creating circular wait: P0 -> R1, P1 -> R2, P2 -> R0 */
    int req[3][3] = {
        {0, 1, 0},
        {0, 0, 1},
        {1, 0, 0}
    };

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            ds->alloc[i][j] = alloc[i][j];
            ds->request[i][j] = req[i][j];
        }
    }
    for (int j = 0; j < 3; j++) {
        ds->avail[j] = avail[j];
    }

    printf("\n>>> [PRESET LOADED]: Deadlocked System (Circular Wait P0 -> P1 -> P2 -> P0)\n");
}

void print_system_state(const BankersState *bs, const DeadlockState *ds)
{
    printf("\n======================= CURRENT SYSTEM STATE =======================\n");
    printf("Processes: %d | Resources: %d\n", bs->n, bs->m);
    printf("--------------------------------------------------------------------\n");
    printf("PID   Allocation       Max Need         Remaining Need   Request\n");
    printf("      ");
    for (int k = 0; k < 4; k++) {
        for (int j = 0; j < bs->m; j++) printf("R%d ", j);
        printf("  ");
    }
    printf("\n");

    for (int i = 0; i < bs->n; i++) {
        printf("P%-2d   ", i);
        /* Alloc */
        for (int j = 0; j < bs->m; j++) printf("%-2d ", bs->alloc[i][j]);
        printf("  ");
        /* Max */
        for (int j = 0; j < bs->m; j++) printf("%-2d ", bs->max[i][j]);
        printf("  ");
        /* Need */
        for (int j = 0; j < bs->m; j++) printf("%-2d ", bs->need[i][j]);
        printf("  ");
        /* Request */
        for (int j = 0; j < bs->m; j++) printf("%-2d ", ds->request[i][j]);
        printf("\n");
    }

    printf("--------------------------------------------------------------------\n");
    printf("Available Resources: ");
    for (int j = 0; j < bs->m; j++) {
        printf("R%d=%d  ", j, bs->avail[j]);
    }
    printf("\n====================================================================\n");
}

int main(void)
{
    BankersState bs;
    DeadlockState ds;
    RAG rag;
    int choice;

    load_silberschatz_preset(&bs, &ds);

    for (;;) {
        printf("\n==================================================\n");
        printf("   INTERACTIVE DEADLOCK SIMULATION SYSTEM (C CLI)\n");
        printf("   OS PBL Week 4 - Team Leader: Aditi Nayak\n");
        printf("==================================================\n");
        printf(" 1) View Current System State\n");
        printf(" 2) Run Banker's Algorithm (Safety Check & Safe Sequence)\n");
        printf(" 3) Request Resources (Banker's Avoidance)\n");
        printf(" 4) Run Deadlock Detection\n");
        printf(" 5) View Resource Allocation Graph (RAG)\n");
        printf(" 6) Recover from Deadlock\n");
        printf(" 7) Load Safe Preset (Silberschatz 5x3)\n");
        printf(" 8) Load Deadlocked Preset (Circular Wait 3x3)\n");
        printf(" 9) Exit\n");
        printf("--------------------------------------------------\n");
        printf("Select option (1-9): ");

        if (scanf("%d", &choice) != 1) {
            scanf("%*[^\n]");
            continue;
        }

        switch (choice) {
            case 1:
                print_system_state(&bs, &ds);
                break;

            case 2:
                printf("\n--- EXECUTING BANKER'S ALGORITHM ---\n");
                run_bankers(&bs);
                break;

            case 3: {
                int p, req[MAX_R];
                printf("Enter Process ID requesting resources (0 to %d): ", bs.n - 1);
                if (scanf("%d", &p) != 1 || p < 0 || p >= bs.n) {
                    printf("Invalid PID.\n");
                    scanf("%*[^\n]");
                    break;
                }
                printf("Enter request vector for %d resources: ", bs.m);
                int ok = 1;
                for (int j = 0; j < bs.m; j++) {
                    if (scanf("%d", &req[j]) != 1) ok = 0;
                }
                if (!ok) {
                    printf("Invalid request input.\n");
                    scanf("%*[^\n]");
                    break;
                }
                if (request_resources(&bs, p, req)) {
                    /* Synchronize DeadlockState */
                    for (int i = 0; i < bs.n; i++) {
                        for (int j = 0; j < bs.m; j++) {
                            ds.alloc[i][j] = bs.alloc[i][j];
                        }
                    }
                    for (int j = 0; j < bs.m; j++) {
                        ds.avail[j] = bs.avail[j];
                    }
                }
                break;
            }

            case 4: {
                int deadlocked[MAX_P];
                int count = 0;
                int res = run_deadlock_detection(&ds, deadlocked, &count);
                print_deadlock_report(res, deadlocked, count);
                break;
            }

            case 5:
                rag_build_from_deadlock_state(&rag, &ds);
                rag_print_text(&rag);
                break;

            case 6: {
                int deadlocked[MAX_P];
                int count = 0;
                int res = run_deadlock_detection(&ds, deadlocked, &count);
                if (!res) {
                    printf("\nNo deadlock exists. Recovery is not needed.\n");
                } else {
                    printf("\nSelect Recovery Mode:\n");
                    printf(" 1. Auto-Greedy Abort (Terminates process holding most resources)\n");
                    printf(" 2. Manual Abort (Choose specific victim process)\n");
                    printf("Choice: ");
                    int r_mode;
                    if (scanf("%d", &r_mode) == 1) {
                        if (r_mode == 1) {
                            int aborted[MAX_P], ab_cnt;
                            recover_greedy_auto(&ds, aborted, &ab_cnt);
                            /* Synchronize BankersState */
                            for (int i = 0; i < ds.n; i++) {
                                for (int j = 0; j < ds.m; j++) {
                                    bs.alloc[i][j] = ds.alloc[i][j];
                                }
                            }
                            for (int j = 0; j < ds.m; j++) {
                                bs.avail[j] = ds.avail[j];
                            }
                            calculate_need(&bs);
                        } else if (r_mode == 2) {
                            int victim;
                            printf("Enter victim PID to abort: ");
                            if (scanf("%d", &victim) == 1) {
                                int rem[MAX_P], r_cnt;
                                recover_abort_process(&ds, victim, rem, &r_cnt);
                                for (int i = 0; i < ds.n; i++) {
                                    for (int j = 0; j < ds.m; j++) {
                                        bs.alloc[i][j] = ds.alloc[i][j];
                                    }
                                }
                                for (int j = 0; j < ds.m; j++) {
                                    bs.avail[j] = ds.avail[j];
                                }
                                calculate_need(&bs);
                            }
                        }
                    }
                }
                break;
            }

            case 7:
                load_silberschatz_preset(&bs, &ds);
                break;

            case 8:
                load_deadlocked_preset(&bs, &ds);
                break;

            case 9:
                printf("\nExiting Deadlock Simulation System. Goodbye!\n");
                return 0;

            default:
                printf("Invalid option. Please choose between 1 and 9.\n");
                break;
        }
    }

    return 0;
}
