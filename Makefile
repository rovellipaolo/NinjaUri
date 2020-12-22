DOCKER_IMAGE := ninjauri
DOCKER_TAG := latest
PWD := $(shell pwd)
NINJAURI_HOME := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


# Build:
.PHONY: build
build:
	@pip3 install -r requirements.txt

.PHONY: build-docker
build-docker:
	@docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .


# Install:
.PHONY: install
install:
	sudo ln -s $(NINJAURI_HOME)/ninjauri.py /usr/local/bin/ninjauri

.PHONY: uninstall
uninstall:
	sudo unlink /usr/local/bin/ninjauri

.PHONY: install-githooks
install-githooks:
	@pip3 install pre-commit
	pre-commit install

.PHONY: uninstall-githooks
uninstall-githooks:
	pre-commit uninstall


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

.PHONY: test-coverage
test-coverage:
	@coverage3 run --source=. -m unittest
	@coverage3 report

.PHONY: test-docker
test-docker:
	@docker run --name ${DOCKER_IMAGE} --rm -w /opt/NinjaUri ${DOCKER_IMAGE}:${DOCKER_TAG} python3 -m unittest

.PHONY: checkstyle
checkstyle:
	pylint ninjauri.py
