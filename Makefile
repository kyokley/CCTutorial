.PHONY: attach build down format logs migrate shell tests up

build:
	docker build -t kyokley/cc .

shell: build
	docker run --rm -it -v $$(pwd):/code kyokley/cc /bin/bash

# format: build
	# Normally I like to use black formatting isort on my code but was afraid it would
	# add too much noise to the PR.
	# docker run --rm -t -v $$(pwd):/code kyokley/cc /venv/bin/black .
	# docker run --rm -t -v $$(pwd):/code kyokley/cc /venv/bin/isort .

up: build
	docker run --rm -it -d -v $$(pwd):/code -p 127.0.0.1:8000:8000 kyokley/cc
	docker run --rm -t -v $$(pwd):/code kyokley/cc python manage.py migrate
	docker logs --follow $$(docker ps | grep kyokley/cc | awk '{print $$1}')

down:
	docker stop $$(docker ps | grep kyokley/cc | awk '{print $$1}')

attach:
	docker attach $$(docker ps | grep kyokley/cc | awk '{print $$1}')

logs:
	docker logs --follow $$(docker ps | grep kyokley/cc | awk '{print $$1}')

migrate: build
	docker run --rm -t -v $$(pwd):/code kyokley/cc python manage.py migrate

tests: build
	docker run --rm -t -v $$(pwd):/code kyokley/cc pytest
