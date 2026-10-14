/*
 * main.c - Process Scheduling Simulator: Main Menu & Integration
 * Written by: Aditi Nayak (Team Leader - Integration & Coordination)
 *
 * Responsibilities:
 * 1. Present unified menu for all 6 CPU scheduling algorithms:
 *    - 1. FCFS (Anas)
 *    - 2. Non-preemptive SJF (Nireeksha)
 *    - 3. Preemptive SJF (Nireeksha)
 *    - 4. Non-preemptive Priority (Yaseem)
 *    - 5. Preemptive Priority (Yaseem)
 *    - 6. Round Robin (Anas)
 *    - 7. Exit
 * 2. Manage process data state (allows testing algorithms on the SAME dataset for comparison).
 * 3. Support custom user input as well as quick sample dataset loading.
 * 4. Coordinate Gantt chart rendering and comprehensive metric calculations.
 */

#include "process.h"

static void print_banner(void) {
    printf("\n=============================================================================\n");
    printf("                  PROCESS SCHEDULING SIMULATOR (WEEK 3 PBL)                  \n");
    printf("   Team: Anas (FCFS/RR/Input) | Nireeksha (SJF/Gantt) | Yaseem (Priority)   \n");
    printf("   System Integration & Main Coordination: Aditi Nayak (Team Leader)        \n");
    printf("=============================================================================\n");
}

static void print_menu(void) {
    printf("\n===== PROCESS SCHEDULING SIMULATOR =====\n");
    printf("1. FCFS\n");
    printf("2. Non-preemptive SJF\n");
    printf("3. Preemptive SJF\n");
    printf("4. Non-preemptive Priority\n");
    printf("5. Preemptive Priority\n");
    printf("6. Round Robin\n");
    printf("7. Exit\n");
    printf("========================================\n");
    printf("Enter your choice: ");
}

int main(void) {
    Process base_processes[MAX_PROCESSES];
    Process current_run[MAX_PROCESSES];
    Gantt gantt;
    int num_processes = 0;
    int choice;

    print_banner();

    /* Initial dataset configuration */
    printf("\nProcess Dataset Selection:\n");
    printf("  1. Enter custom processes manually\n");
    printf("  2. Load standard test dataset (4 processes)\n");
    printf("Select option (1 or 2): ");

    int ds_choice;
    if (scanf("%d", &ds_choice) != 1) {
        printf("Invalid input. Loading standard test dataset by default.\n");
        set_sample_processes(base_processes, &num_processes);
    } else if (ds_choice == 1) {
        if (get_process_input(base_processes, &num_processes) != 0) {
            printf("Error reading input. Loading standard dataset instead.\n");
            set_sample_processes(base_processes, &num_processes);
        }
    } else {
        set_sample_processes(base_processes, &num_processes);
    }

    while (1) {
        print_menu();

        if (scanf("%d", &choice) != 1) {
            printf("\nInvalid input. Please enter a number between 1 and 7.\n");
            while (getchar() != '\n'); /* Flush buffer */
            continue;
        }

        if (choice == 7) {
            printf("\nExiting Process Scheduling Simulator. Thank you!\n");
            break;
        }

        /* Clone base processes into working array for this simulation run */
        for (int i = 0; i < num_processes; i++) {
            current_run[i] = base_processes[i];
        }

        switch (choice) {
            case 1:
                schedule_fcfs(current_run, num_processes, &gantt);
                break;

            case 2:
                schedule_sjf_nonpreemptive(current_run, num_processes, &gantt);
                break;

            case 3:
                schedule_sjf_preemptive(current_run, num_processes, &gantt);
                break;

            case 4:
                schedule_priority_nonpreemptive(current_run, num_processes, &gantt);
                break;

            case 5:
                schedule_priority_preemptive(current_run, num_processes, &gantt);
                break;

            case 6: {
                int quantum;
                printf("\nEnter Round Robin time quantum (integer > 0): ");
                while (scanf("%d", &quantum) != 1 || quantum <= 0) {
                    printf("Error: Quantum must be a positive integer (> 0). Re-enter: ");
                    while (getchar() != '\n');
                }
                schedule_round_robin(current_run, num_processes, quantum, &gantt);
                break;
            }

            default:
                printf("\nError: Unknown option %d. Please select an option from 1 to 7.\n", choice);
                break;
        }

        /* Option to modify/re-enter dataset */
        printf("\nDo you want to re-enter process data for next run? (1 = Yes, 0 = Keep current): ");
        int change_ds;
        if (scanf("%d", &change_ds) == 1 && change_ds == 1) {
            get_process_input(base_processes, &num_processes);
        }
    }

    return 0;
}
