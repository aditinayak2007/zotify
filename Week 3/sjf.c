/*
 * sjf.c - Shortest Job First (SJF) Scheduling Algorithms
 * Written by: Nireeksha
 * Integrated by: Aditi Nayak
 *
 * Implements:
 * 1. Non-preemptive Shortest Job First
 * 2. Preemptive Shortest Job First (Shortest Remaining Time First - SRTF)
 */

#include "process.h"

/* Select shortest job among arrived, unfinished processes */
static int pick_sjf(Process p[], int n, int time) {
    int best = -1;
    for (int i = 0; i < n; i++) {
        if (p[i].rem <= 0 || p[i].at > time) continue;
        if (best == -1 || p[i].rem < p[best].rem ||
            (p[i].rem == p[best].rem && p[i].at < p[best].at) ||
            (p[i].rem == p[best].rem && p[i].at == p[best].at && p[i].pid < p[best].pid)) {
            best = i;
        }
    }
    return best;
}

static int next_sjf_arrival(Process p[], int n, int time) {
    int t = -1;
    for (int i = 0; i < n; i++) {
        if (p[i].rem > 0 && p[i].at > time && (t == -1 || p[i].at < t)) {
            t = p[i].at;
        }
    }
    return t;
}

/* 1. Non-preemptive SJF */
void schedule_sjf_nonpreemptive(Process p[], int n, Gantt *g) {
    process_reset(p, n);
    gantt_init(g);

    int time = 0, completed = 0;
    printf("\n[Non-preemptive SJF Execution Sequence]: ");

    while (completed < n) {
        int i = pick_sjf(p, n, time);
        if (i == -1) {
            /* CPU Idle until next arrival */
            int next_t = next_sjf_arrival(p, n, time);
            gantt_add(g, -1, time, next_t);
            time = next_t;
            continue;
        }

        p[i].start = time;
        printf("P%d ", p[i].pid);

        gantt_add(g, p[i].pid, time, time + p[i].bt);
        time += p[i].bt;
        p[i].rem = 0;
        process_finish(&p[i], time);
        completed++;
    }
    printf("\n");

    print_gantt(g);
    print_metrics(p, n, g, "Non-preemptive Shortest Job First (SJF)");
}

/* 2. Preemptive SJF (SRTF) */
void schedule_sjf_preemptive(Process p[], int n, Gantt *g) {
    process_reset(p, n);
    gantt_init(g);

    int time = 0, completed = 0;
    int last_pid = -2;

    printf("\n[Preemptive SJF (SRTF) Execution Sequence]: ");

    while (completed < n) {
        int i = pick_sjf(p, n, time);
        if (i == -1) {
            int next_t = next_sjf_arrival(p, n, time);
            gantt_add(g, -1, time, next_t);
            time = next_t;
            last_pid = -1;
            continue;
        }

        if (p[i].start == -1) {
            p[i].start = time;
        }

        if (p[i].pid != last_pid) {
            printf("P%d ", p[i].pid);
            last_pid = p[i].pid;
        }

        /* Execute for 1 time slice and re-evaluate for preemption */
        gantt_add(g, p[i].pid, time, time + 1);
        time++;
        p[i].rem--;

        if (p[i].rem == 0) {
            process_finish(&p[i], time);
            completed++;
        }
    }
    printf("\n");

    print_gantt(g);
    print_metrics(p, n, g, "Preemptive Shortest Job First (SRTF)");
}
