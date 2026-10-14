# Root Makefile for Operating Systems PBL Projects
# Team Leader: Aditi Nayak (GitHub: aditinayak2007)

all: week2 week3

week2:
	$(MAKE) -C "Week 2"

week3:
	$(MAKE) -C "Week 3"

test:
	$(MAKE) -C "Week 3" test

clean:
	$(MAKE) -C "Week 2" clean
	$(MAKE) -C "Week 3" clean

.PHONY: all week2 week3 test clean
