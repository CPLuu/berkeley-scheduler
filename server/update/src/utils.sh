#!/usr/bin/env bash

TERM='spring-2017'
TERM_ABBRV='sp17'


PROJECT_DIR=$(cd $(dirname ${BASH_SOURCE[0]})/../../.. && pwd )
CREDENTIALS_DIR=$(cd ${PROJECT_DIR}/server/.credentials && pwd )
SERVER_DIR=$(cd ${PROJECT_DIR}/server/update && pwd )


SRC_DIR=${SERVER_DIR}/src

INPUT_DEPARTMENTS_DIR=${SERVER_DIR}/data/intermediate/departments
INPUT_CLASSES_DIR=${INPUT_DEPARTMENTS_DIR}/class-listing-by-subject-area-${TERM}
INPUT_CLASSES_TERM_DIR=${INPUT_DEPARTMENTS_DIR}/class-listing-by-subject-area-${TERM}
INPUT_INDICES_DIR=${INPUT_DEPARTMENTS_DIR}/indices-${TERM}

OUTPUT_DEPARTMENTS_DIR=${PROJECT_DIR}/data
OUTPUT_CLASSES_DIR=${OUTPUT_DEPARTMENTS_DIR}/${TERM_ABBRV}/classes
OUTPUT_INDICES_DIR=${OUTPUT_DEPARTMENTS_DIR}/${TERM_ABBRV}/indices

RECOVER_DIR=${SERVER_DIR}/data/recover
RECOVER_CLASSES_DIR=${RECOVER_DIR}/classes
RECOVER_INDICES_DIR=${RECOVER_DIR}/indices
