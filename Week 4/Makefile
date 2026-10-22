# Makefile for Week 4 Interactive Deadlock Simulation System
# Team Leader: Aditi Nayak

CC = gcc
CFLAGS = -Wall -Wextra -O2

SRCS = bankers.c deadlock.c rag.c recovery.c
OBJS = $(SRCS:.c=.o)

all: deadlock_sim.exe test_runner.exe

deadlock_sim.exe: main.o $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

test_runner.exe: test_runner.o $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

test: test_runner.exe
	./test_runner.exe

clean:
	rm -f *.o *.exe

.PHONY: all test clean
