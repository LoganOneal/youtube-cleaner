define TARGETS
web \
worker
endef

all: build serve

build: build-web build-worker
serve: server-web serve-worker
stop: stop-web stop-worker
restart: restart-web restart-worker
clean: clean-web clean-worker

.PHONY: build serve down stop restart clean

define target_template
$(1):
	docker-compose -f docker-compose.yml build ${1}
serve-$(1):
	docker-compose -f docker-compose.yml up -d ${1}
down-$(1):
	docker-compose -f docker-compose.yml down ${1}
clean-$(1):
	docker-compose -f docker-compose.yml down -v 
stop-$(1):
	docker-compose -f docker-compose.yml stop ${1}
restart-$(1):
	docker-compose -f docker-compose.yml stop ${1}
	docker-compose -f docker-compose.yml up -d ${1}
reload-deps-$(1):
	docker-compose run ${1} pip install -r requirements.txt
endef

$(foreach t,$(TARGETS), $(eval $(call target_template,$(t))))

list help:
	@$(MAKE) -rpn | sed -n -e '/^$$/ { n ; /^[^ .#][^ ]*:/p ; }' | sort | egrep --color '^[^ ]*:'
