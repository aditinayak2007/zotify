#ifndef PROCESS_H
#define PROCESS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PROCESSES 100
#define MAX_SEG 2000

/* Standardized Process Structure */
typedef struct {
    int pid;        /* Process ID */
    int at;         /* Arrival Time */
    int bt;         /* Burst Time */
    int priority;   /* Priority (Lower number = Higher priority) */
    int rem;        /* Remaining burst time */
    int start;      /* First time process acquired CPU (-1 if not started) */
    int ct;         /* Completion Time */
    int tat;        /* Turnaround Time = ct - at */
    int wt;         /* Waiting Time = tat - bt */
    int rt;         /* Response Time = start - at */
} Process;

/* Gantt Chart Segment: pid == -1 represents CPU IDLE */
typedef struct {
    int pid;
    int start;
    int end;
} Seg;

/* Gantt Chart Structure */
typedef struct {
    Seg seg[MAX_SEG];
    int n;
} Gantt;

/* Helper Functions */
void process_reset(Process p[], int n);
void process_finish(Process *p, int time);
void gantt_init(Gantt *g);
void gantt_add(Gantt *g, int pid, int start, int end);
void print_gantt(const Gantt *g);
void print_metrics(const Process p[], int n, const Gantt *g, const char *algo_name);

/* Input Handling Module (Anas) */
int get_process_input(Process p[], int *n);
void set_sample_processes(Process p[], int *n);

/* Scheduling Algorithms */
/* FCFS & Round Robin (Anas) */
void schedule_fcfs(Process p[], int n, Gantt *g);
void schedule_round_robin(Process p[], int n, int quantum, Gantt *g);

/* Shortest Job First Algorithms (Nireeksha) */
void schedule_sjf_nonpreemptive(Process p[], int n, Gantt *g);
void schedule_sjf_preemptive(Process p[], int n, Gantt *g);

/* Priority Scheduling Algorithms (Yaseem) */
void schedule_priority_nonpreemptive(Process p[], int n, Gantt *g);
void schedule_priority_preemptive(Process p[], int n, Gantt *g);

#endif /* PROCESS_H */
