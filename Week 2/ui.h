#ifndef UI_H
#define UI_H

/*
 * UI Process (Anas Ahmed)
 * Handles user interaction:
 *  - Prompts the user
 *  - Reads and cleans commands
 *  - Sends commands to Core via to_core pipe
 *  - Reads replies from Core via from_core pipe
 *  - Displays results
 */
int ui_process(int to_core, int from_core);

#endif /* UI_H */
