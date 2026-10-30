# Makefile for Process Scheduling Simulator (Week 3 PBL)
# Team Leader: Aditi Nayak
# Modules: Anas (FCFS/RR/Input), Nireeksha (SJF/Gantt), Yaseem (Priority/Metrics)

CC = gcc
CFLAGS = -Wall -Wextra -O2

TARGET = scheduler.exe
SRCS = main.c input.c gantt.c fcfs.c sjf.c priority.c rr.c
OBJS = $(SRCS:.c=.o)

all: $(TARGET) test_runner.exe

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

test_runner.exe: test_runner.c gantt.c fcfs.c sjf.c priority.c rr.c
	$(CC) $(CFLAGS) -o $@ $^

test: test_runner.exe
	.\test_runner.exe

%.o: %.c process.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET) $(TARGET).exe test_runner test_runner.exe *.o

.PHONY: all test clean
