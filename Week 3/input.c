/*
 * input.c - Process Input and Validation Module
 * Written by: Anas Ahmed
 * Integrated by: Aditi Nayak
 */

#include "process.h"

int get_process_input(Process p[], int *n) {
    int count;

    printf("\nEnter number of processes (1-%d): ", MAX_PROCESSES);
    if (scanf("%d", &count) != 1 || count < 1 || count > MAX_PROCESSES) {
        printf("Error: Invalid number of processes. Must be between 1 and %d.\n", MAX_PROCESSES);
        while (getchar() != '\n'); /* Flush input buffer */
        return -1;
    }

    printf("\nEnter process details (PID, Arrival Time, Burst Time, Priority):\n");
    printf("[Note: Priority is positive integer; 1 = Highest Priority]\n\n");

    for (int i = 0; i < count; i++) {
        printf("Process %d:\n", i + 1);

        printf("  Enter Process ID (PID): ");
        if (scanf("%d", &p[i].pid) != 1 || p[i].pid < 0) {
            printf("Error: Invalid PID. Must be non-negative integer.\n");
            while (getchar() != '\n');
            return -1;
        }

        /* Check for duplicate PID */
        for (int j = 0; j < i; j++) {
            if (p[j].pid == p[i].pid) {
                printf("Error: Duplicate PID %d detected. Each process must have a unique PID.\n", p[i].pid);
                while (getchar() != '\n');
                return -1;
            }
        }

        printf("  Enter Arrival Time (AT): ");
        if (scanf("%d", &p[i].at) != 1 || p[i].at < 0) {
            printf("Error: Arrival time cannot be negative.\n");
            while (getchar() != '\n');
            return -1;
        }

        printf("  Enter Burst Time (BT): ");
        if (scanf("%d", &p[i].bt) != 1 || p[i].bt <= 0) {
            printf("Error: Burst time must be positive (> 0).\n");
            while (getchar() != '\n');
            return -1;
        }

        printf("  Enter Priority (e.g., 1=Highest): ");
        if (scanf("%d", &p[i].priority) != 1 || p[i].priority < 0) {
            printf("Error: Priority must be non-negative integer.\n");
            while (getchar() != '\n');
            return -1;
        }

        p[i].rem = p[i].bt;
        p[i].start = -1;
        p[i].ct = 0;
        p[i].tat = 0;
        p[i].wt = 0;
        p[i].rt = 0;
        printf("\n");
    }

    *n = count;
    return 0;
}

void set_sample_processes(Process p[], int *n) {
    /* Standard textbook sample set from project specification */
    *n = 4;
    p[0] = (Process){.pid = 1, .at = 0, .bt = 5, .priority = 2, .rem = 5, .start = -1};
    p[1] = (Process){.pid = 2, .at = 1, .bt = 3, .priority = 1, .rem = 3, .start = -1};
    p[2] = (Process){.pid = 3, .at = 2, .bt = 1, .priority = 3, .rem = 1, .start = -1};
    p[3] = (Process){.pid = 4, .at = 3, .bt = 2, .priority = 4, .rem = 2, .start = -1};

    printf("\n[Default Test Dataset Loaded]:\n");
    printf("  P1: Arrival=0, Burst=5, Priority=2\n");
    printf("  P2: Arrival=1, Burst=3, Priority=1\n");
    printf("  P3: Arrival=2, Burst=1, Priority=3\n");
    printf("  P4: Arrival=3, Burst=2, Priority=4\n");
}
