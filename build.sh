#!/bin/sh

if [ "$#" -eq 0 ]; then
    echo "Usage: /bin/sh $0 WRAPPER_TYPE [GROUP]" >&2
    exit 1
elif [ "$#" -eq 1 ]; then
    # set default arguments as groups to use when no GROUP is specified
    set "$1" archives dev
fi

# FUNCTIONS
analyze_include() {
    # $1 - include line
    # $2 - group key
    # $3 - asset file
    case "$1" in
        *"--GROUP.shtm' -->")
            # replace GROUP to construct the appropriate filename
            included_group_file="$(echo "$1" | cut -d\' -f2 | sed "s/GROUP/${2}/")"
            # loop over every line in the group file
            process_included_file_lines "$included_group_file" "$2" "$3"
        ;;
        *"--GROUP.html' -->")
            # replace GROUP to construct the appropriate filename
            included_group_file="$(echo "$1" | cut -d\' -f2 | sed "s/GROUP/${2}/")"
            # append the contents of the group file to the asset file
            printf '%s\n' "$(cat "${included_group_file}")" >> "$3"
        ;;
        *".html' -->")
            # get the filename from the include statement
            included_file=$(echo "$1" | cut -d\' -f2)
            # append the contents of the included file to the asset file
            printf '%s\n' "$(cat "${included_file}")" >> "$3"
        ;;
    esac
}
process_included_file_lines() {
    # $1 - included file
    # $2 - group key
    # $3 - asset file
    while IFS= read -r line || [ -n "$line" ]; do
        case "$line" in
            *"<!--#include"*)
                # analyze the found include statement
                analyze_include "$line" "$2" "$3"
            ;;
            *)
                # append this line to the asset file
                printf '%s\n' "$line" >> "$3"
            ;;
        esac
    done < "$1"
}

wrapper_type="$1"
# remove $1 and decrement the variable for each remaining argument
shift
# `for` statement without `in` will loop over arguments
for group; do
    if [ "$wrapper_type" = "header" ]; then
        # shellcheck disable=SC1111
        instructions=$(printf "  Copy and paste the contents of this file into the “Group Header” section of\n  the “Header / Footer / Tabs / Boxes” tab when editing the appropriate group.")
        if [ -f "header.shtm" ]; then
            wrapper_file="header.shtm"
        else
            echo "file header.shtm does not exist"
            exit 1
        fi
        asset="assets/header--${group}.html"
        printf "" > "$asset"
    elif [ "$wrapper_type" = "footer" ]; then
        # shellcheck disable=SC1111
        instructions=$(printf "  Copy and paste the contents of this file into the “Group Footer” section of\n  the “Header / Footer / Tabs / Boxes” tab when editing the appropriate group.")
        if [ -f "footer.shtm" ]; then
            wrapper_file="footer.shtm"
        else
            echo "file footer.shtm does not exist"
            exit 1
        fi
        asset="assets/footer--${group}.html"
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
            *"<!--#include"*)
                analyze_include "$line" "$group" "$asset"
            ;;
            *"<!--end"*)
                printf '%s\n' "<!--end ${wrapper_type} ${group}-->" >> "$asset"
            ;;
            *)
                printf '%s\n' "$line" >> "$asset"
            ;;
        esac
    done < "$wrapper_file"
done

