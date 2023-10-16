LAC = PYTHONPATH=../ python3 -m lac.lac
CC=gcc

TEST_DIR=out
TMPLT_DIR=../data

CREATE_EMPTY_TEST_DIR=rm -r -f ${TEST_DIR} && mkdir -p ${TEST_DIR}
CLEAN_TEST_DIR=rm -r -f ${TEST_DIR}

TESTS = \
	basic_types_c \
	basic_types_py \
	complex_types_c \
	complex_types_py

.SILENT : \
	${TESTS}

.PHONY : \
	${TESTS} \
	check

check: ${TESTS}

basic_types_c:
	echo "Basic Types C"
	${CREATE_EMPTY_TEST_DIR}
	${LAC} -t ${TMPLT_DIR}/cheader.mako -o ${TEST_DIR} -e c basic_types.asn basic_types.acn

basic_types_py:
	echo "Basic Types Python"
	${CREATE_EMPTY_TEST_DIR}
	${LAC} -t ${TMPLT_DIR}/python.mako -o ${TEST_DIR} -e py basic_types.asn basic_types.acn
	 

complex_types_c:
	echo "Complex Types C"
	${CREATE_EMPTY_TEST_DIR}
	${LAC} -t ${TMPLT_DIR}/cheader.mako -o ${TEST_DIR} -e c complex_types.asn complex_types.acn
	${CC} -c ${TEST_DIR}/Test.c -o ${TEST_DIR}/Test.o
	
complex_types_py:
	echo "Complex Types Python"
	${CREATE_EMPTY_TEST_DIR}
	${LAC} -t ${TMPLT_DIR}/python.mako -o ${TEST_DIR} -e py complex_types.asn complex_types.acn
	