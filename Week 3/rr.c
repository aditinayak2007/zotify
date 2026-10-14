/*
 * rr.c - Round Robin (RR) Scheduling Algorithm
 * Written by: Anas Ahmed
 * Integrated by: Aditi Nayak
 */

#include "process.h"

void schedule_round_robin(Process p[], int n, int quantum, Gantt *g) {
    if (quantum <= 0) {
        printf("Error: Time quantum must be a positive integer (> 0).\n");
        return;
    }

    process_reset(p, n);
    gantt_init(g);

    int queue[100000];
    int front = 0, rear = 0;
    int added[MAX_PROCESSES] = {0};
    int time = 0, completed = 0;

    printf("\n[Round Robin (Quantum = %d) Execution Sequence]: ", quantum);

    while (completed < n) {
        /* Enqueue all newly arrived processes in order of arrival time */
        while (1) {
            int next = -1;
            for (int i = 0; i < n; i++) {
                if (!added[i] && p[i].at <= time) {
                    if (next == -1 || p[i].at < p[next].at ||
                       (p[i].at == p[next].at && p[i].pid < p[next].pid)) {
                        next = i;
                    }
                }
            }
            if (next == -1) break;
            queue[rear++] = next;
            added[next] = 1;
        }

        /* If queue is empty, advance time to next process arrival (CPU Idle) */
        if (front == rear) {
            int next_time = -1;
            for (int i = 0; i < n; i++) {
                if (!added[i] && (next_time == -1 || p[i].at < next_time)) {
                    next_time = p[i].at;
                }
            }
            if (next_time != -1) {
                gantt_add(g, -1, time, next_time);
                time = next_time;
            }
            continue;
        }

        int i = queue[front++];
        if (p[i].start == -1) {
            p[i].start = time;
        }

        int run_time = (p[i].rem < quantum) ? p[i].rem : quantum;
        printf("P%d ", p[i].pid);

        gantt_add(g, p[i].pid, time, time + run_time);
        time += run_time;
        p[i].rem -= run_time;

        /* Add processes that arrived during this execution slice */
        while (1) {
            int next = -1;
            for (int j = 0; j < n; j++) {
                if (!added[j] && p[j].at <= time) {
                    if (next == -1 || p[j].at < p[next].at ||
                       (p[j].at == p[next].at && p[j].pid < p[next].pid)) {
                        next = j;
                    }
                }
            }
            if (next == -1) break;
            queue[rear++] = next;
            added[next] = 1;
        }

        /* If process still has remaining burst time, return it to end of queue */
        if (p[i].rem > 0) {
            queue[rear++] = i;
        } else {
            process_finish(&p[i], time);
            completed++;
        }
    }
    printf("\n");

    print_gantt(g);
    print_metrics(p, n, g, "Round Robin (RR)");
}
