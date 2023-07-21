.PHONY: superuser
superuser:
	python -m tracksales.manage createsuperuser

.PHONY: migrations
migrations:
	python -m tracksales.manage makemigrations

.PHONY: migrate
migrate:
	python -m tracksales.manage migrate

.PHONY: collectstatic
collectstatic:
	python -m tracksales.manage collectstatic

.PHONY: shell
shell:
	python -m tracksales.manage shell

.PHONY: dbshell
dbshell:
	python -m tracksales.manage dbshell

.PHONY: run-server
run-server:
	python -m tracksales.manage runserver 127.0.0.1:8000
