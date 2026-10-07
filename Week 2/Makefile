# Makefile for Multi-Process Simulator (Week 4 PBL)
# Team Leader: Aditi Nayak (POSIX Pipes IPC)
# Members: Anas (UI), Nireeksha (Core), Yaseem (Logger)

CC ?= gcc
CFLAGS ?= -Wall -Wextra -O2
LDFLAGS ?= -pthread

TARGET = simulator
SRCS = main.c ui.c core.c logger.c
OBJS = $(SRCS:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LDFLAGS)

%.o: %.c pipe_ipc.h ui.h core.h logger.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET) $(TARGET).exe ui_test core_test logger_test yaseem.log nireeksha_log.txt

# Standalone builds for individual testing
ui_test: ui.c
	$(CC) $(CFLAGS) -DUI_STANDALONE -o $@ ui.c $(LDFLAGS)

core_test: core.c
	$(CC) $(CFLAGS) -DCORE_STANDALONE -o $@ core.c $(LDFLAGS)

logger_test: logger.c
	$(CC) $(CFLAGS) -DLOGGER_STANDALONE -o $@ logger.c $(LDFLAGS)

.PHONY: all clean ui_test core_test logger_test
