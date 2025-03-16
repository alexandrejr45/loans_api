#!/bin/sh

install:
	docker-compose build

run:
	docker-compose build
	docker-compose up

run-dev:
	python app/manage.py runserver:8000

clear:
	docker-compose down -v

