clean:
	docker-compose down

up:
	docker-compose up

acceptance:
	docker-compose exec app run-contexts -v ./tests/acceptance

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
	python3 -m shortener.bootstrap

unit:
	run-contexts -v tests/unit

unit-watch:
	ls **/*.py | entr run-contexts -v tests/unit
