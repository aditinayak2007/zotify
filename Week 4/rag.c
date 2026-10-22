/*
 * rag.c - Resource Allocation Graph (RAG) Implementation
 * Module Owner: Yaseem
 * Integrated by: Aditi Nayak (Team Leader)
 */

#include "rag.h"
#include <stdio.h>
#include <string.h>

void rag_build_from_deadlock_state(RAG *rag, const DeadlockState *ds)
{
    rag->n_procs = ds->n;
    rag->n_resources = ds->m;
    rag->edge_count = 0;

    /* Add Allocation Edges: R_j -> P_i */
    for (int i = 0; i < ds->n; i++) {
        for (int j = 0; j < ds->m; j++) {
            if (ds->alloc[i][j] > 0 && rag->edge_count < MAX_EDGES) {
                rag->edges[rag->edge_count].from = j; /* R_j */
                rag->edges[rag->edge_count].to = i;   /* P_i */
                rag->edges[rag->edge_count].weight = ds->alloc[i][j];
                rag->edges[rag->edge_count].is_request = 0;
                rag->edge_count++;
            }
        }
    }

    /* Add Request Edges: P_i -> R_j */
    for (int i = 0; i < ds->n; i++) {
        for (int j = 0; j < ds->m; j++) {
            if (ds->request[i][j] > 0 && rag->edge_count < MAX_EDGES) {
                rag->edges[rag->edge_count].from = i; /* P_i */
                rag->edges[rag->edge_count].to = j;   /* R_j */
                rag->edges[rag->edge_count].weight = ds->request[i][j];
                rag->edges[rag->edge_count].is_request = 1;
                rag->edge_count++;
            }
        }
    }
}

void rag_build_from_bankers_state(RAG *rag, const BankersState *bs)
{
    rag->n_procs = bs->n;
    rag->n_resources = bs->m;
    rag->edge_count = 0;

    /* Allocation Edges: R_j -> P_i */
    for (int i = 0; i < bs->n; i++) {
        for (int j = 0; j < bs->m; j++) {
            if (bs->alloc[i][j] > 0 && rag->edge_count < MAX_EDGES) {
                rag->edges[rag->edge_count].from = j;
                rag->edges[rag->edge_count].to = i;
                rag->edges[rag->edge_count].weight = bs->alloc[i][j];
                rag->edges[rag->edge_count].is_request = 0;
                rag->edge_count++;
            }
        }
    }

    /* Need / Claim Edges: P_i -> R_j */
    for (int i = 0; i < bs->n; i++) {
        for (int j = 0; j < bs->m; j++) {
            if (bs->need[i][j] > 0 && rag->edge_count < MAX_EDGES) {
                rag->edges[rag->edge_count].from = i;
                rag->edges[rag->edge_count].to = j;
                rag->edges[rag->edge_count].weight = bs->need[i][j];
                rag->edges[rag->edge_count].is_request = 1;
                rag->edge_count++;
            }
        }
    }
}

void rag_print_text(const RAG *rag)
{
    printf("\n================ RESOURCE ALLOCATION GRAPH ================\n");
    printf(" Nodes: %d Processes (P0-P%d), %d Resources (R0-R%d)\n",
           rag->n_procs, rag->n_procs - 1,
           rag->n_resources, rag->n_resources - 1);
    printf(" Total Directed Edges: %d\n", rag->edge_count);
    printf("-----------------------------------------------------------\n");
    printf(" [Allocation Edges (R -> P)]:\n");
    int alloc_found = 0;
    for (int i = 0; i < rag->edge_count; i++) {
        if (!rag->edges[i].is_request) {
            printf("   R%d ---[%d instances]---> P%d\n",
                   rag->edges[i].from, rag->edges[i].weight, rag->edges[i].to);
            alloc_found = 1;
        }
    }
    if (!alloc_found) printf("   (None)\n");

    printf("\n [Request Edges (P -> R)]:\n");
    int req_found = 0;
    for (int i = 0; i < rag->edge_count; i++) {
        if (rag->edges[i].is_request) {
            printf("   P%d ---[requests %d]---> R%d\n",
                   rag->edges[i].from, rag->edges[i].weight, rag->edges[i].to);
            req_found = 1;
        }
    }
    if (!req_found) printf("   (None)\n");
    printf("===========================================================\n");
}

/* Helper for DFS cycle finding in Wait-For graph */
static int dfs_waitfor(int u, int n, const int adj[MAX_P][MAX_P],
                       int visited[], int rec_stack[], int parent[], int *cycle_start, int *cycle_end)
{
    visited[u] = 1;
    rec_stack[u] = 1;

    for (int v = 0; v < n; v++) {
        if (adj[u][v]) {
            if (!visited[v]) {
                parent[v] = u;
                if (dfs_waitfor(v, n, adj, visited, rec_stack, parent, cycle_start, cycle_end))
                    return 1;
            } else if (rec_stack[v]) {
                *cycle_start = v;
                *cycle_end = u;
                return 1;
            }
        }
    }

    rec_stack[u] = 0;
    return 0;
}

int rag_detect_cycle_waitfor(int n, const int alloc[MAX_P][MAX_R], const int req[MAX_P][MAX_R],
                             int cycle_nodes[], int *cycle_len)
{
    int adj[MAX_P][MAX_P];
    memset(adj, 0, sizeof(adj));

    /* Build Wait-For Graph:
     * If Pi requests Rk (req[i][k] > 0) and Pj holds Rk (alloc[j][k] > 0),
     * then Pi is waiting for Pj: Pi -> Pj
     */
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            for (int k = 0; k < MAX_R; k++) {
                if (req[i][k] > 0 && alloc[j][k] > 0) {
                    adj[i][j] = 1;
                    break;
                }
            }
        }
    }

    int visited[MAX_P] = {0};
    int rec_stack[MAX_P] = {0};
    int parent[MAX_P];
    for (int i = 0; i < n; i++) parent[i] = -1;

    int cycle_start = -1, cycle_end = -1;
    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            if (dfs_waitfor(i, n, adj, visited, rec_stack, parent, &cycle_start, &cycle_end)) {
                /* Reconstruct cycle path */
                int path[MAX_P];
                int count = 0;
                path[count++] = cycle_start;
                for (int cur = cycle_end; cur != cycle_start && cur != -1; cur = parent[cur]) {
                    path[count++] = cur;
                }
                /* Reverse into cycle_nodes */
                for (int idx = 0; idx < count; idx++) {
                    cycle_nodes[idx] = path[count - 1 - idx];
                }
                *cycle_len = count;
                return 1;
            }
        }
    }

    *cycle_len = 0;
    return 0;
}
