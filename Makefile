# Root Makefile forwarding to Week 2 Multi-Process Simulator
# Team Leader: Aditi Nayak

all:
	$(MAKE) -C "Week 2"

clean:
	$(MAKE) -C "Week 2" clean

.PHONY: all clean
