# Makefile for Week 5 Page Replacement Simulator
# Team Leader: Aditi Nayak

CC = gcc
CFLAGS = -Wall -Wextra -O2

SRCS = fifo.c lru.c optimal.c metrics.c
OBJS = $(SRCS:.c=.o)

all: page_sim.exe test_runner.exe

page_sim.exe: main.o $(OBJS)
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
