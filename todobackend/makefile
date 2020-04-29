PROJECT_NAME ?= todobackend
ORG_NAME ?= reboot87
REPO_NAME ?= todobackend

# Filenames
DEV_COMPOSE_FILE := docker/dev/docker-compose.yml
REL_COMPOSE_FILE := docker/release/docker-compose.yml

# Docker Compose Project Names
REL_PROJECT := $(PROJECT_NAME)$(BUILD_ID)
DEV_PROJECT := $(REL_PROJECT)dev

# Check and Inspect Logic
INSPECT := $$(docker-compose -p $$1 -f $$2 ps -q $$3 | xargs -I ARGS docker inspect -f "{{ .State.ExitCode }}" ARGS)

CHECK := @bash -c '\
	if [[ $(INSPECT) -ne 0 ]]; \
	then exit $(INSPECT); fi' VALUE

.PHONY: test build release clean

test:
	${INFO} "Staring test environment..."
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) pull
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) build --pull test
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) run --rm agent
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) up test
	docker cp $$(docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) ps -q test):/reports/. reports
	${CHECK} $(DEV_PROJECT) $(DEV_COMPOSE_FILE) test
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) down
	${INFO} "Test environment stopped"

build:
	${INFO} "Building application artifacts..."
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) build builder
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) up builder
	${CHECK} $(DEV_PROJECT) $(DEV_COMPOSE_FILE) builder
	docker cp $$(docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) ps -q builder):/wheelhouse/. target
	${INFO} "Build complete"

release:
	${INFO} "Staring release environment..."
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) pull test
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) build app
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) build --pull nginx
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) run --rm agent
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) run --rm app manage.py collectstatic --no-input
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) run --rm app manage.py migrate --no-input
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) up test
	docker cp $$(docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) ps -q test):/reports/. reports
	${CHECK} $(REL_PROJECT) $(REL_COMPOSE_FILE) test
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) kill
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) rm -f	
	${INFO} "Release environment stopped"

# Not working... needs looking into. works when running seperatley from folders...
# app:
# 	docker-compose -p $(REL_PROJECT) -f ../../todobackend-client/docker-compose.yml up -d && \
# 		docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) up -d app 

clean:
	${INFO} "Destroying development environment..."
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) kill
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) rm -fv
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) kill
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) rm -fv	
	docker-compose -p $(REL_PROJECT) -f ../../todobackend-client/docker-compose.yml kill
	docker-compose -p $(REL_PROJECT) -f ../../todobackend-client/docker-compose.yml rm -f
	docker images -q -f dangling=true | xargs -I ARGS docker rmi -f ARGS
	${INFO} "Clean complete"


# Cosmetics
YELLOW := "\e[1;33m"
NC := "\e[0m"

# Shell functions
INFO := @bash -c '\
	printf $(YELLOW); \
	echo "=> $$1"; \
	printf $(NC)' VALUE