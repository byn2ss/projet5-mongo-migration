.PHONY: venv install test dry-run migrate up down logs

venv:
	python -m venv .venv

install: venv
	. .venv/bin/activate && pip install -r requirements.txt

test:
	. .venv/bin/activate && pytest -q

dry-run:
	. .venv/bin/activate && python scripts/migrate_dry_run.py --csv data/patients_sample.csv --id-field id

migrate:
	. .venv/bin/activate && python src/migrate.py --csv data/patients_sample.csv --export-json out.json

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker logs -f mongo-medical
