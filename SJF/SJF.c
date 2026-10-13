/*
 * sjf.c - Non-preemptive SJF, Preemptive SJF (SRTF) and Gantt chart.
 * Integration: call sjf_nonpreemptive() / sjf_preemptive() with an array
 * of Process, then print_gantt(). Compile the self-test with:
 *     gcc -Wall -Wextra -DSJF_TEST sjf.c -o sjf_test && ./sjf_test
 */
#include <stdio.h>
#include <string.h>

#define MAX_SEG 1000

typedef struct {
    int pid;    /* process id                         */
    int at;     /* arrival time                       */
    int bt;     /* burst time                         */
    int rem;    /* remaining time (working field)     */
    int start;  /* first time it got the CPU (-1)     */
    int ct;     /* completion time                    */
    int tat;    /* turnaround = ct - at               */
    int wt;     /* waiting    = tat - bt              */
    int rt;     /* response   = start - at            */
} Process;

typedef struct { int pid; int start; int end; } Seg;   /* pid == -1 -> idle */
typedef struct { Seg seg[MAX_SEG]; int n; } Gantt;

/* ---------- helpers ---------- */

static void reset(Process p[], int n) {
    for (int i = 0; i < n; i++) {
        p[i].rem = p[i].bt;
        p[i].start = -1;
        p[i].ct = p[i].tat = p[i].wt = p[i].rt = 0;
    }
}

/* Add [s,e) to the chart, merging with the previous block if same pid. */
static void gantt_add(Gantt *g, int pid, int s, int e) {
    if (s >= e) return;
    if (g->n > 0 && g->seg[g->n - 1].pid == pid && g->seg[g->n - 1].end == s) {
        g->seg[g->n - 1].end = e;
        return;
    }
    if (g->n < MAX_SEG) g->seg[g->n++] = (Seg){pid, s, e};
}

static void finish(Process *p, int time) {
    p->ct  = time;
    p->tat = p->ct - p->at;
    p->wt  = p->tat - p->bt;
    p->rt  = p->start - p->at;
}

/* Shortest remaining job among arrived, unfinished ones.
 * Tie-break: earlier arrival, then lower index. Returns -1 if none. */
static int pick(Process p[], int n, int time) {
    int best = -1;
    for (int i = 0; i < n; i++) {
        if (p[i].rem <= 0 || p[i].at > time) continue;
        if (best == -1 || p[i].rem < p[best].rem ||
            (p[i].rem == p[best].rem && p[i].at < p[best].at))
            best = i;
    }
    return best;
}

static int next_arrival(Process p[], int n, int time) {
    int t = -1;
    for (int i = 0; i < n; i++)
        if (p[i].rem > 0 && p[i].at > time && (t == -1 || p[i].at < t))
            t = p[i].at;
    return t;
}

/* ---------- Non-preemptive SJF ---------- */

void sjf_nonpreemptive(Process p[], int n, Gantt *g) {
    reset(p, n);
    g->n = 0;
    int time = 0, done = 0;
    while (done < n) {
        int i = pick(p, n, time);
        if (i == -1) {                       /* CPU idle until next arrival */
            int t = next_arrival(p, n, time);
            gantt_add(g, -1, time, t);
            time = t;
            continue;
        }
        p[i].start = time;
        gantt_add(g, p[i].pid, time, time + p[i].bt);
        time += p[i].bt;
        p[i].rem = 0;
        finish(&p[i], time);
        done++;
    }
}

/* ---------- Preemptive SJF (SRTF) ---------- */

void sjf_preemptive(Process p[], int n, Gantt *g) {
    reset(p, n);
    g->n = 0;
    int time = 0, done = 0;
    while (done < n) {
        int i = pick(p, n, time);
        if (i == -1) {
            int t = next_arrival(p, n, time);
            gantt_add(g, -1, time, t);
            time = t;
            continue;
        }
        if (p[i].start == -1) p[i].start = time;
        gantt_add(g, p[i].pid, time, time + 1);   /* run 1 unit, re-decide */
        time++;
        if (--p[i].rem == 0) { finish(&p[i], time); done++; }
    }
}

/* ---------- Gantt chart output ---------- */

