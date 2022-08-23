#region CONFIG
COMPOSE_FILE := "images/docker-compose.yml"
MLB_COMPOSE_NAME := "load-balancer"
#endregion
#region SCRAPPED_CODE
#ifeq ($(c),)
#	c := $(MLB_COMPOSE_NAME)
#endif
#ifndef abc
#$(error abc is not set)
#endif
#endregion

THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help all build up start down destroy stop restart run updestroy logs logs-api ps login-timescale login-api db-shell
#region Makefile
help: ### Shows this help
	@awk 'BEGIN {FS = ":.*###"; printf "make \033[36m<command>\033[0m [c=image-name]\n\nUsage:\033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?###/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^###@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
all: ### Builds and runs specified flag or all image solutions
	make build c=$(c)
	make upndown c=$(c)
build: ### Builds the images
	docker-compose -f $(COMPOSE_FILE) build $(c)
up: ### Brings up a dormant container in detached mode
	docker-compose -f $(COMPOSE_FILE) up -d $(c)
start: ### Starts a container
	docker-compose -f $(COMPOSE_FILE) start $(c)
down: ### Brings down a running container
	docker-compose -f $(COMPOSE_FILE) down $(c)
destroy: ### Destroys specified container
	docker-compose -f $(COMPOSE_FILE) down -v $(c)
stop: ### Stops specified container
	docker-compose -f $(COMPOSE_FILE) stop $(c)
restart: ### Restarts specified container
	make stop c=$(c); make up c=$(c)
run: ### Runs an image and automatically removes it on exit
	docker-compose -f $(COMPOSE_FILE) run --rm $(if $(c),$(c),$(MLB_COMPOSE_NAME))
updestroy: ### Brings up a container and destroys it afterwards
	docker-compose -f $(COMPOSE_FILE) up $(c); docker-compose -f $(COMPOSE_FILE) down -v $(c)
#logs:
#	docker-compose -f $(COMPOSE_FILE) logs --tail=100 -f $(c)
#logs-api:
#	docker-compose -f $(COMPOSE_FILE) logs --tail=100 -f api
#ps:
#	docker-compose -f $(COMPOSE_FILE) ps
#login-timescale:
#	docker-compose -f $(COMPOSE_FILE) exec timescale /bin/bash
#login-api:
#	docker-compose -f $(COMPOSE_FILE) exec api /bin/bash
#db-shell:
#	docker-compose -f $(COMPOSE_FILE) exec timescale psql -Upostgres
#endregion