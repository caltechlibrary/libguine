#!/bin/sh

if [ "$#" -eq 0 ]; then
    echo "Usage: /bin/sh $0 FILE" >&2
    exit 0
elif [ "${1##*.}" = "html" ] || [ "${1##*.}" = "scss" ] || [ "${1##*.}" = "shtm" ]; then
    echo "TODO"
else
    echo "Skipping ${1}"
fi
