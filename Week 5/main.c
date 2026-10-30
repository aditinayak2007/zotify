/*
 * main.c - Interactive Page Replacement Simulator (C CLI Runner)
 * Operating Systems Project-Based Learning (Week 5)
 *
 * Integrated by: Aditi Nayak (Team Leader)
 * Team Members: Aditi Nayak, Anas Ahmed, Nireeksha, Yaseem
 */

#include "page_replacement.h"

static void load_default_benchmark(int pages[], int *n, int *capacity)
{
    /* Benchmark from project specification */
    int def_pages[] = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3};
    *n = 10;
    *capacity = 3;
    for (int i = 0; i < *n; i++) {
        pages[i] = def_pages[i];
    }
    printf("\n>>> [LOADED]: Course Specification Benchmark: 7 0 1 2 0 3 0 4 2 3 (Frames: 3)\n");
}

static void print_current_config(const int pages[], int n, int capacity)
{
    printf("\n--- CURRENT CONFIGURATION ---\n");
    printf("Reference String (%d pages): ", n);
    for (int i = 0; i < n; i++) {
        printf("%d ", pages[i]);
    }
    printf("\nAvailable Frame Capacity   : %d\n", capacity);
    printf("-------------------------------\n");
}

int main(void)
{
    int pages[MAX_PAGES];
    int n = 0;
    int capacity = 3;
    int choice;

    load_default_benchmark(pages, &n, &capacity);

    for (;;) {
        printf("\n========================================================\n");
        printf("    PAGE REPLACEMENT ALGORITHMS SIMULATOR (WEEK 5)      \n");
        printf("    OS PBL Team Leader: Aditi Nayak                     \n");
        printf("========================================================\n");
        printf(" 1) Run FIFO (First-In, First-Out)\n");
        printf(" 2) Run LRU (Least Recently Used)\n");
        printf(" 3) Run Optimal (OPT / MIN)\n");
        printf(" 4) Compare All Algorithms (FIFO vs LRU vs Optimal)\n");
        printf(" 5) Load Course Benchmark (7 0 1 2 0 3 0 4 2 3, 3 Frames)\n");
        printf(" 6) Enter Custom Page References & Frame Count\n");
        printf(" 7) View Current Configuration\n");
        printf(" 8) Exit\n");
        printf("--------------------------------------------------------\n");
        printf("Select option (1-8): ");

        if (scanf("%d", &choice) != 1) {
            scanf("%*[^\n]");
            continue;
        }

        switch (choice) {
            case 1: {
                SimulationResult res;
                fifo_simulate(pages, n, capacity, &res);
                print_simulation_table(&res);
                break;
            }

            case 2: {
                SimulationResult res;
                lru_simulate(pages, n, capacity, &res);
                print_simulation_table(&res);
                break;
            }

            case 3: {
                SimulationResult res;
                optimal_simulate(pages, n, capacity, &res);
                print_simulation_table(&res);
                break;
            }

            case 4: {
                SimulationResult results[3];
                compare_all_algorithms(pages, n, capacity, results);
                for (int i = 0; i < 3; i++) {
                    print_simulation_table(&results[i]);
                }
                print_comparison_table(results);
                break;
            }

            case 5:
                load_default_benchmark(pages, &n, &capacity);
                break;

            case 6: {
                int input_n, input_cap;
                printf("\nEnter number of page references (1-%d): ", MAX_PAGES);
                if (scanf("%d", &input_n) != 1 || input_n <= 0 || input_n > MAX_PAGES) {
                    printf("Error: Invalid number of pages.\n");
                    scanf("%*[^\n]");
                    break;
                }

                printf("Enter %d page numbers (non-negative integers):\n", input_n);
                int valid = 1;
                for (int i = 0; i < input_n; i++) {
                    if (scanf("%d", &pages[i]) != 1 || pages[i] < 0) {
                        valid = 0;
                        break;
                    }
                }

                if (!valid) {
                    printf("Error: Invalid page numbers encountered.\n");
                    scanf("%*[^\n]");
                    break;
                }

                printf("Enter number of frames (1-%d): ", MAX_FRAMES);
                if (scanf("%d", &input_cap) != 1 || input_cap <= 0 || input_cap > MAX_FRAMES) {
                    printf("Error: Frame count must be at least 1.\n");
                    scanf("%*[^\n]");
                    break;
                }

                n = input_n;
                capacity = input_cap;
                printf("Configuration updated successfully!\n");
                break;
            }

            case 7:
                print_current_config(pages, n, capacity);
                break;

            case 8:
                printf("\nExiting Page Replacement Simulator. Thank you!\n");
                return 0;

            default:
                printf("Invalid selection. Please choose an option from 1 to 8.\n");
                break;
        }
    }

    return 0;
}
