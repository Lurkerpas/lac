BLACK=black

.PHONY : check \
	all \
	install \
	check-format \
	format

all: check-format check

install:
	python3 -m pip install --user --upgrade .

check:
	python3 -m pytest tests
	${MAKE} -C integrationtests check 

check-format:
	${BLACK} --version
	${BLACK} --check lac
	${BLACK} --check tests

format:
	${BLACK} lac
	${BLACK} tests