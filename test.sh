#/bin/bash

LAB=Lab1

cd ${LAB}

for DIR in $(ls -d test_primjeri/*); do
  cat ${DIR}/test.lan | python3 GLA.py 1>/dev/null && OUTPUT="$(cat ${DIR}/test.in | python3 analizator/LA.py)"
  DIFF="$( diff ${DIR}/test.out <(echo "$OUTPUT") )"
  if [[ ${DIFF} != "" ]]; then
    echo "${DIR}"
    echo "${DIFF}"
  else
    echo "${DIR} is fine."
  fi
done

exit 1

