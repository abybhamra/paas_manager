SHELL := /bin/sh

PROJECT := paas_manager

LOCALPATH := ./paas_manager
PYTHONPATH := $(LOCALPATH)/
LOCAL_SETTINGS := local
DJANGO_LOCAL_SETTINGS_MODULE = $(PROJECT).settings.$(LOCAL_SETTINGS)
DJANGO_LOCAL_POSTFIX := --settings=$(DJANGO_LOCAL_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
PYTHON_BIN := $(VIRTUAL_ENV)/bin

.PHONY: clean showenv coverage test bootstrap pip virtualenv virtual_env_set

showenv:
	@echo 'Environment:'
	@echo '-----------------------'
	@$(PYTHON_BIN)/python -c "import sys; print 'sys.path:', sys.path"
	@echo 'PYTHONPATH:' $(PYTHONPATH)
	@echo 'PROJECT:' $(PROJECT)
	@echo 'DJANGO_SETTINGS_MODULE:' $(DJANGO_SETTINGS_MODULE)
	@echo 'DJANGO_LOCAL_SETTINGS_MODULE:' $(DJANGO_LOCAL_SETTINGS_MODULE)
	@echo 'DJANGO_TEST_SETTINGS_MODULE:' $(DJANGO_TEST_SETTINGS_MODULE)

showenv.all: showenv showenv.virtualenv showenv.site

showenv.virtualenv: virtual_env_set
	PATH := $(VIRTUAL_ENV)/bin:$(PATH)
	export $(PATH)
	@echo 'VIRTUAL_ENV:' $(VIRTUAL_ENV)
	@echo 'PATH:' $(PATH)

showenv.site: site_set
	@echo 'SITE:' $(SITE)

collectstatic: virtual_env_set
	-mkdir -p .$(LOCALPATH)/static
	$(PYTHON_BIN)/django-admin.py collectstatic -c --noinput $(DJANGO_LOCAL_POSTFIX)

runserver: virtual_env_set
	$(PYTHON_BIN)/django-admin.py runserver $(DJANGO_LOCAL_POSTFIX)

syncdb: virtual_env_set
	$(PYTHON_BIN)/django-admin.py syncdb $(DJANGO_LOCAL_POSTFIX)

migratedb: virtual_env_set
	$(PYTHON_BIN)/django-admin.py migrate $(DJANGO_LOCAL_POSTFIX)

cmd: virtual_env_set
	$(PYTHON_BIN)/django-admin.py $(CMD) $(DJANGO_LOCAL_POSTFIX)

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf .coverage

test: clean virtual_env_set
	-$(PYTHON_BIN)/coverage run $(PYTHON_BIN)/django-admin.py test $(APP) $(DJANGO_TEST_POSTFIX)

coverage: virtual_env_set
	$(PYTHON_BIN)/coverage html --include="$(LOCALPATH)/*" --omit="*/admin.py,*/test*"

bootstrap: virtualenv pip virtual_env_set

pip: requirements.txt virtual_env_set
	pip install -r requirements.txt

virtualenv:
	virtualenv --no-site-packages $(VIRTUAL_ENV)
	echo $(VIRTUAL_ENV)

all: collectstatic refresh