DOCKER_FILE :=  docker/Dockerfile
DOCKER_IMAGE := ninjauri
DOCKER_TAG := latest
FLATPAK_MANIFEST := flatpak/com.github.rovellipaolo.NinjaUri.yaml
PWD := $(shell pwd)
NINJAURI_HOME := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


# Build:
.PHONY: build
build:
	@pip3 install -r requirements.txt

.PHONY: build-docker
build-docker:
	@docker build -f ${DOCKER_FILE} -t ${DOCKER_IMAGE}:${DOCKER_TAG} .

.PHONY: build-flatpak
build-flatpak:
	@flatpak install flathub org.freedesktop.Platform//22.08 org.freedesktop.Sdk//22.08 --user
	@flatpak-builder flatpak/build ${FLATPAK_MANIFEST} --force-clean

.PHONY: build-snap
build-snap:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	rm -f ninjauri_*.snap
	@snapcraft clean
	@snapcraft

.PHONY: generate-checkstyle-config
generate-checkstyle-config:
	pylint --generate-rcfile > .pylintrc


# Install:
.PHONY: install
install:
	sudo ln -s ${NINJAURI_HOME}/ninjauri.py /usr/local/bin/ninjauri

.PHONY: uninstall
uninstall:
	sudo unlink /usr/local/bin/ninjauri

.PHONY: install-snap
install-snap:
	snap install ninjauri_2.0_amd64.snap --devmode

.PHONY: uninstall-snap
uninstall-snap:
	snap remove ninjauri

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
	@docker run --name ${DOCKER_IMAGE} -it --rm ${DOCKER_IMAGE}:${DOCKER_TAG} ninjauri $(uri) --json

.PHONY: run-flatpak
run-flatpak:
	@flatpak-builder --run flatpak/build ${FLATPAK_MANIFEST} ninjauri $(uri)


# Test:
.PHONY: test
test:
	@python3 -m unittest

.PHONY: test-coverage
test-coverage:
	@coverage3 run --source=. --omit="tests/*" -m unittest
	@coverage3 report

.PHONY: test-docker
test-docker:
	@docker run --name ${DOCKER_IMAGE} --rm -w /opt/NinjaUri -v ${NINJAURI_HOME}/tests:/opt/NinjaUri/tests ${DOCKER_IMAGE}:${DOCKER_TAG} python3 -m unittest

.PHONY: checkstyle
checkstyle:
	pycodestyle --max-line-length=120 ninjauri.py tests/
	pylint ninjauri.py tests/

.PHONY: checkstyle-docker
checkstyle-docker:
	@docker run --name ${DOCKER_IMAGE} --rm -w /opt/NinjaUri -v ${NINJAURI_HOME}/.pylintrc:/opt/NinjaUri/.pylintrc ${DOCKER_IMAGE}:${DOCKER_TAG} pycodestyle --max-line-length=120 ninjauri.py && pylint ninjauri.py
