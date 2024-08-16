build:
	docker compose build
	CMD="poetry install" $(MAKE) run-backend-command
	CMD="poetry run python manage.py migrate" $(MAKE) run-backend-command

migrate:
	@CMD="poetry run python manage.py migrate" $(MAKE) run-backend-command

migrations:
	CMD="poetry run python manage.py makemigrations" $(MAKE) run-backend-command

run:
	docker compose up

pre-commit:
	pre-commit run -a

run-backend-command:
	@docker compose run --rm backend $(CMD)

shell:
	@CMD="/bin/bash" $(MAKE) run-backend-command

update-entities:
	CMD="poetry run python manage.py update_entities" $(MAKE) run-backend-command
