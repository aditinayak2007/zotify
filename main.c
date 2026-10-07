/*
 * main.c - Multi-Process Simulator: IPC Coordinator & Integration
 * Written by: Aditi Nayak (Team Leader - Pipes IPC & Integration)
 *
 * Responsibilities:
 * 1. Initialize POSIX Pipes for inter-process communication:
 *    - ui_to_core[2]: UI Process -> Core Process
 *    - core_to_ui[2]: Core Process -> UI Process
 *    - core_to_logger[2]: Core Process -> Logging Process
 * 2. Fork and manage three distinct processes:
 *    - Process 1: Logging Process (Yaseem)
 *    - Process 2: Core Process (Nireeksha - CPU, Memory, Stack, Queue)
 *    - Process 3: UI Process (Anas)
 * 3. Enforce proper pipe hygiene:
 *    - Close unused read and write ends in each child process.
 *    - Close all pipe ends in the parent coordinator.
 *    - Prevent leaks, blocking, and deadlocks.
 * 4. Coordinate orderly shutdown:
 *    - Wait for child processes using waitpid() / wait().
 */

#include "pipe_ipc.h"
#include "ui.h"
#include "core.h"
#include "logger.h"

#ifdef _WIN32
/* Worker argument structures for Windows concurrent execution */
typedef struct {
    int read_fd;
} logger_thread_args_t;

typedef struct {
    int from_ui;
    int to_ui;
    int to_logger;
} core_thread_args_t;

typedef struct {
    int to_core;
    int from_core;
} ui_thread_args_t;

static void* run_logger_thread(void *arg) {
    logger_thread_args_t *args = (logger_thread_args_t*)arg;
    logger_process(args->read_fd);
    free(args);
    return NULL;
}

static void* run_core_thread(void *arg) {
    core_thread_args_t *args = (core_thread_args_t*)arg;
    core_process(args->from_ui, args->to_ui, args->to_logger);
    free(args);
    return NULL;
}

static void* run_ui_thread(void *arg) {
    ui_thread_args_t *args = (ui_thread_args_t*)arg;
    ui_process(args->to_core, args->from_core);
    free(args);
    return NULL;
}
#endif

