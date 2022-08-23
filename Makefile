COMPOSE_FILE := "docker-compose.yml"
MLB_COMPOSE_NAME := "metric-load-balancer"
#region SCRAPPED_CODE
#ifeq ($(c),)
#	c := $(MLB_COMPOSE_NAME)
#endif
#ifndef abc
#$(error abc is not set)
#endif
#endregion

THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help all build up start down destroy stop restart run updestroy logs ps stats mlb logs-mlb login-mlb
help: ### Shows this help
	@awk 'BEGIN {FS = ":.*###"; printf "make \033[36m<command>\033[0m [c=image-name]\n\nUsage:\033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?###/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^###@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
##
all: ### Builds and runs specified flag or all image solutions
	make build c=$(c)
	make up c=$(c)
build: ### Builds the images
	docker-compose -f $(COMPOSE_FILE) build $(c)
up: ### Brings up a dormant container in detached mode
	docker-compose -f $(COMPOSE_FILE) up --force-recreate -d $(c)
start: ### Starts a container
	docker-compose -f $(COMPOSE_FILE) start $(c)
down: ### Brings down a running container
	docker-compose -f $(COMPOSE_FILE) down $(c)
stop: ### Stops specified container
	docker-compose -f $(COMPOSE_FILE) stop $(c)
rm: ### Destroys specified container
	docker-compose -f $(COMPOSE_FILE) down -v $(c)
restart: ### Restarts specified container
	make stop c=$(c); make up c=$(c)
run: ### Runs an image and automatically removes it on exit
	docker-compose -f $(COMPOSE_FILE) run --rm $(if $(entrypoint),--entrypoint=$(entrypoint),) $(if $(c),$(c),$(MLB_COMPOSE_NAME))
updestroy: ### Brings up a container and destroys it afterwards
	docker-compose -f $(COMPOSE_FILE) up $(c); docker-compose -f $(COMPOSE_FILE) down -v $(c)
logs: ### Bring up logs for app
	docker-compose -f $(COMPOSE_FILE) logs --tail=100 -f $(c)
ps: ### Shows running containers
	docker-compose -f $(COMPOSE_FILE) ps
stats: ### Shows resources being consumed by the system
	docker ps --format={{.Names}} --filter "label=com.docker.compose.project=metric-load-balancer" | xargs docker stats
##
mlb: ### Builds MLB and runs self-removing instance.
	make build c=$(MLB_COMPOSE_NAME); make run c=$(MLB_COMPOSE_NAME)
logs-mlb: ### Bring up logs for MLB
	docker-compose -f $(COMPOSE_FILE) logs --tail=100 -f $(MLB_COMPOSE_NAME)
login-mlb: ### Login to MLB with shell
	docker-compose -f $(COMPOSE_FILE) exec $(MLB_COMPOSE_NAME) /bin/bash