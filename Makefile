build:
	docker build -t kyokley/cc .

shell: build
	docker run --rm -it -v $$(pwd):/code kyokley/cc /bin/bash

format: build
	docker run --rm -t -v $$(pwd):/code kyokley/cc /venv/bin/black .
	docker run --rm -t -v $$(pwd):/code kyokley/cc /venv/bin/isort .

run: build
	docker run --rm -v $$(pwd):/code -p 127.0.0.1:8000:8000 --workdir=/code/cctutorial kyokley/cc

migrate: build
	docker run --rm -t -v $$(pwd):/code --workdir=/code/cctutorial kyokley/cc python manage.py migrate
