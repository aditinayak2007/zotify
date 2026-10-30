/*
 * metrics.c - Performance Metrics & Comparative Analysis Engine
 * Module Owner: Yaseem
 * Integrated by: Aditi Nayak (Team Leader)
 */

#include "page_replacement.h"

void calculate_metrics(SimulationResult *res)
{
    if (res->total_references > 0) {
        res->hit_ratio = ((double)res->hits / res->total_references) * 100.0;
        res->fault_ratio = ((double)res->faults / res->total_references) * 100.0;
    } else {
        res->hit_ratio = 0.0;
        res->fault_ratio = 0.0;
    }
}

void compare_all_algorithms(const int pages[], int n, int capacity, SimulationResult results[3])
{
    fifo_simulate(pages, n, capacity, &results[0]);
    lru_simulate(pages, n, capacity, &results[1]);
    optimal_simulate(pages, n, capacity, &results[2]);
}

int find_best_algorithm(const SimulationResult results[3])
{
    int best_idx = 0;
    int min_faults = results[0].faults;

    for (int i = 1; i < 3; i++) {
        if (results[i].faults < min_faults) {
            min_faults = results[i].faults;
            best_idx = i;
        }
    }
    return best_idx;
}

void print_simulation_table(const SimulationResult *res)
{
    if (res->step_count == 0) return;
    int capacity = res->steps[0].capacity;

    printf("\n========================================================================\n");
    printf("   ALGORITHM: %s PAGE REPLACEMENT SIMULATION\n", res->algorithm_name);
    printf("========================================================================\n");
    printf("%-6s | %-6s | Frame Contents %-18s | %-8s\n", "Step", "Page", "", "Result");
    printf("-------+--------+------------------------------------+----------\n");

    for (int i = 0; i < res->step_count; i++) {
        printf("%-6d | %-6d | [ ", i + 1, res->steps[i].page);
        for (int j = 0; j < capacity; j++) {
            if (res->steps[i].frames[j] == -1) {
                printf("- ");
            } else {
                printf("%d ", res->steps[i].frames[j]);
            }
        }
        printf("]");
        /* Padding */
        int printed_len = capacity * 2 + 3;
        for (int pad = printed_len; pad < 32; pad++) {
            printf(" ");
        }
        printf(" | %s\n", res->steps[i].is_hit ? "HIT " : "FAULT");
    }

    printf("========================================================================\n");
    printf(" PERFORMANCE EVALUATION SUMMARY (%s):\n", res->algorithm_name);
    printf("   * Total Page References : %d\n", res->total_references);
    printf("   * Total Page Hits       : %d\n", res->hits);
    printf("   * Total Page Faults     : %d\n", res->faults);
    printf("   * Page Hit Ratio        : %.2f%%\n", res->hit_ratio);
    printf("   * Page Fault Ratio      : %.2f%%\n", res->fault_ratio);
    printf("========================================================================\n");
}

void print_comparison_table(const SimulationResult results[3])
{
    int best_idx = find_best_algorithm(results);

    printf("\n================================================================================\n");
    printf("                PAGE REPLACEMENT ALGORITHMS COMPARATIVE ANALYSIS                \n");
    printf("================================================================================\n");
    printf("%-12s | %-12s | %-10s | %-11s | %-11s | %-11s\n",
           "Algorithm", "Total Refs", "Page Hits", "Page Faults", "Hit Ratio", "Fault Ratio");
    printf("-------------+--------------+------------+-------------+-------------+-------------\n");

    for (int i = 0; i < 3; i++) {
        printf("%-12s | %-12d | %-10d | %-11d | %9.2f%%  | %9.2f%%\n",
               results[i].algorithm_name,
               results[i].total_references,
               results[i].hits,
               results[i].faults,
               results[i].hit_ratio,
               results[i].fault_ratio);
    }
    printf("================================================================================\n");
    printf(" >>> BEST PERFORMING ALGORITHM: %s (Lowest Faults: %d, Fault Ratio: %.2f%%)\n",
           results[best_idx].algorithm_name,
           results[best_idx].faults,
           results[best_idx].fault_ratio);
    printf("================================================================================\n");
}
