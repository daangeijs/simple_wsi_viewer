create_superuser:
	docker compose run --rm web python manage.py createsuperuser
build:
	docker build -t wsi_viewer:latest .

migrations:
	docker compose run --rm web python manage.py makemigrations viewer

migrate:
	docker compose run --rm web python manage.py migrate

clear-cache:
	docker compose run --rm web python manage.py clear_cache

runserver: build migrations migrate clear-cache
	export FOLDER=$(FOLDER); \
	bash -c "trap 'docker compose down' EXIT; docker compose up"