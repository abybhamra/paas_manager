PYTHON=${PYENV}/bin/python
PYENV=paas_mgr_env

.DEFAULT: help
help:
	@echo "Available commands are:"
	@echo "make run_api"
	@echo "make run_test"

clean_slate:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	-rm -rf *pycache*
	-rm -rf htmlcov
	-rm -rf .coverage

prepare_env:clean_slate
	python3 -m venv ${PYENV}
	. ./${PYENV}/bin/activate
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r requirements.txt

source_env:
	. ./${PYENV}/bin/activate

migrate_db:
	${PYTHON} manage.py migrate

run_server:
	${PYTHON} manage.py runserver

run_test:
	${PYTHON} -m coverage run manage.py test api

generate_coverage:
	${PYTHON} -m coverage html --omit="*/admin.py,*/test*"

run_test: prepare_env source_env migrate_db run_test generate_coverage

run_api:prepare_env source_env migrate_db run_server