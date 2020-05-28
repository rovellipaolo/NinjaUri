PWD := $(shell pwd)
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


# Build:
.PHONY: build
build:
	@pip3 install -r requirements.txt
	sudo ln -s $(ROOT_DIR)/ninjauri.py /usr/local/bin/ninjauri


# Run:
.PHONY: run
run:
	@python3 ninjauri.py $(uri)


# Test:
.PHONY: test
test:
	@python3 -m unittest
