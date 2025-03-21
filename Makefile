#!/bin/sh

install-dev:
	docker-compose build

install:
	docker-compose -f docker-compose.prod.yml build

migrate:
	python app/manage.py flush --no-input
	python app/manage.py makemigrations loan_simulation
	python app/manage.py migrate

run-dev: install-dev
	docker-compose up -d
	docker-compose exec api python manage.py flush --no-input
	docker-compose exec api python manage.py migrate


run: install tests
	docker-compose -f docker-compose.prod.yml up -d
	docker-compose -f docker-compose.prod.yml exec api python manage.py migrate
	docker-compose -f docker-compose.prod.yml exec api python manage.py collectstatic --no-input --clear

create-super-user:
	docker-compose -f docker-compose.prod.yml exec api python manage.py createsuperuser --noinput

fix-imports:
	@poetry run isort app/

clear:
	docker-compose -f docker-compose.prod.yml down -v

clear-dev:
	docker-compose down -v

lint: fix-imports
	@poetry run flake8 --show-source .

stop:
	docker-compose -f docker-compose.prod.yml stop

stop-dev:
	docker-compose -f docker-compose.prod.yml stop

tests:
	@poetry run pytest app/