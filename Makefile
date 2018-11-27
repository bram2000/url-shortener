up:
	docker-compose up

up-db: run-migrations
	docker-compose up -d db

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

acceptance:
	run-contexts -vs tests/acceptance

docker-acceptance: up-db
	docker-compose run app run-contexts -v tests/acceptance
