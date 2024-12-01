# Variables
PYTHON := python3
DNS_SERVER := dns_resolver.py

# Default Target
all: run

# Run the DNS Resolver
run:
	$(PYTHON) $(DNS_SERVER)

# Clean temporary or log files (if any in the future)
clean:
	rm -f *.log

# Help
help:
	@echo "Makefile for DNS Resolver Project"
	@echo "Usage:"
	@echo "  make run     - Run the DNS resolver"
	@echo "  make clean   - Clean temporary files"
	@echo "  make help    - Display this help message"
