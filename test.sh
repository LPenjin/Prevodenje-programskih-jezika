#/bin/bash

LAB=Lab2

cd ${LAB}

for DIR in $(ls -d test_primjeri_laksi/*); do
  OUTPUT="$(cat ${DIR}/test.in | python3 SintaksniAnalizator.py)"
  DIFF="$( diff ${DIR}/test.out <(echo "$OUTPUT") )"
  if [[ ${DIFF} != "" ]]; then
    echo "${DIR}"
    echo "${DIFF}"
    exit 1
  else
    echo "${DIR} is fine."
  fi
done

exit 1

