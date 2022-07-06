# Generate Selenium IDE project file for batch deleting blog posts.

# USAGE: python3 side-delete-posts.py <count> "<tag>"

import csv
import json
import sys

side_tests_wrapper = {
    "version": "2.0",
    "name": "delete-posts",
    "url": "https://caltech.libapps.com",
    "tests": [],
    "suites": [],
    "urls": ["https://caltech.libapps.com/"],
    "plugins": [],
}

count = int(sys.argv[1])
while count:
    side_test = {
        "name": f"post-{str(count).zfill(3)}",
        "commands": [
            {
                "comment": "",
                "command": "open",
                "target": "/libguides/blog.php",
                "targets": [],
                "value": "",
            },
            {
                "comment": "",
                "command": "setWindowSize",
                "target": "1200x960",
                "targets": [],
                "value": "",
            },
            {
                f"comment": f"click {sys.argv[2]} tag link",
                "command": "click",
                "target": f"xpath=//div[@id='s-lg-blog-content']/div/div[2]/div[6]/a[contains(text(),'{sys.argv[2]}')]",
                "targets": [
                    [
                        f"xpath=//div[@id='s-lg-blog-content']/div/div[2]/div[6]/a[contains(text(),'{sys.argv[2]}')]",
                        "xpath:idRelative",
                    ],
                ],
                "value": "",
            },
            {
                "comment": "click top post cog icon",
                "command": "click",
                "target": "xpath=//div[@id='s-lg-blog-posts']/div[3]/div/div/button",
                "targets": [
                    ["css=.row:nth-child(5) .btn", "css:finder"],
                    ["xpath=(//button[@type='button'])[3]", "xpath:attributes"],
                    [
                        "xpath=//div[@id='s-lg-blog-posts']/div[3]/div/div/button",
                        "xpath:idRelative",
                    ],
                    ["xpath=//div[3]/div/div/button", "xpath:position"],
                ],
                "value": "",
            },
            {
                "comment": "click Delete under cog icon",
                "command": "click",
                "target": "css=.open .fa-trash-o",
                "targets": [
                    ["css=.open .fa-trash-o", "css:finder"],
                    [
                        "xpath=//div[@id='s-lg-blog-posts']/div[4]/div/div/ul/li[3]/a/i",
                        "xpath:idRelative",
                    ],
                    ["xpath=//div[4]/div/div/ul/li[3]/a/i", "xpath:position"],
                ],
                "value": "",
            },
            {
                "comment": "click understand checkbox",
                "command": "click",
                "target": "css=.checkbox",
                "targets": [
                    ["css=.checkbox", "css:finder"],
                    [
                        "xpath=//div[@id='s-lib-alert-content']/label",
                        "xpath:idRelative",
                    ],
                    ["xpath=//div[4]/div[2]/div/label", "xpath:position"],
                    [
                        "xpath=//label[contains(.,' I understand that this cannot be undone.')]",
                        "xpath:innerText",
                    ],
                ],
                "value": "",
            },
            {
                "comment": "click Delete button",
                "command": "click",
                "target": "id=s-lib-alert-btn-first",
                "targets": [
                    ["id=s-lib-alert-btn-first", "id"],
                    ["css=#s-lib-alert-btn-first", "css:finder"],
                    ["xpath=//button[@id='s-lib-alert-btn-first']", "xpath:attributes"],
                    ["xpath=//div[3]/div/button", "xpath:position"],
                    [
                        "xpath=//button[contains(.,'Delete it - I mean it!')]",
                        "xpath:innerText",
                    ],
                ],
                "value": "",
            },
        ],
    }
    side_tests_wrapper["tests"].append(side_test)
    count -= 1

with open("assets/delete-posts--archives.side", "w") as fp:
    json.dump(side_tests_wrapper, fp, indent=4)
