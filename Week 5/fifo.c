/*
 * fifo.c - First-In, First-Out (FIFO) Page Replacement Algorithm
 * Module Owner: Nireeksha
 * Integrated by: Aditi Nayak (Team Leader)
 */

#include "page_replacement.h"

void fifo_simulate(const int pages[], int n, int capacity, SimulationResult *result)
{
    int frames[MAX_FRAMES];
    int pointer = 0;
    int hits = 0;
    int faults = 0;

    /* Initialize result structure */
    strncpy(result->algorithm_name, "FIFO", sizeof(result->algorithm_name) - 1);
    result->algorithm_name[sizeof(result->algorithm_name) - 1] = '\0';
    result->total_references = n;
    result->step_count = n;

    /* Initialize all frame slots as empty (-1) */
    for (int i = 0; i < capacity; i++) {
        frames[i] = -1;
    }

    /* Process each page in the reference string */
    for (int i = 0; i < n; i++) {
        int page = pages[i];
        int hit = 0;

        /* Check if page is currently in one of the frames */
        for (int j = 0; j < capacity; j++) {
            if (frames[j] == page) {
                hit = 1;
                break;
            }
        }

        if (hit) {
            hits++;
        } else {
            faults++;
            /* Replace page at the current FIFO circular pointer */
            frames[pointer] = page;
            pointer = (pointer + 1) % capacity;
        }

        /* Record step details for visualization and reporting */
        result->steps[i].page = page;
        result->steps[i].capacity = capacity;
        result->steps[i].is_hit = hit;
        for (int j = 0; j < capacity; j++) {
            result->steps[i].frames[j] = frames[j];
        }
    }

    result->hits = hits;
    result->faults = faults;
    calculate_metrics(result);
}
