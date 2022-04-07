#!/bin/sh

if [ "$#" -ne 2 ]; then
    echo "Usage: /bin/sh $0 TYPE GROUP" >&2
    exit 1
fi

if [ "$1" = "header" ]; then
    # shellcheck disable=SC1111
    instructions=$(printf "  Copy and paste the contents of this file into the “Group Header” section of\n  the “Header / Footer / Tabs / Boxes” tab when editing the appropriate group.")
    if [ -f "header-wrapper.html" ]; then
        wrapper="header-wrapper.html"
    else
        echo "file header-wrapper.html does not exist"
        exit 1
    fi
    if [ -f "header-top-${2}.html" ]; then
        include=$(cat "header-top-${2}.html")
        asset="assets/header-${2}.html"
        printf "" > "$asset"
    else
        echo "snippet header-top-${2}.html does not exist"
        exit 1
    fi
else
    echo "no support for TYPE ${1}"
    exit 1
fi

while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
        *"Last Modified:"*)
            printf '%s\n' "  Last Modified: $(date '+%Y-%m-%d %H:%M:%S')" >> "$asset"
        ;;
        *"Run '/bin/sh build.sh"*)
            printf "%s\n" "$instructions" >> "$asset"
        ;;
        *"<!--#include"*)
            printf '%s\n' "$include" >> "$asset"
        ;;
        *"<!--end-->"*)
            printf '%s\n' "<!--end ${1} ${2}-->" >> "$asset"
        ;;
        *)
            printf '%s\n' "$line" >> "$asset"
        ;;
    esac
done < "$wrapper"
