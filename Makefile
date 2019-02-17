.PHONY: clean bootstrap test coverage migratedb runserver

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf .coverage

virtualenv:
	virtualenv --no-site-packages $(VIRTUAL_ENV)
	echo $(VIRTUAL_ENV)

pip: requirements.txt
	pip install -r requirements.txt

bootstrap: virtualenv pip

test: clean
	coverage run manage.py test api

coverage:
	coverage html --omit="*/admin.py,*/test*"

migratedb:
	python manage.py migrate

runserver:
	python manage.py runserver