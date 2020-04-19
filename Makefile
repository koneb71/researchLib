build:
	docker-compose build

up:
	docker-compose up -d

up-non-daemon:
	docker-compose up

start:
	docker-compose start

stop:
	docker-compose stop

restart:
	docker-compose stop && docker-compose start

shell-nginx:
	docker exec -ti NGINX /bin/sh

shell-web:
	docker exec -ti APP /bin/sh

shell-db:
	docker exec -ti DB /bin/sh

log-nginx:
	docker-compose logs nginx

log-web:
	docker-compose logs app

log-db:
	docker-compose logs db

collectstatic:
	docker exec -ti APP /bin/sh -c "python manage.py collectstatic --noinput"

createsuperuser:
    docker exec -ti APP /bin/sh -c "python manage.py createsuperuser"