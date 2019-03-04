start:
	bash ./.makefile/start.sh

stop:
	docker-compose stop

clean:
	bash ./.makefile/clean.sh

logs:
	docker-compose logs -f

offline:
	docker-compose exec app npx serverless offline --preserveTrailingSlash

migrations:
	docker-compose exec app python manage.py makemigrations
	docker-compose exec app python manage.py migrate

bash:
	docker-compose exec app bash
