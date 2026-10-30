/*
 * lru.c - Least Recently Used (LRU) Page Replacement Algorithm
 * Module Owner: Nireeksha
 * Integrated by: Aditi Nayak (Team Leader)
 */

#include "page_replacement.h"

void lru_simulate(const int pages[], int n, int capacity, SimulationResult *result)
{
    int frames[MAX_FRAMES];
    int last_used[MAX_FRAMES];
    int hits = 0;
    int faults = 0;

    /* Initialize result structure */
    strncpy(result->algorithm_name, "LRU", sizeof(result->algorithm_name) - 1);
    result->algorithm_name[sizeof(result->algorithm_name) - 1] = '\0';
    result->total_references = n;
    result->step_count = n;

    /* Initialize frames and usage trackers */
    for (int i = 0; i < capacity; i++) {
        frames[i] = -1;
        last_used[i] = -1;
    }

    /* Process each page in the reference string */
    for (int i = 0; i < n; i++) {
        int page = pages[i];
        int hit = 0;
        int hit_pos = -1;

        /* Check if page already exists in frames */
        for (int j = 0; j < capacity; j++) {
            if (frames[j] == page) {
                hit = 1;
                hit_pos = j;
                break;
            }
        }

        if (hit) {
            hits++;
            last_used[hit_pos] = i; /* Update timestamp of last access */
        } else {
            faults++;
            int replace_idx = -1;

            /* Check if there is an empty frame available first */
            for (int j = 0; j < capacity; j++) {
                if (frames[j] == -1) {
                    replace_idx = j;
                    break;
                }
            }

            /* If all frames are occupied, evict the least recently used frame */
            if (replace_idx == -1) {
                replace_idx = 0;
                for (int j = 1; j < capacity; j++) {
                    if (last_used[j] < last_used[replace_idx]) {
                        replace_idx = j;
                    }
                }
            }

            frames[replace_idx] = page;
            last_used[replace_idx] = i;
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
