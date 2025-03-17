#!/bin/sh

install:
	docker-compose build

migrate:
	docker-compose exec api python manage.py flush --no-input
	docker-compose exec api python manage.py migrate

run: install
	docker-compose up -d
	docker-compose exec api python manage.py flush --no-input
	docker-compose exec api python manage.py migrate
	docker-compose exec api python manage.py createsuperuser --noinput


run-dev:
	python app/manage.py runserver:8000

clear:
	docker-compose down -v

stop:
	docker-compose stop