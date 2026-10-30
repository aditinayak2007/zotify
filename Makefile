# Root Makefile for Operating Systems PBL Projects
# Team Leader: Aditi Nayak (GitHub: aditinayak2007)

all: week2 week3 week4 week5

week2:
	$(MAKE) -C "Week 2"

week3:
	$(MAKE) -C "Week 3"

week4:
	$(MAKE) -C "Week 4"

week5:
	$(MAKE) -C "Week 5"

test:
	$(MAKE) -C "Week 3" test
	$(MAKE) -C "Week 4" test
	$(MAKE) -C "Week 5" test

clean:
	$(MAKE) -C "Week 2" clean
	$(MAKE) -C "Week 3" clean
	$(MAKE) -C "Week 4" clean
	$(MAKE) -C "Week 5" clean

.PHONY: all week2 week3 week4 week5 test clean
