DOCKER_IMAGE := ninjauri
DOCKER_TAG := latest
PWD := $(shell pwd)
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


# Build:
.PHONY: build
build:
	@pip3 install -r requirements.txt
	sudo ln -s $(ROOT_DIR)/ninjauri.py /usr/local/bin/ninjauri

.PHONY: build-docker
build-docker:
	@docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .


# Run:
.PHONY: run
run:
	@python3 ninjauri.py $(uri)

.PHONY: run-docker
run-docker:
	@docker run --name ${DOCKER_IMAGE} -it --rm ${DOCKER_IMAGE}:${DOCKER_TAG} ninjauri $(uri)


# Test:
.PHONY: test
test:
	@python3 -m unittest

.PHONY: test-docker
test-docker:
	@docker run --name ${DOCKER_IMAGE} --rm -w /opt/NinjaUri ${DOCKER_IMAGE}:${DOCKER_TAG} python3 -m unittest
