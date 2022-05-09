.PHONY: coverage lint publish push test

package_name = stationindex
source_dir = ${package_name}

# https://github.com/nalgeon/podsearcg-py/blob/main/Makefile
# via
# https://antonz.org/python-packaging/

coverage:  ## Run tests with coverage
	python -m coverage erase
	#python -m coverage run --include=${source_dir}/* -m pytest -ra
	# Tests require input:
	[ -t 0 ] && python -m coverage run --include=${source_dir}/* -m pytest -s
	python -m coverage report -m

lint:  ## Lint and static-check
	python -m pylama

publish:  ## Publish to PyPi
	python -m flit publish

push:  ## Push code with tags
	git push && git push --tags

test :
	mkdir -p results/
	#python -m pytest -ra
	# Tests require input:
	[ -t 0 ] && python -m pytest --junit-xml=results/pytest.xml -s

	# tests/run-bats tests --report-formatter junit -o results/
	[ -t 0 ] && tests/run-bats tests --report-formatter junit -o results/

