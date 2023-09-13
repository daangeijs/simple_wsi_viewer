create_superuser:
	docker compose run --rm web python manage.py createsuperuser
build:
	docker build -t wsu_viewer:latest .

migrations:
	docker compose run --rm web python manage.py makemigrations viewer

migrate:
	docker compose run --rm web python manage.py migrate

runserver: build migrations migrate
	bash -c "trap 'docker compose down' EXIT; docker compose up"