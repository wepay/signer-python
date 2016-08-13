all:
	@cat Makefile | grep : | grep -v PHONY | grep -v @ | sed 's/:/ /' | awk '{print $$1}' | sort

#-------------------------------------------------------------------------------

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: activate
activate:
	$$(which bash) -c "source vendor/bin/activate"

.PHONY: deactivate
deactivate:
	deactivate

.PHONY: lint
lint:
	autopep8 --max-line-length 120 --in-place **/*.py
	autoflake --in-place --remove-unused-variables **/*.py
	for py in $$(ls **/*.py); do pylint --rcfile .pylint $$py; done;

.PHONY: test
test:
	pip install -e .
	nose2

#-------------------------------------------------------------------------------

.PHONY: docs
docs:

.PHONY: pushdocs
pushdocs: docs
	rm -Rf /tmp/gh-pages
	git clone git@github.devops.wepay-inc.com:devtools/datacenter.git --branch gh-pages --single-branch /tmp/gh-pages
	cp -Rf ./docs/* /tmp/gh-pages/
	cd /tmp/gh-pages/ && git add . && git commit -a -m "Automated commit on $$(date)" && git push origin gh-pages

#-------------------------------------------------------------------------------

.PHONY: buildpip
build:
	python setup.py sdist
	python setup.py bdist_wheel

.PHONY: readme
readme:
	pandoc -r markdown_github -w rst -o README.rst README.md

.PHONY: pushpip
push:
	twine upload dist/*

.PHONY: tag
tag:
	@ if [ $$(git status -s -uall | wc -l) != 0 ]; then echo 'ERROR: Git workspace must be clean.'; exit 1; fi;

	@echo "This release will be tagged as: $$(cat ./VERSION)"
	@echo "This version should match your gem. If it doesn't, re-run 'make gem'."
	@echo "---------------------------------------------------------------------"
	@read -p "Press any key to continue, or press Control+C to cancel. " x;

	git add .
	git commit -a -m "Preparing the $$(cat ./VERSION) release."
	git tag $$(cat ./VERSION)

#-------------------------------------------------------------------------------

.PHONY: version
version:
	@echo "Current version: $$(cat ./VERSION)"
	@read -p "Enter new version number: " nv; \
	printf "$$nv" > ./VERSION

.PHONY: clean
clean:
	rm -Rf **/*.pyc **/__pycache__ build/ dist/ docs/ *.egg-info/
