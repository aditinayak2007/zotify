#ifndef PIPE_IPC_H
#define PIPE_IPC_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
/* ================= Windows Compatibility Layer ================= */
#include <io.h>
#include <fcntl.h>
#include <process.h>
#include <windows.h>
#include <pthread.h>

#define pipe(fds) _pipe(fds, 4096, _O_BINARY)
#ifndef STDIN_FILENO
#define STDIN_FILENO 0
#endif
#ifndef STDOUT_FILENO
#define STDOUT_FILENO 1
#endif
#ifndef STDERR_FILENO
#define STDERR_FILENO 2
#endif

#else
/* ================= Standard POSIX Header ================= */
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>

#endif

#define BUFFER_SIZE 256
#define LOG_FILE "yaseem.log"

/* Function declarations for the three modular processes */
int ui_process(int to_core, int from_core);
int core_process(int from_ui, int to_ui, int to_logger);
int logger_process(int pipe_read_fd);

#endif /* PIPE_IPC_H */
