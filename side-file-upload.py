# Generate Selenium IDE project file for batch uploading to the Image Manager.

# USAGE: python3 side-file-upload.py /path/to/files [folder-keywords]
#
# The optional `folder-keywords` string will be used to create a folder in the
# Image Manager as well as a suffix for existing filenames.

import json
import mimetypes
import re
import shutil
import sys
import tempfile

from pathlib import Path

side_tests_wrapper = {
    "version": "2.0",
    "name": "file-upload",
    "url": "https://caltech.libapps.com",
    "tests": [],
    "suites": [],
    "urls": ["https://caltech.libapps.com/"],
    "plugins": [],
}

for p in Path(sys.argv[1]).glob("*"):

    if not mimetypes.guess_type(p)[0]:
        continue
    elif not mimetypes.guess_type(p)[0].startswith("image"):
        continue

    if re.search(r"[^\w.-]", p.name):
        print(f"‼️ unsafe filename: {p.name}")

    if sys.argv[2]:
        tmp = Path(f"{tempfile.gettempdir()}").joinpath(sys.argv[2])
        tmp.mkdir(parents=True, exist_ok=True)
        filepath = str(tmp.joinpath(f"{p.stem}--{sys.argv[2]}{p.suffix}"))
        shutil.copy(str(p.resolve()), filepath)
    else:
        filepath = str(p.resolve())

    side_test = {
        "name": p.name,
        "commands": [
            {
                "comment": "",
                "command": "open",
                "target": "/libapps/image_manager.php",
                "targets": [],
                "value": "",
            },
            {
                "comment": "",
                "command": "setWindowSize",
                "target": "1280x800",
                "targets": [],
                "value": "",
            },
            {
                "comment": "",
                "command": "click",
                "target": "id=label-library_type_1",
                "targets": [
                    ["id=label-library_type_1", "id"],
                    ["css=#label-library_type_1", "css:finder"],
                    ["xpath=//label[@id='label-library_type_1']", "xpath:attributes"],
                    [
                        "xpath=//div[@id='btn-group-library_type']/label[2]",
                        "xpath:idRelative",
                    ],
                    ["xpath=//label[2]", "xpath:position"],
                    ["xpath=//label[contains(.,'Shared Library')]", "xpath:innerText"],
                ],
                "value": "",
            },
            {
                "comment": "",
                "command": "if",
                "target": f"linkText='{sys.argv[2]}'",
                "targets": [],
                "value": "",
            },
            {
                "comment": "",
                "command": "click",
                "target": f"linkText={sys.argv[2]}",
                "targets": [
                    [f"linkText={sys.argv[2]}", "linkText"],
                    [f"xpath=//a[contains(text(),'{sys.argv[2]}')]", "xpath:link"],
                    [f"xpath=//a[contains(.,'{sys.argv[2]}')]", "xpath:innerText"],
                ],
                "value": "",
            },
            {"comment": "", "command": "end", "target": "", "targets": [], "value": ""},
            {
                "comment": "",
                "command": "click",
                "target": "css=#s-lg-img-mgr-upload-container .fileupload .fileupload-new",
                "targets": [
                    [
                        "css=#s-lg-img-mgr-upload-container .fileupload .fileupload-new",
                        "css:finder",
                    ],
                    [
                        "xpath=//span[@id='fileupload']/div/div/div/label/span",
                        "xpath:idRelative",
                    ],
                    ["xpath=//label/span", "xpath:position"],
                ],
                "value": "",
            },
            {
                "comment": "",
                "command": "type",
                "target": "id=file_upload",
                "targets": [
                    ["id=file_upload", "id"],
                    ["name=file_upload", "name"],
                    ["css=.btn:nth-child(2) > #file_upload", "css:finder"],
                    ["xpath=//input[@id='file_upload']", "xpath:attributes"],
                    [
                        "xpath=//span[@id='fileupload']/div/div/div/label/input",
                        "xpath:idRelative",
                    ],
                    ["xpath=//div/div/div/label/input", "xpath:position"],
                ],
                "value": filepath,
            },
            {
                "comment": "",
                "command": "click",
                "target": "id=label-library_type_1",
                "targets": [
                    ["id=label-library_type_1", "id"],
                    ["css=#label-library_type_1", "css:finder"],
                    ["xpath=//label[@id='label-library_type_1']", "xpath:attributes"],
                    [
                        "xpath=//div[@id='btn-group-library_type']/label[2]",
                        "xpath:idRelative",
                    ],
                    ["xpath=//label[2]", "xpath:position"],
                    ["xpath=//label[contains(.,'Shared Library')]", "xpath:innerText"],
                ],
                "value": "",
            },
        ],
    }

    side_tests_wrapper["tests"].append(side_test)

with open("assets/file-upload.side", "w") as fp:
    json.dump(side_tests_wrapper, fp, indent=4)
