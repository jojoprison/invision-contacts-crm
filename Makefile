.PHONY: build up down logs shell migrate createuser tenant test clean

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec web python src/manage.py shell

migrate:
	docker-compose exec web python src/manage.py migrate

createuser:
	docker-compose exec web python src/manage.py createsuperuser

tenant:
	@read -p "Введите схему тенанта: " schema; \
	read -p "Введите название тенанта: " name; \
	docker-compose exec web python src/manage.py create_tenant $$schema "$$name"

test:
	docker-compose exec web python src/manage.py test

clean:
	docker-compose down -v
	docker volume rm invision-contacts-crm_postgres_data invision-contacts-crm_redis_data || true

reset: clean build up
	echo "Система полностью пересоздана"
