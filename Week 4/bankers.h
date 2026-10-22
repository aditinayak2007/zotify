/*
 * bankers.h - Header for Banker's Algorithm and Safety Analysis
 * Module Owner: Nireeksha
 * Integrated by: Aditi Nayak (Team Leader)
 */

#ifndef BANKERS_H
#define BANKERS_H

#include <stdio.h>

#define MAX_P 10   /* Maximum number of processes supported */
#define MAX_R 10   /* Maximum number of resource types supported */

/* Banker's Algorithm State Structure */
typedef struct {
    int n;                      /* Number of processes (1 to MAX_P) */
    int m;                      /* Number of resource types (1 to MAX_R) */
    int alloc[MAX_P][MAX_R];    /* Allocation Matrix */
    int max[MAX_P][MAX_R];      /* Maximum Requirement Matrix */
    int need[MAX_P][MAX_R];     /* Need Matrix (Need = Max - Allocation) */
    int avail[MAX_R];           /* Available Resources Vector */
} BankersState;

/* Function Prototypes */
int  check_max_vs_alloc(const BankersState *s);
void calculate_need(BankersState *s);
void print_need(const BankersState *s);
int  is_safe(const BankersState *s, int seq[]);
void print_sequence(const BankersState *s, const int seq[]);
int  request_resources(BankersState *s, int p, const int req[]);
int  run_bankers(const BankersState *s);

#endif /* BANKERS_H */
