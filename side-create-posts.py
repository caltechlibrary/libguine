# Generate Selenium IDE project file for batch creating blog posts.

# USAGE: python3 side-create-posts.py </path/to/csv> <name>

import csv
import json
import sys

from bs4 import BeautifulSoup

side_tests_wrapper = {
    "version": "2.0",
    "name": f"create-posts--{sys.argv[2]}",
    "url": "https://caltech.libapps.com",
    "tests": [],
    "suites": [],
    "urls": ["https://caltech.libapps.com/"],
    "plugins": [],
}

with open(sys.argv[1]) as posts:
    reader = csv.DictReader(posts)
    count = 0
    for post in reader:
        count += 1
        if post["subjects"]:
            chosen_subjects = []
            subjects = [s.strip() for s in post["subjects"].split(",")]
            for subject in subjects:
                chosen_subjects.extend(
                    [
                        {
                            "comment": "",
                            "command": "click",
                            "target": "xpath=//div[@id='tags_chosen']/ul/li/input",
                            "targets": [
                                [
                                    "xpath=//input[@value='Choose Subjects']",
                                    "xpath:attributes",
                                ],
                                [
                                    "xpath=//div[@id='tags_chosen']/ul/li/input",
                                    "xpath:idRelative",
                                ],
                            ],
                            "value": "",
                        },
                        {
                            "comment": "",
                            "command": "click",
                            "target": f"xpath=//div[@id='tags_chosen']/div/ul/li[contains(text(), '{subject}')]",
                            "targets": [
                                [
                                    f"xpath=//div[@id='tags_chosen']/div/ul/li[contains(text(), '{subject}')]",
                                    "xpath:idRelative",
                                ],
                                [
                                    "xpath=//div[2]/div/div/div/div/ul/li[contains(text(), '{subject}')]",
                                    "xpath:position",
                                ],
                            ],
                            "value": "",
                        },
                    ]
                )

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
                    "comment": "",
                    "command": "click",
                    "target": "css=a > .btn",
                    "targets": [
                        ["css=a > .btn", "css:finder"],
                        ["xpath=(//button[@type='button'])[2]", "xpath:attributes"],
                        ["xpath=//a/button", "xpath:position"],
                        ["xpath=//button[contains(.,' Add Post')]", "xpath:innerText"],
                    ],
                    "value": "",
                },
                {
                    "comment": "",
                    "command": "type",
                    "target": "id=title",
                    "targets": [
                        ["id=title", "id"],
                        ["name=title", "name"],
                        ["css=#title", "css:finder"],
                        ["xpath=//input[@id='title']", "xpath:attributes"],
                        [
                            "xpath=//div[@id='form-group-title']/div/input",
                            "xpath:idRelative",
                        ],
                        ["xpath=//div/input", "xpath:position"],
                    ],
                    "value": post["title"],
                },
                {
                    "comment": "",
                    "command": "selectFrame",
                    "target": "index=0",
                    "targets": [["index=0"]],
                    "value": "",
                },
                {
                    "comment": "",
                    "command": "click",
                    "target": "css=html",
                    "targets": [
                        ["css=html", "css:finder"],
                        ["xpath=//html", "xpath:position"],
                        ["xpath=//html[contains(.,'\n')]", "xpath:innerText"],
                    ],
                    "value": "",
                },
                {
                    "comment": "",
                    "command": "editContent",
                    "target": "css=.cke_editable",
                    "targets": [
                        ["css=.cke_editable", "css:finder"],
                        ["xpath=//body", "xpath:position"],
                        ["xpath=//body[contains(.,'post-wysiwyg')]", "xpath:innerText"],
                    ],
                    "value": BeautifulSoup(" ".join(post["body"].split()), "html.parser").prettify(),
                },
                {
                    "comment": "",
                    "command": "selectFrame",
                    "target": "relative=parent",
                    "targets": [["relative=parent"]],
                    "value": "",
                },
            ],
        }

        if chosen_subjects:
            side_test["commands"].extend(chosen_subjects)

        side_test["commands"].extend(
            [
                {
                    "comment": "",
                    "command": "select",
                    "target": "id=pub_opt",
                    "targets": [],
                    "value": "label=On a Date",
                },
                {
                    "comment": "",
                    "command": "type",
                    "target": "id=created",
                    "targets": [],
                    "value": post["date"],
                },
                {
                    "comment": "",
                    "command": "click",
                    "target": "id=s-lg-btn-edit-post",
                    "targets": [
                        ["id=s-lg-btn-edit-post", "id"],
                        ["css=#s-lg-btn-edit-post", "css:finder"],
                        ["xpath=//div[3]/div/button", "xpath:position"],
                        ["xpath=//button[contains(.,'Save Post')]", "xpath:innerText"],
                    ],
                    "value": "",
                },
            ]
        )

        side_tests_wrapper["tests"].append(side_test)

with open(f"assets/create-posts--{sys.argv[2]}.side", "w") as fp:
    json.dump(side_tests_wrapper, fp, indent=4)
