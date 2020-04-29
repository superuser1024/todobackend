PROJECT_NAME ?= todobackend
ORG_NAME ?= reboot87
REPO_NAME ?= todobackend

# Filenames
DEV_COMPOSE_FILE := docker/dev/docker-compose.yml
REL_COMPOSE_FILE := docker/release/docker-compose.yml

# Docker Compose Project Names
REL_PROJECT := $(PROJECT_NAME)$(BUILD_ID)
DEV_PROJECT := $(REL_PROJECT)dev

.PHONY: test build release clean

test:
	${INFO} "Staring test environment..."
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) build
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) up agent
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) up test
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) down
	${INFO} "Test environment stopped"

build:
	${INFO} "Building application artifacts..."
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) build builder
	docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) up builder
	${INFO} "Build complete"

release:
	${INFO} "Staring release environment..."
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) build
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) up agent
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) run --rm app manage.py collectstatic --no-input
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) run --rm app manage.py migrate --no-input
	docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) up test
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