#!/bin/sh

if [ "$#" -eq 0 ]; then
    echo "Usage: /bin/sh $0 FILE" >&2
    exit 0
elif [ "${FILE##*.}" = "html" ] || [ "${FILE##*.}" = "scss" ] || [ "${FILE##*.}" = "shtm" ]; then
    echo "TODO"
else
    echo "Skipping ${FILE}"
fi
