up:
	docker-compose up

acceptance: up wait-for-app
	docker-compose exec app run-contexts ./tests/acceptance

wait-for-app:
	while ! nc -z localhost 5000; do echo "Waiting for app"; sleep 2; done; \
	sleep 2; \


start-db:
	docker-compose up -d db

up-db: start-db run-migrations

run-migrations:
	while ! nc -z localhost 5432; do echo "Waiting for DB"; sleep 2; done; \
	sleep 2; \
	alembic upgrade head

start-app-local: up-db
	FLASK_APP=shortener/app.py flask run

unit:
	run-contexts -v tests/unit

unit-watch:
	ls **/*.py | entr run-contexts -v tests/unit
