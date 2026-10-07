#ifndef CORE_H
#define CORE_H

/*
 * Core Process (Nireeksha)
 * Contains CPU, Memory, Stack, and Queue subsystems.
 *  - Reads commands from UI via from_ui pipe
 *  - Executes arithmetic/memory/stack/queue operations
 *  - Sends replies to UI via to_ui pipe
 *  - Forwards execution logs to Logging process via to_logger pipe
 */
int core_process(int from_ui, int to_ui, int to_logger);

#endif /* CORE_H */
