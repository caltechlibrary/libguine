import sys

import arrow
import bleach
import feedparser

from bs4 import BeautifulSoup

if len(sys.argv) == 1:
    raise RuntimeError("❓ MISSING ARGUMENT: LIBCAL_RSS_NOTICES_TODAY_URL")

notices = feedparser.parse(sys.argv[1])
import pprint
pprint.pprint(notices.entries)


def construct_bootstrap_alert(entry):
    # wrap description in a div initially for ease in working with soup
    soup = BeautifulSoup(
        f'<div>{bleach.clean(entry["libcal_description"], tags=["a", "b", "code", "em", "i", "span", "strong"], attributes={"a": ["href"], "span": ["class"]}, strip=True)}</div>',
        "html.parser",
    )
    level = entry["libcal_location"].split()[-1].lower()
    # wrap with bootstrap 3 alert markup
    soup.div.wrap(
        soup.new_tag("div", attrs={"class": "alert alert-dismissible", "role": "alert"})
    )
    soup.div["class"].append(f"alert-{level}")
    soup.div.div.insert_before(
        soup.new_tag(
            "button",
            attrs={
                "aria-label": "Close",
                "class": "close",
                "data-dismiss": "alert",
                "type": "button",
            },
        )
    )
    soup.div.div.insert_after("\n")  # prettify
    soup.button.insert_before("\n  ")  # prettify
    soup.button.append(soup.new_tag("span", attrs={"aria-hidden": "true"}))
    soup.button.span.append("×")
    soup.button.insert_after("\n  ")  # prettify
    # there will not always be links in the description
    if soup.a:
        soup.a["class"] = "alert-link"
    # remove the helper div around description
    soup.div.div.unwrap()
    return str(soup)


# split library and archives notices into separate lists
archives_entries = []
library_entries = []
for entry in notices.entries:
    locations = entry["libcal_location"].split(", ")
    for location in locations:
        if "Archives" in location:
            entry["libcal_location"] = location
            archives_entries.append(entry)
        if "Library" in location:
            entry["libcal_location"] = location
            library_entries.append(entry)


def evaluate_entry(entry):
    # create date/time/tz string from feed entry elements
    datetimetz_string = (
        f'{entry["libcal_date"]} {entry["libcal_end"]} America/Los_Angeles'
    )
    # GitHub Actions runners are on UTC
    if arrow.get(datetimetz_string, "YYYY-MM-DD HH:mm:ss ZZZ") > arrow.now():
        # proceed when the end time is still in the future
        return construct_bootstrap_alert(entry) + "\n"  # prettify
    else:
        return


with open("fragments/notices/archives.html", "w") as fp:
    if archives_entries:
        for entry in archives_entries:
            fp.write(evaluate_entry(entry))
    else:
        fp.write("<!-- NO NOTICES -->")

with open("fragments/notices/library.html", "w") as fp:
    if library_entries:
        for entry in library_entries:
            fp.write(evaluate_entry(entry))
    else:
        fp.write("<!-- NO NOTICES -->")
