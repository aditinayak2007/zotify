#include <stdio.h>

#define MAX 100

/* ---------------- FIFO ---------------- */

void fifo(int pages[], int n, int framesCount)
{
    int frames[MAX];
    int pointer = 0;
    int hits = 0, faults = 0;

    for (int i = 0; i < framesCount; i++)
        frames[i] = -1;

    printf("\n========== FIFO ==========\n");

    for (int i = 0; i < n; i++)
    {
        int hit = 0;

        /* Check if page is already present */
        for (int j = 0; j < framesCount; j++)
        {
            if (frames[j] == pages[i])
            {
                hit = 1;
                break;
            }
        }

        if (hit)
        {
            hits++;
        }
        else
        {
            frames[pointer] = pages[i];
            pointer = (pointer + 1) % framesCount;
            faults++;
        }

        printf("Page %d : ", pages[i]);

        for (int j = 0; j < framesCount; j++)
        {
            if (frames[j] == -1)
                printf("- ");
            else
                printf("%d ", frames[j]);
        }

        if (hit)
            printf(" HIT\n");
        else
            printf(" FAULT\n");
    }

    printf("\nTotal Hits   : %d\n", hits);
    printf("Total Faults : %d\n", faults);
}


/* ---------------- LRU ---------------- */

void lru(int pages[], int n, int framesCount)
{
    int frames[MAX];
    int lastUsed[MAX];

    int hits = 0, faults = 0;

    for (int i = 0; i < framesCount; i++)
    {
        frames[i] = -1;
        lastUsed[i] = -1;
    }

    printf("\n========== LRU ==========\n");

    for (int i = 0; i < n; i++)
    {
        int hit = 0;
        int position = -1;

        /* Check for hit */
        for (int j = 0; j < framesCount; j++)
        {
            if (frames[j] == pages[i])
            {
                hit = 1;
                position = j;
                break;
            }
        }

        if (hit)
        {
            hits++;
            lastUsed[position] = i;
        }
        else
        {
            faults++;

            int replace = -1;

            /* First check for empty frame */
            for (int j = 0; j < framesCount; j++)
            {
                if (frames[j] == -1)
                {
                    replace = j;
                    break;
                }
            }

            /* If no empty frame, find least recently used */
            if (replace == -1)
            {
                replace = 0;

                for (int j = 1; j < framesCount; j++)
                {
                    if (lastUsed[j] < lastUsed[replace])
                        replace = j;
                }
            }

            frames[replace] = pages[i];
            lastUsed[replace] = i;
        }

        printf("Page %d : ", pages[i]);

        for (int j = 0; j < framesCount; j++)
        {
            if (frames[j] == -1)
                printf("- ");
            else
                printf("%d ", frames[j]);
        }

        if (hit)
            printf(" HIT\n");
        else
            printf(" FAULT\n");
    }

    printf("\nTotal Hits   : %d\n", hits);
    printf("Total Faults : %d\n", faults);
}


/* ---------------- MAIN ---------------- */

int main()
{
    int pages[MAX];
    int n;
    int framesCount;

    printf("Enter number of page requests: ");
    scanf("%d", &n);

    printf("Enter reference string:\n");

    for (int i = 0; i < n; i++)
        scanf("%d", &pages[i]);

    printf("Enter number of frames: ");
    scanf("%d", &framesCount);

    fifo(pages, n, framesCount);

    lru(pages, n, framesCount);

    return 0;
}
