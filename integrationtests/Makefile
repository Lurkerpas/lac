LAC = PYTHONPATH=../ python3 -m lac.lac
CC=gcc

TEST_DIR=out
TMPLT_DIR=../data

CREATE_EMPTY_TEST_DIR=rm -r -f ${TEST_DIR} && mkdir -p ${TEST_DIR}
CLEAN_TEST_DIR=rm -r -f ${TEST_DIR}

TESTS = \
	basic_types

.SILENT : \
	${TESTS}

.PHONY : \
	${TESTS} \
	check

check: ${TESTS}

basic_types:
	echo "Basic Types"
	${CREATE_EMPTY_TEST_DIR}
	${LAC} -t ${TMPLT_DIR}/cheader.mako -o ${TEST_DIR} -e c basic_types.asn basic_types.acn
	${CC} -c ${TEST_DIR}/Test.c -o ${TEST_DIR}/Test.o 
	${CLEAN_TEST_DIR}