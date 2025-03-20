#!/bin/sh

install:
	docker-compose build

migrate:
	python app/manage.py flush --no-input
	python app/manage.py makemigrations loan_simulation
	python app/manage.py migrate

run: install
	docker-compose up -d
	docker-compose exec api python manage.py flush --no-input
	docker-compose exec api python manage.py flush --no-input
	docker-compose exec api python manage.py migrate
	docker-compose exec api python manage.py createsuperuser --noinput

fix-imports:
	@poetry run isort app/

run-dev:
	python app/manage.py runserver:8000

clear:
	docker-compose down -v

lint: fix-imports
	@poetry run flake8 --show-source .

stop:
	docker-compose stop

tests:
	@poetry run pytest app/