PYTHON ?= python3
WEEK ?=
OLDER_THAN_DAYS ?= 20

setup:
	bash scripts/setup_local.sh

run-api:
	$(PYTHON) -m uvicorn social_scheduler.api:app --reload --host $${APP_HOST:-127.0.0.1} --port $${APP_PORT:-8000}

create-week:
	$(PYTHON) scripts/create_week.py $(if $(WEEK),--week $(WEEK),)

validate-projects:
	$(PYTHON) scripts/validate_projects.py

schedule:
	$(PYTHON) scripts/run_scheduler.py

archive:
	$(PYTHON) scripts/archive_week.py $(if $(WEEK),--week $(WEEK),)

cleanup:
	$(PYTHON) scripts/cleanup_archive.py --older-than-days $(OLDER_THAN_DAYS)

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py" -v

install-cron:
	bash scripts/install_cron.sh
