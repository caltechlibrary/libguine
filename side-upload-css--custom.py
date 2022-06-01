# Generate Selenium IDE project file for uploading a custom CSS file.

# USAGE: python3 side-upload-css--custom.py

import json

from pathlib import Path

from decouple import config

slug = "upload-css--custom"
filepath = str(Path("assets/custom.css").resolve())

side_tests_wrapper = {
    "id": "b5ca31b1-18e3-4f09-bb46-58911b663ebc",
    "version": "2.0",
    "name": slug,
    "url": "https://caltech.libapps.com",
    "tests": [],
    "suites": [
        {
            "id": "3451be93-aef3-45d4-874e-559eeb320132",
            "name": "dev",
            "persistSession": False,
            "parallel": False,
            "timeout": 300,
            "tests": ["71c7a101-ecf6-42dc-a56e-7ff002076244"],
        }
    ],
    "urls": ["https://caltech.libapps.com/"],
    "plugins": [],
}

side_test = {
    "id": "71c7a101-ecf6-42dc-a56e-7ff002076244",
    "name": slug,
    "commands": [
        {
            "id": "a11b0406-0302-4190-a2e8-bb6c35dc166b",
            "comment": "",
            "command": "open",
            "target": "/libapps/login.php",
            "targets": [],
            "value": "",
        },
        {
            "id": "17aaabc0-7587-4058-bf20-20cf862bc41e",
            "comment": "",
            "command": "setWindowSize",
            "target": "1280x800",
            "targets": [],
            "value": "",
        },
        {
            "id": "7bdd28a4-c07d-4bb8-a53e-c346277f9542",
            "comment": "",
            "command": "storeXpathCount",
            "target": "xpath=//input[@id='s-libapps-email']",
            "targets": [],
            "value": "login",
        },
        {
            "id": "4f890956-a08f-4003-be4b-b1dd3e2116a3",
            "comment": "",
            "command": "if",
            "target": "${login}>0",
            "targets": [],
            "value": "",
        },
        {
            "id": "5b7498fc-c86e-4301-ae3c-5995be9df39a",
            "comment": "",
            "command": "click",
            "target": "id=s-libapps-email",
            "targets": [
                ["id=s-libapps-email", "id"],
                ["name=s-libapps-email", "name"],
                ["css=#s-libapps-email", "css:finder"],
                ["xpath=//input[@id='s-libapps-email']", "xpath:attributes"],
                [
                    "xpath=//form[@id='s-libapps-login-form']/div[2]/input",
                    "xpath:idRelative",
                ],
                ["xpath=//div[2]/input", "xpath:position"],
            ],
            "value": "",
        },
        {
            "id": "37dd3f4e-37e1-4a9d-b7f8-8e4fbffe07d2",
            "comment": "",
            "command": "type",
            "target": "id=s-libapps-email",
            "targets": [
                ["id=s-libapps-email", "id"],
                ["name=s-libapps-email", "name"],
                ["css=#s-libapps-email", "css:finder"],
                ["xpath=//input[@id='s-libapps-email']", "xpath:attributes"],
                [
                    "xpath=//form[@id='s-libapps-login-form']/div[2]/input",
                    "xpath:idRelative",
                ],
                ["xpath=//div[2]/input", "xpath:position"],
            ],
            "value": config("LIBAPPS_USER"),
        },
        {
            "id": "2500ccc5-ea45-4726-bc95-18da97b2e639",
            "comment": "",
            "command": "type",
            "target": "id=s-libapps-password",
            "targets": [
                ["id=s-libapps-password", "id"],
                ["name=s-libapps-password", "name"],
                ["css=#s-libapps-password", "css:finder"],
                ["xpath=//input[@id='s-libapps-password']", "xpath:attributes"],
                [
                    "xpath=//form[@id='s-libapps-login-form']/div[3]/input",
                    "xpath:idRelative",
                ],
                ["xpath=//div[3]/input", "xpath:position"],
            ],
            "value": config("LIBAPPS_PASS"),
        },
        {
            "id": "1ade3120-9591-4a8d-a6de-4cb0bf30986a",
            "comment": "",
            "command": "click",
            "target": "id=s-libapps-login-button",
            "targets": [
                ["id=s-libapps-login-button", "id"],
                ["css=#s-libapps-login-button", "css:finder"],
                ["xpath=//button[@id='s-libapps-login-button']", "xpath:attributes"],
                [
                    "xpath=//form[@id='s-libapps-login-form']/div[4]/button",
                    "xpath:idRelative",
                ],
                ["xpath=//button", "xpath:position"],
                ["xpath=//button[contains(.,'Log Into LibApps')]", "xpath:innerText"],
            ],
            "value": "",
        },
        {
            "id": "43daca78-0cb9-48c7-8517-56910c6fdd32",
            "comment": "",
            "command": "end",
            "target": "",
            "targets": [],
            "value": "",
        },
        {
            "id": "873a7bae-d867-408e-a22e-9c6323fe9d64",
            "comment": "",
            "command": "click",
            "target": "id=s-lib-app-anchor",
            "targets": [
                ["id=s-lib-app-anchor", "id"],
                ["linkText=LibApps", "linkText"],
                ["css=#s-lib-app-anchor", "css:finder"],
                ["xpath=//a[contains(text(),'LibApps')]", "xpath:link"],
                ["xpath=//a[@id='s-lib-app-anchor']", "xpath:attributes"],
                [
                    "xpath=//nav[@id='s-lg-admin-command-bar']/div/ul/li/a",
                    "xpath:idRelative",
                ],
                ["xpath=//a[contains(@href, '#')]", "xpath:href"],
                ["xpath=//a", "xpath:position"],
                ["xpath=//a[contains(.,'LibApps ')]", "xpath:innerText"],
            ],
            "value": "",
        },
        {
            "id": "5bdaa4b6-218c-40c6-942c-40c066c4faa8",
            "comment": "",
            "command": "click",
            "target": "linkText=LibGuides",
            "targets": [
                ["linkText=LibGuides", "linkText"],
                ["css=li:nth-child(3) > .dropdown-item", "css:finder"],
                ["xpath=//a[contains(text(),'LibGuides')]", "xpath:link"],
                ["xpath=//ul[@id='s-lib-app-menu']/li[3]/a", "xpath:idRelative"],
                [
                    "xpath=//a[contains(@href, 'https://caltech.libapps.com/libapps/login.php?site_id=64')]",
                    "xpath:href",
                ],
                ["xpath=//li[3]/a", "xpath:position"],
                ["xpath=//a[contains(.,'LibGuides')]", "xpath:innerText"],
            ],
            "value": "",
        },
        {
            "id": "1defc037-f605-4503-a9cf-5f44740a9ee1",
            "comment": "",
            "command": "click",
            "target": "linkText=Admin",
            "targets": [
                ["linkText=Admin", "linkText"],
                ["css=.dropdown:nth-child(11) > a", "css:finder"],
                [
                    "xpath=//nav[@id='s-lg-admin-command-bar']/ul/li[11]/a",
                    "xpath:idRelative",
                ],
                ["xpath=(//a[contains(@href, '#')])[5]", "xpath:href"],
                ["xpath=//nav/ul/li[11]/a", "xpath:position"],
                ["xpath=//a[contains(.,'Admin')]", "xpath:innerText"],
            ],
            "value": "",
        },
        {
            "id": "5a65f9c9-bd38-48d5-bf87-6abfad5bd9d3",
            "comment": "",
            "command": "click",
            "target": "linkText=Look & Feel",
            "targets": [
                ["linkText=Look & Feel", "linkText"],
                ["css=.open li:nth-child(2) > a", "css:finder"],
                ["xpath=//a[contains(text(),'Look & Feel')]", "xpath:link"],
                ["xpath=(//a[@onclick=''])[17]", "xpath:attributes"],
                [
                    "xpath=//nav[@id='s-lg-admin-command-bar']/ul/li[11]/ul/li[2]/a",
                    "xpath:idRelative",
                ],
                ["xpath=//a[contains(@href, 'lookfeel.php')]", "xpath:href"],
                ["xpath=//li[11]/ul/li[2]/a", "xpath:position"],
                ["xpath=//a[contains(.,'Look & Feel')]", "xpath:innerText"],
            ],
            "value": "",
        },
        {
            "id": "b38478e0-e5e0-4e33-b661-9c782d9040b1",
            "comment": "",
            "command": "click",
            "target": "linkText=Custom JS/CSS",
            "targets": [
                ["linkText=Custom JS/CSS", "linkText"],
                ["css=.nav > li:nth-child(2) > a", "css:finder"],
                ["xpath=//a[contains(text(),'Custom JS/CSS')]", "xpath:link"],
                ["xpath=//div[@id='col1']/ul/li[2]/a", "xpath:idRelative"],
                ["xpath=//a[contains(@href, '?action=1')]", "xpath:href"],
                ["xpath=//div/ul/li[2]/a", "xpath:position"],
                ["xpath=//a[contains(.,'Custom JS/CSS')]", "xpath:innerText"],
            ],
            "value": "",
        },
        {
            "id": "5d730e36-9b95-4646-95bf-793ff2d6ecf1",
            "comment": "",
            "command": "click",
            "target": "css=#s-lg-include-files_link",
            "targets": [
                [
                    "css=#s-lg-include-files_link > .s-lg-admin-field-label",
                    "css:finder",
                ],
                ["xpath=//a[@id='s-lg-include-files_link']/span", "xpath:idRelative"],
                ["xpath=//div[2]/div/a/span", "xpath:position"],
                [
                    "xpath=//span[contains(.,'Upload Customization Files')]",
                    "xpath:innerText",
                ],
            ],
            "value": "",
        },
        {
            "id": "7dfba71e-6e50-47a9-b06e-a62c1c387921",
            "comment": "",
            "command": "type",
            "target": "id=include_file",
            "targets": [
                ["id=include_file", "id"],
                ["name=include_file", "name"],
                ["css=#include_file", "css:finder"],
                ["xpath=//input[@id='include_file']", "xpath:attributes"],
                ["xpath=//div[@id='include_file-grp']/span/input", "xpath:idRelative"],
                ["xpath=//span/input", "xpath:position"],
            ],
            "value": filepath,
        },
    ],
}
side_tests_wrapper["tests"].append(side_test)

with open(f"assets/{slug}.side", "w") as fp:
    json.dump(side_tests_wrapper, fp, indent=4)
