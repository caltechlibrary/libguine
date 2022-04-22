#!/bin/sh

if [ "$#" -eq 0 ]; then
    echo "Usage: /bin/sh $0 TYPE [GROUP]" >&2
    exit 1
elif [ "$#" -eq 1 ]; then
    # set default arguments as groups to use when no GROUP is specified
    set "$1" archives dev
fi

wrapper_type="$1"
# shift will remove $1 and shift remaining arguments in its place
shift
# for without in will loop over arguments
for group; do
    if [ "$wrapper_type" = "head" ]; then
        # shellcheck disable=SC1111
        instructions=$(printf "  Copy and paste the contents of this file into the “Public Pages Header/Footer\n  Customization” section of the “Custom JS/CSS Code” tab when editing the\n  appropriate group.")
        if [ -f "head-wrapper.html" ]; then
            wrapper_file="head-wrapper.html"
        else
            echo "file head-wrapper.html does not exist"
            exit 1
        fi
        asset="assets/head-${group}.html"
        printf "" > "$asset"
    elif [ "$wrapper_type" = "header" ]; then
        # shellcheck disable=SC1111
        instructions=$(printf "  Copy and paste the contents of this file into the “Group Header” section of\n  the “Header / Footer / Tabs / Boxes” tab when editing the appropriate group.")
        if [ -f "header-wrapper.html" ]; then
            wrapper_file="header-wrapper.html"
        else
            echo "file header-wrapper.html does not exist"
            exit 1
        fi
        if [ -f "header-top-${group}.html" ]; then
            include1=$(cat "header-top-${group}.html")
        else
            echo "snippet header-top-${group}.html does not exist"
            exit 1
        fi
        asset="assets/header-${group}.html"
        printf "" > "$asset"
    elif [ "$wrapper_type" = "footer" ]; then
        # shellcheck disable=SC1111
        instructions=$(printf "  Copy and paste the contents of this file into the “Group Footer” section of\n  the “Header / Footer / Tabs / Boxes” tab when editing the appropriate group.")
        if [ -f "footer-wrapper.html" ]; then
            wrapper_file="footer-wrapper.html"
        else
            echo "file footer-wrapper.html does not exist"
            exit 1
        fi
        if [ -f "footer-contact-${group}.html" ]; then
            include1=$(cat "footer-contact-${group}.html")
        else
            echo "snippet footer-contact-${group}.html does not exist"
            exit 1
        fi
        if [ -f "footer-org-${group}.html" ]; then
            include2=$(cat "footer-org-${group}.html")
        else
            echo "snippet footer-org-${group}.html does not exist"
            exit 1
        fi
        asset="assets/footer-${group}.html"
        printf "" > "$asset"
    else
        echo "no support for TYPE ${wrapper_type}"
        exit 1
    fi

    while IFS= read -r line || [ -n "$line" ]; do
        case "$line" in
            "<!--begin"*)
                printf '%s\n' "<!--begin ${wrapper_type} ${group}" >> "$asset"
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
                printf '%s\n' "<!--end ${wrapper_type} ${group}-->" >> "$asset"
            ;;
            *)
                printf '%s\n' "$line" >> "$asset"
            ;;
        esac
    done < "$wrapper_file"
done