void print_gantt(const Gantt *g) {
    printf("\nGantt Chart:\n");
    for (int i = 0; i < g->n; i++) {            /* top border */
        int w = (g->seg[i].end - g->seg[i].start) * 2; if (w < 5) w = 5;
        putchar('+'); for (int k = 0; k < w; k++) putchar('-');
    }
    puts("+");
    for (int i = 0; i < g->n; i++) {            /* process labels */
        int w = (g->seg[i].end - g->seg[i].start) * 2; if (w < 5) w = 5;
        char lbl[16];
        if (g->seg[i].pid == -1) strcpy(lbl, "IDLE");
        else snprintf(lbl, sizeof lbl, "P%d", g->seg[i].pid);
        int len = (int)strlen(lbl), left = (w - len) / 2;
        putchar('|');
        printf("%*s%s%*s", left, "", lbl, w - len - left, "");
    }
    puts("|");
    for (int i = 0; i < g->n; i++) {            /* bottom border */
        int w = (g->seg[i].end - g->seg[i].start) * 2; if (w < 5) w = 5;
        putchar('+'); for (int k = 0; k < w; k++) putchar('-');
    }
    puts("+");
    for (int i = 0; i < g->n; i++) {            /* time stamps */
        int w = (g->seg[i].end - g->seg[i].start) * 2; if (w < 5) w = 5;
        printf("%-*d", w + 1, g->seg[i].start);
    }
    printf("%d\n", g->n ? g->seg[g->n - 1].end : 0);
}

void print_table(const Process p[], int n) {
    double sw = 0, st = 0, sr = 0;
    printf("PID  AT  BT  CT  TAT  WT  RT\n");
    for (int i = 0; i < n; i++) {
        printf("P%-3d %3d %3d %3d %4d %3d %3d\n", p[i].pid, p[i].at, p[i].bt,
               p[i].ct, p[i].tat, p[i].wt, p[i].rt);
        sw += p[i].wt; st += p[i].tat; sr += p[i].rt;
    }
    printf("Avg WT=%.2f  Avg TAT=%.2f  Avg RT=%.2f\n", sw / n, st / n, sr / n);
}

/* ---------- Self-test ---------- */
#ifdef SJF_TEST
#include <assert.h>
#include <math.h>
#define P(id,a,b) {.pid=(id),.at=(a),.bt=(b)}

static double avg_wt(Process p[], int n) {
    double s = 0; for (int i = 0; i < n; i++) s += p[i].wt; return s / n;
}

static void run(const char *title, Process p[], int n,
                void (*algo)(Process[], int, Gantt *)) {
    Gantt g;
    printf("\n=== %s ===\n", title);
    algo(p, n, &g);
    print_table(p, n);
    print_gantt(&g);
}

int main(void) {
    /* Test 1: classic set, both algorithms */
    Process a[] = {P(1,0,7),P(2,2,4),P(3,4,1),P(4,5,4)};
    run("Test 1 - Non-preemptive SJF", a, 4, sjf_nonpreemptive);
    assert(fabs(avg_wt(a, 4) - 4.0) < 1e-9);
    assert(a[2].ct == 8 && a[1].ct == 12 && a[3].ct == 16);

    run("Test 1 - Preemptive SJF (SRTF)", a, 4, sjf_preemptive);
    assert(fabs(avg_wt(a, 4) - 3.0) < 1e-9);
    assert(a[2].ct == 5 && a[1].ct == 7 && a[3].ct == 11 && a[0].ct == 16);

    /* Test 2: CPU idle at start and in the middle */
    Process b[] = {P(1,2,3),P(2,10,2)};
    run("Test 2 - Idle gaps (non-preemptive)", b, 2, sjf_nonpreemptive);
    assert(b[0].ct == 5 && b[1].ct == 12);
    run("Test 2 - Idle gaps (preemptive)", b, 2, sjf_preemptive);
    assert(b[0].ct == 5 && b[1].ct == 12);

    /* Test 3: equal burst times -> FCFS tie-break; unsorted input */
    Process c[] = {P(3,1,4),P(1,0,4),P(2,0,4)};
    run("Test 3 - Tie-break (non-preemptive)", c, 3, sjf_nonpreemptive);
    assert(c[1].ct == 4 && c[2].ct == 8 && c[0].ct == 12);

    /* Test 4: single process */
    Process d[] = {P(1,0,5)};
    run("Test 4 - Single process (preemptive)", d, 1, sjf_preemptive);
    assert(d[0].wt == 0 && d[0].ct == 5);

    puts("\nAll tests passed.");
    return 0;
}
#endif
