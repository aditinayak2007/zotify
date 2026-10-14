/*
 * gantt.c - Gantt Chart Rendering and Performance Metrics Engine
 * Written by: Nireeksha (Gantt Chart) & Yaseem (Performance Metrics)
 * Integrated by: Aditi Nayak
 */

#include "process.h"

void process_reset(Process p[], int n) {
    for (int i = 0; i < n; i++) {
        p[i].rem = p[i].bt;
        p[i].start = -1;
        p[i].ct = 0;
        p[i].tat = 0;
        p[i].wt = 0;
        p[i].rt = 0;
    }
}

void process_finish(Process *p, int time) {
    p->ct = time;
    p->tat = p->ct - p->at;
    p->wt = p->tat - p->bt;
    p->rt = p->start - p->at;
}

void gantt_init(Gantt *g) {
    g->n = 0;
}

void gantt_add(Gantt *g, int pid, int start, int end) {
    if (start >= end) return;
    
    /* Merge adjacent blocks of the same process / idle */
    if (g->n > 0 && g->seg[g->n - 1].pid == pid && g->seg[g->n - 1].end == start) {
        g->seg[g->n - 1].end = end;
        return;
    }

    if (g->n < MAX_SEG) {
        g->seg[g->n].pid = pid;
        g->seg[g->n].start = start;
        g->seg[g->n].end = end;
        g->n++;
    }
}

void print_gantt(const Gantt *g) {
    if (g->n == 0) {
        printf("\n[Gantt Chart] Empty timeline (no execution recorded).\n");
        return;
    }

    printf("\n================================ GANTT CHART ================================\n");

    /* Top border */
    for (int i = 0; i < g->n; i++) {
        int duration = g->seg[i].end - g->seg[i].start;
        int width = duration * 2;
        if (width < 6) width = 6;
        if (width > 14) width = 14;

        putchar('+');
        for (int k = 0; k < width; k++) putchar('-');
    }
    puts("+");

    /* Process Labels */
    for (int i = 0; i < g->n; i++) {
        int duration = g->seg[i].end - g->seg[i].start;
        int width = duration * 2;
        if (width < 6) width = 6;
        if (width > 14) width = 14;

        char label[16];
        if (g->seg[i].pid == -1) {
            snprintf(label, sizeof(label), "IDLE");
        } else {
            snprintf(label, sizeof(label), "P%d", g->seg[i].pid);
        }

        int len = (int)strlen(label);
        int left = (width - len) / 2;
        int right = width - len - left;

        putchar('|');
        printf("%*s%s%*s", left, "", label, right, "");
    }
    puts("|");

    /* Bottom border */
    for (int i = 0; i < g->n; i++) {
        int duration = g->seg[i].end - g->seg[i].start;
        int width = duration * 2;
        if (width < 6) width = 6;
        if (width > 14) width = 14;

        putchar('+');
        for (int k = 0; k < width; k++) putchar('-');
    }
    puts("+");

    /* Time markers */
    for (int i = 0; i < g->n; i++) {
        int duration = g->seg[i].end - g->seg[i].start;
        int width = duration * 2;
        if (width < 6) width = 6;
        if (width > 14) width = 14;

        printf("%-*d", width + 1, g->seg[i].start);
    }
    printf("%d\n", g->seg[g->n - 1].end);
    printf("=============================================================================\n");
}

void print_metrics(const Process p[], int n, const Gantt *g, const char *algo_name) {
    float total_wt = 0, total_tat = 0, total_rt = 0;
    int total_idle = 0;
    int total_time = g->n > 0 ? g->seg[g->n - 1].end : 0;

    for (int i = 0; i < g->n; i++) {
        if (g->seg[i].pid == -1) {
            total_idle += (g->seg[i].end - g->seg[i].start);
        }
    }

    int busy_time = total_time - total_idle;
    float cpu_utilization = total_time > 0 ? ((float)busy_time / total_time) * 100.0f : 0.0f;
    float throughput = total_time > 0 ? ((float)n / total_time) : 0.0f;

    printf("\n-----------------------------------------------------------------------------\n");
    printf(" PERFORMANCE EVALUATION: %s\n", algo_name);
    printf("-----------------------------------------------------------------------------\n");
    printf("%-6s %-10s %-10s %-10s %-6s %-6s %-6s %-6s\n",
           "PID", "Arrival", "Burst", "Priority", "CT", "TAT", "WT", "RT");
    printf("-----------------------------------------------------------------------------\n");

    for (int i = 0; i < n; i++) {
        printf("P%-5d %-10d %-10d %-10d %-6d %-6d %-6d %-6d\n",
               p[i].pid, p[i].at, p[i].bt, p[i].priority,
               p[i].ct, p[i].tat, p[i].wt, p[i].rt);

        total_wt += p[i].wt;
        total_tat += p[i].tat;
        total_rt += p[i].rt;
    }

    printf("-----------------------------------------------------------------------------\n");
    printf(" Statistical Summary:\n");
    printf("   - Average Waiting Time (WT):      %.2f time units\n", total_wt / n);
    printf("   - Average Turnaround Time (TAT):  %.2f time units\n", total_tat / n);
    printf("   - Average Response Time (RT):     %.2f time units\n", total_rt / n);
    printf("   - Total Simulation Time:          %d time units\n", total_time);
    printf("   - Total CPU Idle Time:            %d time units\n", total_idle);
    printf("   - CPU Utilization:                %.2f%%\n", cpu_utilization);
    printf("   - Throughput:                     %.4f processes/unit time\n", throughput);
    printf("-----------------------------------------------------------------------------\n");
}
