/*
 * bankers.c - Implementation of Banker's Algorithm (Deadlock Avoidance)
 * Original Implementation: Nireeksha
 * Integrated by: Aditi Nayak (Team Leader)
 */

#include "bankers.h"
#include <stdio.h>

/* Check that Max is never less than Allocation */
int check_max_vs_alloc(const BankersState *s)
{
    for (int i = 0; i < s->n; i++) {
        for (int j = 0; j < s->m; j++) {
            if (s->max[i][j] < s->alloc[i][j]) {
                printf("Error: Max[%d][%d] = %d is less than Allocation[%d][%d] = %d\n",
                       i, j, s->max[i][j], i, j, s->alloc[i][j]);
                return 0;
            }
        }
    }
    return 1;
}

/* Need = Max - Allocation */
void calculate_need(BankersState *s)
{
    for (int i = 0; i < s->n; i++) {
        for (int j = 0; j < s->m; j++) {
            s->need[i][j] = s->max[i][j] - s->alloc[i][j];
        }
    }
}

/* Print the Need matrix */
void print_need(const BankersState *s)
{
    printf("\nNeed matrix:\n      ");
    for (int j = 0; j < s->m; j++)
        printf("R%-3d", j);
    printf("\n");
    for (int i = 0; i < s->n; i++) {
        printf("P%-4d ", i);
        for (int j = 0; j < s->m; j++)
            printf("%-4d", s->need[i][j]);
        printf("\n");
    }
}

/* Safety algorithm: Returns 1 if safe (fills seq with safe order), 0 if unsafe */
int is_safe(const BankersState *s, int seq[])
{
    int work[MAX_R];            /* Available resources work vector */
    int finished[MAX_P] = {0};  /* Tracks whether process can finish */
    int count = 0;              /* Processes in the safe sequence */

    /* Initialize work with the Available vector */
    for (int j = 0; j < s->m; j++)
        work[j] = s->avail[j];

    /* Find processes that can satisfy their need with available work */
    int found = 1;
    while (count < s->n && found) {
        found = 0;
        for (int i = 0; i < s->n; i++) {
            if (finished[i])
                continue;

            /* Can this process get everything it still needs? */
            int can_run = 1;
            for (int j = 0; j < s->m; j++) {
                if (s->need[i][j] > work[j]) {
                    can_run = 0;
                    break;
                }
            }

            if (can_run) {
                /* Process executes and releases all allocated resources */
                for (int j = 0; j < s->m; j++)
                    work[j] += s->alloc[i][j];
                finished[i] = 1;
                seq[count++] = i;
                found = 1;
            }
        }
    }

    /* Safe only if every process finishes */
    return (count == s->n);
}

/* Print the safe sequence (e.g. P1 -> P3 -> P4) */
void print_sequence(const BankersState *s, const int seq[])
{
    for (int i = 0; i < s->n; i++) {
        printf("P%d", seq[i]);
        if (i < s->n - 1)
            printf(" -> ");
    }
    printf("\n");
}

/* Handle resource request for process p: returns 1 if granted, 0 if denied */
int request_resources(BankersState *s, int p, const int req[])
{
    int seq[MAX_P];

    if (p < 0 || p >= s->n) {
        printf("Denied: process P%d does not exist.\n", p);
        return 0;
    }

    for (int j = 0; j < s->m; j++) {
        if (req[j] < 0) {
            printf("Denied: request for R%d is negative.\n", j);
            return 0;
        }
    }

    /* Condition 1: Request <= Need */
    for (int j = 0; j < s->m; j++) {
        if (req[j] > s->need[p][j]) {
            printf("Denied: P%d asks for more R%d (%d) than its Need (%d).\n",
                   p, j, req[j], s->need[p][j]);
            return 0;
        }
    }

    /* Condition 2: Request <= Available */
    for (int j = 0; j < s->m; j++) {
        if (req[j] > s->avail[j]) {
            printf("Denied: not enough R%d available (asked %d, have %d). P%d must wait.\n",
                   j, req[j], s->avail[j], p);
            return 0;
        }
    }

    /* Pretend to allocate requested resources */
    for (int j = 0; j < s->m; j++) {
        s->avail[j]    -= req[j];
        s->alloc[p][j] += req[j];
        s->need[p][j]  -= req[j];
    }

    /* Condition 3: Resulting state must be safe */
    if (is_safe(s, seq)) {
        printf("Granted: the new state is SAFE.\nSafe sequence: ");
        print_sequence(s, seq);
        return 1;
    }

    /* Roll back the pretend allocation if unsafe */
    for (int j = 0; j < s->m; j++) {
        s->avail[j]    += req[j];
        s->alloc[p][j] -= req[j];
        s->need[p][j]  += req[j];
    }
    printf("Denied: granting this request would leave the system UNSAFE.\n");
    return 0;
}

/* Check state and print safety result */
int run_bankers(const BankersState *s)
{
    int seq[MAX_P];

    if (is_safe(s, seq)) {
        printf("\nSystem is SAFE.\nSafe sequence: ");
        print_sequence(s, seq);
        return 1;
    }
    printf("\nUNSAFE (deadlock possible)\n");
    return 0;
}
