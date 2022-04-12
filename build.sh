#!/bin/sh

if [ "$#" -ne 2 ]; then
    echo "Usage: /bin/sh $0 TYPE GROUP" >&2
    exit 1
fi

if [ "$1" = "head" ]; then
    # shellcheck disable=SC1111
    instructions=$(printf "  Copy and paste the contents of this file into the “Public Pages Header/Footer\n  Customization” section of the “Custom JS/CSS Code” tab when editing the\n  appropriate group.")
    if [ -f "head-wrapper.html" ]; then
        wrapper="head-wrapper.html"
    else
        echo "file head-wrapper.html does not exist"
        exit 1
    fi
    asset="assets/head-${2}.html"
    printf "" > "$asset"
elif [ "$1" = "header" ]; then
    # shellcheck disable=SC1111
    instructions=$(printf "  Copy and paste the contents of this file into the “Group Header” section of\n  the “Header / Footer / Tabs / Boxes” tab when editing the appropriate group.")
    if [ -f "header-wrapper.html" ]; then
        wrapper="header-wrapper.html"
    else
        echo "file header-wrapper.html does not exist"
        exit 1
    fi
    if [ -f "header-top-${2}.html" ]; then
        include1=$(cat "header-top-${2}.html")
    else
        echo "snippet header-top-${2}.html does not exist"
        exit 1
    fi
    asset="assets/header-${2}.html"
    printf "" > "$asset"
elif [ "$1" = "footer" ]; then
    # shellcheck disable=SC1111
    instructions=$(printf "  Copy and paste the contents of this file into the “Group Footer” section of\n  the “Header / Footer / Tabs / Boxes” tab when editing the appropriate group.")
    if [ -f "footer-wrapper.html" ]; then
        wrapper="footer-wrapper.html"
    else
        echo "file footer-wrapper.html does not exist"
        exit 1
    fi
    if [ -f "footer-contact-${2}.html" ]; then
        include1=$(cat "footer-contact-${2}.html")
    else
        echo "snippet footer-contact-${2}.html does not exist"
        exit 1
    fi
    if [ -f "footer-org-${2}.html" ]; then
        include2=$(cat "footer-org-${2}.html")
    else
        echo "snippet footer-org-${2}.html does not exist"
        exit 1
    fi
    asset="assets/footer-${2}.html"
    printf "" > "$asset"
else
    echo "no support for TYPE ${1}"
    exit 1
fi

while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
        "<!--begin"*)
            printf '%s\n' "<!--begin ${1} ${2}" >> "$asset"
        ;;
        *"Last Modified:"*)
            printf '%s\n' "  Last Modified: $(date '+%Y-%m-%d %H:%M:%S')" >> "$asset"
        ;;
        *"Run '/bin/sh build.sh"*)
            printf "%s\n" "$instructions" >> "$asset"
        ;;
        *"<!--#include1"*)
            printf '%s\n' "$include1" >> "$asset"
        ;;
        *"<!--#include2"*)
            printf '%s\n' "$include2" >> "$asset"
        ;;
        *"<!--end-->"*)
            printf '%s\n' "<!--end ${1} ${2}-->" >> "$asset"
        ;;
        *)
            printf '%s\n' "$line" >> "$asset"
        ;;
    esac
done < "$wrapper"
