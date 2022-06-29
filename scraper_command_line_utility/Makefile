.PHONY: coverage lint publish push test

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

../%.shiv :
	shiv -o "$@" -c scrape-and-collect .