int main(void)
{
    printf("=====================================================\n");
    printf(" MULTI-PROCESS SIMULATOR (WEEK 4 PBL)\n");
    printf(" Team: Anas (UI) | Nireeksha (Core) | Yaseem (Logger)\n");
    printf(" IPC Coordinator: Aditi Nayak (POSIX Pipes)\n");
    printf("=====================================================\n\n");

    /*
     * 1. Create Pipes
     * ui_to_core:      UI -> Core
     * core_to_ui:      Core -> UI
     * core_to_logger:  Core -> Logger
     */
    int ui_to_core[2];
    int core_to_ui[2];
    int core_to_logger[2];

    if (pipe(ui_to_core) == -1)
    {
        perror("Coordinator: Failed to create ui_to_core pipe");
        exit(EXIT_FAILURE);
    }

    if (pipe(core_to_ui) == -1)
    {
        perror("Coordinator: Failed to create core_to_ui pipe");
        close(ui_to_core[0]);
        close(ui_to_core[1]);
        exit(EXIT_FAILURE);
    }

    if (pipe(core_to_logger) == -1)
    {
        perror("Coordinator: Failed to create core_to_logger pipe");
        close(ui_to_core[0]);
        close(ui_to_core[1]);
        close(core_to_ui[0]);
        close(core_to_ui[1]);
        exit(EXIT_FAILURE);
    }

    printf("[COORDINATOR] Pipes initialized successfully:\n");
    printf("  - UI -> Core Pipe:     [read=%d, write=%d]\n", ui_to_core[0], ui_to_core[1]);
    printf("  - Core -> UI Pipe:     [read=%d, write=%d]\n", core_to_ui[0], core_to_ui[1]);
    printf("  - Core -> Logger Pipe: [read=%d, write=%d]\n\n", core_to_logger[0], core_to_logger[1]);

#ifndef _WIN32
    /* =====================================================
     * POSIX FORK IMPLEMENTATION (Linux / Unix / macOS / WSL)
     * ===================================================== */

    /* Process 1: Fork Logging Process (Yaseem) */
    pid_t pid_logger = fork();
    if (pid_logger < 0)
    {
        perror("Coordinator: fork() failed for Logging Process");
        exit(EXIT_FAILURE);
    }
    if (pid_logger == 0)
    {
        /* In Logger child process:
         * Close unused pipe descriptors:
         *  - UI <-> Core pipes are not needed by Logger
         *  - Write end of Core -> Logger pipe is closed
         */
        close(ui_to_core[0]);
        close(ui_to_core[1]);
        close(core_to_ui[0]);
        close(core_to_ui[1]);
        close(core_to_logger[1]);

        /* Execute Logger Process */
        logger_process(core_to_logger[0]);

        close(core_to_logger[0]);
        exit(EXIT_SUCCESS);
    }

    /* Process 2: Fork Core Process (Nireeksha) */
    pid_t pid_core = fork();
    if (pid_core < 0)
    {
        perror("Coordinator: fork() failed for Core Process");
        exit(EXIT_FAILURE);
    }
    if (pid_core == 0)
    {
        /* In Core child process:
         * Close unused pipe descriptors:
         *  - Write end of UI -> Core pipe (UI writes, Core only reads)
         *  - Read end of Core -> UI pipe (Core writes, UI reads)
         *  - Read end of Core -> Logger pipe (Core writes, Logger reads)
         */
        close(ui_to_core[1]);
        close(core_to_ui[0]);
        close(core_to_logger[0]);

        /* Execute Core Process */
        core_process(ui_to_core[0], core_to_ui[1], core_to_logger[1]);

        close(ui_to_core[0]);
        close(core_to_ui[1]);
        close(core_to_logger[1]);
        exit(EXIT_SUCCESS);
    }

    /* Process 3: Fork UI Process (Anas) */
    pid_t pid_ui = fork();
    if (pid_ui < 0)
    {
        perror("Coordinator: fork() failed for UI Process");
        exit(EXIT_FAILURE);
    }
    if (pid_ui == 0)
    {
        /* In UI child process:
         * Close unused pipe descriptors:
         *  - Read end of UI -> Core pipe (UI only writes)
         *  - Write end of Core -> UI pipe (UI only reads)
         *  - Both ends of Core -> Logger pipe (UI does not touch Logger pipe)
         */
        close(ui_to_core[0]);
        close(core_to_ui[1]);
        close(core_to_logger[0]);
        close(core_to_logger[1]);

        /* Execute UI Process */
        ui_process(ui_to_core[1], core_to_ui[0]);

        close(ui_to_core[1]);
        close(core_to_ui[0]);
        exit(EXIT_SUCCESS);
    }

    /*
     * Coordinator Parent Process (Aditi):
     * Close all pipe ends in coordinator so EOF propagates when children exit.
     */
    close(ui_to_core[0]);
    close(ui_to_core[1]);
    close(core_to_ui[0]);
    close(core_to_ui[1]);
    close(core_to_logger[0]);
    close(core_to_logger[1]);

    printf("[COORDINATOR] All 3 processes spawned successfully:\n");
    printf("  - Logging Process PID: %d\n", (int)pid_logger);
    printf("  - Core Process PID:    %d\n", (int)pid_core);
    printf("  - UI Process PID:      %d\n\n", (int)pid_ui);

    /* Wait for child processes to terminate cleanly */
    int status;
    waitpid(pid_ui, &status, 0);
    printf("[COORDINATOR] UI Process exited.\n");

    waitpid(pid_core, &status, 0);
    printf("[COORDINATOR] Core Process exited.\n");

    waitpid(pid_logger, &status, 0);
    printf("[COORDINATOR] Logging Process exited.\n");

    printf("\n[COORDINATOR] Multi-Process Simulator finished successfully.\n");

#else
    /* =====================================================
     * WINDOWS COMPATIBILITY EXECUTION (MinGW / Windows)
     * ===================================================== */
    pthread_t thread_logger, thread_core, thread_ui;

    logger_thread_args_t *l_args = (logger_thread_args_t*)malloc(sizeof(logger_thread_args_t));
    l_args->read_fd = core_to_logger[0];
    pthread_create(&thread_logger, NULL, run_logger_thread, l_args);

    core_thread_args_t *c_args = (core_thread_args_t*)malloc(sizeof(core_thread_args_t));
    c_args->from_ui = ui_to_core[0];
    c_args->to_ui = core_to_ui[1];
    c_args->to_logger = core_to_logger[1];
    pthread_create(&thread_core, NULL, run_core_thread, c_args);

    ui_thread_args_t *u_args = (ui_thread_args_t*)malloc(sizeof(ui_thread_args_t));
    u_args->to_core = ui_to_core[1];
    u_args->from_core = core_to_ui[0];
    pthread_create(&thread_ui, NULL, run_ui_thread, u_args);

    /* Wait for processes/threads to finish */
    pthread_join(thread_ui, NULL);
    printf("[COORDINATOR] UI Process completed.\n");

    pthread_join(thread_core, NULL);
    printf("[COORDINATOR] Core Process completed.\n");

    pthread_join(thread_logger, NULL);
    printf("[COORDINATOR] Logging Process completed.\n");

    printf("\n[COORDINATOR] Multi-Process Simulator finished successfully.\n");
#endif

    return 0;
}
