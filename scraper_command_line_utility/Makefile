.PHONY: coverage deploy lint publish push test
TMPDIR ?= $(shell mktemp -d)

package_name = scraper
source_dir = ${package_name}

coverage:  ## Run tests with coverage
	python -m coverage erase
	python -m coverage run --include=${source_dir}/* -m pytest -ra
	python -m coverage report -m

lint:  ## Lint and static-check
	python -m pylama

publish:  ## Publish to PyPi
	python -m flit publish

push:  ## Push code with tags
	git push && git push --tags

test :
	mkdir -p results/
	python -m pytest -ra

%.pyz :
	# Using the command-line entrypoint scrape-and-collect, defined in pyproject.toml
	shiv -o "$@" -c scrape-and-collect .

deploy : ${TMPDIR}/scrape-attack.pyz
	echo "Sending $< to ${DEPLOY_HOST}..." >&2
	rsync -brtu "$<" "${DEPLOY_HOST}:"
	rsync -brtu scraper/config/story_info/ "${DEPLOY_HOST}:scraper/config/story_info"

# TODO: is there maybe a 'retrieve' verb for this project?
