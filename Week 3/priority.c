/*
 * priority.c - Priority Scheduling Algorithms
 * Written by: Yaseem
 * Integrated by: Aditi Nayak
 *
 * Implements:
 * 1. Non-preemptive Priority Scheduling
 * 2. Preemptive Priority Scheduling
 * Priority Convention: Lower numerical value = Higher priority (1 is highest).
 */

#include "process.h"

/* Select highest priority job among arrived, unfinished processes */
static int pick_priority(Process p[], int n, int time) {
    int best = -1;
    for (int i = 0; i < n; i++) {
        if (p[i].rem <= 0 || p[i].at > time) continue;
        if (best == -1 || p[i].priority < p[best].priority ||
            (p[i].priority == p[best].priority && p[i].at < p[best].at) ||
            (p[i].priority == p[best].priority && p[i].at == p[best].at && p[i].pid < p[best].pid)) {
            best = i;
        }
    }
    return best;
}

static int next_priority_arrival(Process p[], int n, int time) {
    int t = -1;
    for (int i = 0; i < n; i++) {
        if (p[i].rem > 0 && p[i].at > time && (t == -1 || p[i].at < t)) {
            t = p[i].at;
        }
    }
    return t;
}

/* 1. Non-preemptive Priority Scheduling */
void schedule_priority_nonpreemptive(Process p[], int n, Gantt *g) {
    process_reset(p, n);
    gantt_init(g);

    int time = 0, completed = 0;
    printf("\n[Non-preemptive Priority Execution Sequence]: ");

    while (completed < n) {
        int i = pick_priority(p, n, time);
        if (i == -1) {
            /* CPU Idle */
            int next_t = next_priority_arrival(p, n, time);
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
    print_metrics(p, n, g, "Non-preemptive Priority Scheduling");
}

/* 2. Preemptive Priority Scheduling */
void schedule_priority_preemptive(Process p[], int n, Gantt *g) {
    process_reset(p, n);
    gantt_init(g);

    int time = 0, completed = 0;
    int last_pid = -2;

    printf("\n[Preemptive Priority Execution Sequence]: ");

    while (completed < n) {
        int i = pick_priority(p, n, time);
        if (i == -1) {
            int next_t = next_priority_arrival(p, n, time);
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

        /* Run 1 unit of time and re-evaluate */
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
    print_metrics(p, n, g, "Preemptive Priority Scheduling");
}
