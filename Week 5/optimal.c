/*
 * optimal.c - Optimal (OPT / MIN) Page Replacement Algorithm
 * Module Owner: Yaseem
 * Integrated by: Aditi Nayak (Team Leader)
 */

#include "page_replacement.h"
#include <limits.h>

void optimal_simulate(const int pages[], int n, int capacity, SimulationResult *result)
{
    int frames[MAX_FRAMES];
    int hits = 0;
    int faults = 0;

    /* Initialize result structure */
    strncpy(result->algorithm_name, "Optimal", sizeof(result->algorithm_name) - 1);
    result->algorithm_name[sizeof(result->algorithm_name) - 1] = '\0';
    result->total_references = n;
    result->step_count = n;

    /* Initialize frames as empty */
    for (int i = 0; i < capacity; i++) {
        frames[i] = -1;
    }

    /* Process each page in the reference string */
    for (int i = 0; i < n; i++) {
        int page = pages[i];
        int hit = 0;

        /* Check if page already exists in frames */
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
            int replace_idx = -1;

            /* Check for an empty frame first */
            for (int j = 0; j < capacity; j++) {
                if (frames[j] == -1) {
                    replace_idx = j;
                    break;
                }
            }

            /* If all frames are occupied, look forward into the future */
            if (replace_idx == -1) {
                int farthest_use = -1;

                for (int j = 0; j < capacity; j++) {
                    int next_use = INT_MAX; /* Assume not used in future */

                    for (int k = i + 1; k < n; k++) {
                        if (pages[k] == frames[j]) {
                            next_use = k;
                            break;
                        }
                    }

                    /* If page is never used again, it is an optimal victim */
                    if (next_use == INT_MAX) {
                        replace_idx = j;
                        break; /* First page never used in future selected */
                    }

                    /* Otherwise find the page needed farthest in the future */
                    if (next_use > farthest_use) {
                        farthest_use = next_use;
                        replace_idx = j;
                    }
                }
            }

            frames[replace_idx] = page;
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
