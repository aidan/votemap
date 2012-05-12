MONGOD_DB_PATH=`pwd`/runtime/mongod_db
MONGOD_PORT=27023

.PHONY: all test run rundb run-mongo  \
	coverage clean pep8 pyflakes check

all:
	@echo 'run-mongo      mongodb, required to run votemap locally'
	@echo 'test           run the unit tests'
	@echo 'coverage       generate coverage statistics'
	@echo 'pep8           check pep8 compliance'
	@echo 'pyflakes       check for unused imports (requires pyflakes)'
	@echo 'check          make sure you are ready to commit'
	@echo 'apidocs        generate and display the web API documentation'
	@echo 'clean          cleanup the source tree'

test: clean_coverage
	@echo 'Running all tests...'
	@VERBOSE=1 ./run_tests.sh

run: run-votemap
run-votemap:
	python main.py --debug

rundb: run-mongo
run-mongo:
	@mkdir -p $(MONGOD_DB_PATH)
	@mongod --dbpath $(MONGOD_DB_PATH) --port $(MONGOD_PORT)

runall:
	@make rundb &
	@make run

testdata:
	python make_test_data.py

clean_coverage:
	@rm -f .coverage

coverage:
	@echo 'Generating coverage statistics html...'
	@coverage html -d coverage_html --include=votemap/* --omit=votemap/tests/* --omit=*.txt,*.json

clean: clean_coverage
	@echo 'Cleaning...'
	@find . -name "*.pyc" -exec rm -f {} \;
	@echo 'Done.'

pep8:
	@echo 'Checking pep8 compliance...'
	@pep8 main.py votemap

pyflakes:
	@echo 'Running pyflakes...'
	@pyflakes main.py votemap

check: pep8 pyflakes test
	@grep ^TOTAL tests_output/test.log | grep 100% >/dev/null || \
	{ echo 'Unit tests coverage is incomplete.'; exit 1; }
