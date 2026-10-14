/*
 * fcfs.c - First-Come, First-Served (FCFS) Scheduling Algorithm
 * Written by: Anas Ahmed
 * Integrated by: Aditi Nayak
 */

#include "process.h"

void schedule_fcfs(Process p[], int n, Gantt *g) {
    process_reset(p, n);
    gantt_init(g);

    int order[MAX_PROCESSES];
    for (int i = 0; i < n; i++) {
        order[i] = i;
    }

    /* Stable sort by arrival time; tie-break: lower PID */
    for (int i = 0; i < n - 1; i++) {
        for (int j = i + 1; j < n; j++) {
            if (p[order[i]].at > p[order[j]].at ||
               (p[order[i]].at == p[order[j]].at && p[order[i]].pid > p[order[j]].pid)) {
                int temp = order[i];
                order[i] = order[j];
                order[j] = temp;
            }
        }
    }

    int current_time = 0;

    printf("\n[FCFS Execution Sequence]: ");

    for (int i = 0; i < n; i++) {
        int idx = order[i];

        /* If CPU is idle before process arrives */
        if (current_time < p[idx].at) {
            gantt_add(g, -1, current_time, p[idx].at);
            current_time = p[idx].at;
        }

        p[idx].start = current_time;
        printf("P%d ", p[idx].pid);

        int end_time = current_time + p[idx].bt;
        gantt_add(g, p[idx].pid, current_time, end_time);

        current_time = end_time;
        p[idx].rem = 0;
        process_finish(&p[idx], current_time);
    }
    printf("\n");

    print_gantt(g);
    print_metrics(p, n, g, "First-Come First-Served (FCFS)");
}
