#ifndef LOGGER_H
#define LOGGER_H

#define LOG_FILE "yaseem.log"

/*
 * Logging Process (Yaseem)
 * Responsibilities:
 * 1. Receive execution logs from Core through a POSIX pipe
 * 2. Record successful operations
 * 3. Record errors
 * 4. Record important events
 * 5. Store information in yaseem.log
 */
int logger_process(int pipe_read_fd);

#endif /* LOGGER_H */
