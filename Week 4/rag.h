/*
 * rag.h - Resource Allocation Graph (RAG) Header
 * Module Owner: Yaseem
 * Integrated by: Aditi Nayak (Team Leader)
 */

#ifndef RAG_H
#define RAG_H

#include "bankers.h"
#include "deadlock.h"

/* Structure to store graph edge */
typedef struct {
    int from;       /* Source node index */
    int to;         /* Destination node index */
    int weight;     /* Multiplicity / Instance count */
    int is_request; /* 1 if Request (P -> R), 0 if Allocation (R -> P) */
} RagEdge;

#define MAX_EDGES 100

typedef struct {
    int n_procs;
    int n_resources;
    int edge_count;
    RagEdge edges[MAX_EDGES];
} RAG;

/* Function Prototypes */
void rag_build_from_deadlock_state(RAG *rag, const DeadlockState *ds);
void rag_build_from_bankers_state(RAG *rag, const BankersState *bs);
void rag_print_text(const RAG *rag);
void rag_print_adjacency(const RAG *rag);
int  rag_detect_cycle_waitfor(int n, const int alloc[MAX_P][MAX_R], const int req[MAX_P][MAX_R], int cycle_nodes[], int *cycle_len);

#endif /* RAG_H */
