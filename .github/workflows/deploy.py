import json
import os
import sys

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


def test_deploy(page: Page):
    for item in os.scandir("artifacts"):
        try:
            page.goto("/libapps/login.php")
            page.fill("#s-libapps-email", os.environ.get("USERNAME"))
            page.fill("#s-libapps-password", os.environ.get("PASSWORD"))
            page.click("#s-libapps-login-button")
            page.click("#s-lib-app-anchor")
            page.click("#s-lib-app-menu a:text('LibGuides')")
            if item.name.endswith(".css") or item.name.endswith(".js"):
                page.click("#s-lg-admin-command-bar a:text('Admin')")
                page.click("#s-lg-admin-command-bar a:text('Look & Feel')")
                page.click("#s-lib-admin-tabs a:text('Custom JS/CSS')")
                page.click("#s-lg-include-files_link")
                page.set_input_files("#include_file", item.path)
            elif item.name.endswith(".html"):
                target = item.name.split("-")[0]
                with open(item) as f:
                    html = f.read()
                if target == "template":
                    page.click("#s-lg-admin-command-bar a:text('Admin')")
                    page.click("#s-lg-admin-command-bar a:text('Look & Feel')")
                    page.click("#s-lib-admin-tabs a:text('Page Layout')")
                    if item.name.split("-")[1] == "guide":
                        page.click("#s-lib-admin-tabs a:text('Guide')")
                        page.click("#s-lg-guide-templates_link")
                        page.click("#select2-chosen-2")
                        # NOTE template must already exist
                        # TODO account for template not found condition
                        page.fill("#s2id_autogen2_search", item.name.split(".")[0])
                        page.press("#s2id_autogen2_search", "Enter")
                        # NOTE template takes time to load after select
                        page.wait_for_load_state("networkidle")
                        page.fill("#template_code", html)
                        page.click("#btn-save-template")
                        # NOTE must wait for success before moving on
                        page.wait_for_selector("#btn-save-template.btn-success")
                    if item.name.split("-")[1] == "search":
                        page.click("#s-lib-admin-tabs a:text('Search')")
                        page.click("#s-lg-tpl_link")
                        page.click("#select2-chosen-3")
                        # NOTE template must already exist
                        # TODO account for template not found condition
                        page.fill("#s2id_autogen3_search", item.name.split(".")[0])
                        page.press("#s2id_autogen3_search", "Enter")
                        # NOTE template takes time to load after select
                        page.wait_for_load_state("networkidle")
                        page.fill("#template_code", html)
                        page.click("#btn-save-template")
                        # NOTE must wait for success before moving on
                        page.wait_for_selector("#btn-save-template.btn-success")
                elif target == "widget":
                    page.click("#s-lg-admin-command-bar a:text('Content')")
                    page.click("#s-lg-admin-command-bar a:text('Assets')")
                    page.fill(
                        "#name", item.name.split("-", maxsplit=2)[-1].split(".")[0]
                    )
                    page.click(
                        "#lg-admin-asset-filter .datatable-filter__button--submit"
                    )
                    try:
                        page.wait_for_selector(
                            "#s-lg-admin-datatable-content_info:text('showing 1 to 1 of 1 entries')"
                        )
                        page.click("#s-lg-admin-datatable-content a i.fa-edit")
                    except PlaywrightTimeoutError:
                        page.click("#s-lg-page-content button:text('Add Content Item')")
                        page.click("#s-lg-page-content a:text('Media / Widget')")
                        page.fill(
                            "#widget_name",
                            item.name.split("-", maxsplit=2)[-1].split(".")[0],
                        )
                    page.fill("#embed_code", html)
                    page.click("#s-lib-alert-btn-first")
                    page.wait_for_selector(
                        "td:text('"
                        + item.name.split("-", maxsplit=2)[-1].split(".")[0]
                        + "')"
                    )
                elif target == "head":
                    variant = item.name.split(".")[0].split("-")[-1]
                    if variant == "system":
                        page.goto("/libguides/lookfeel.php?action=1")
                        page.fill("#jscss_code", html)
                        page.click("#s-lg-btn-save-jscss")
                        # NOTE must wait for success before moving on
                        page.wait_for_selector("#s-lg-btn-save-jscss.btn-success")
                    elif variant == "libanswers":
                        # NOTE JS/CSS files are uploaded in LibGuides
                        page.click("#s-lib-app-anchor")
                        page.click("#s-lib-app-menu a:text('LibAnswers')")
                        page.click("#s-la-cmd-bar-collapse a:text('Admin')")
                        page.click("#s-la-cmd-bar-collapse a:text('System Settings')")
                        page.click(".nav-tabs a:text('Look & Feel')")
                        page.fill("#instmetafield", html)
                        page.click("#instmetabut")
                        # NOTE must wait for success before moving on
                        page.wait_for_selector("#s-ui-notification :text('Success')")
                    elif variant == "libcal":
                        # NOTE JS/CSS files are uploaded in LibGuides
                        page.click("#s-lib-app-anchor")
                        page.click("#s-lib-app-menu a:text('LibCal')")
                        page.click("#s-lc-app-menu-adm a")  # Admin
                        page.click("#s-lc-app-menu-adm a:text('Look & Feel')")
                        page.fill("#instmeta", html)
                        page.click("#instmeta ~ button")
                    else:
                        for group in json.loads(os.environ.get("GROUPS"))["groups"]:
                            if variant == group["slug"]:
                                page.goto(
                                    f'/libguides/groups.php?action=3&group_id={group["id"]}'
                                )
                                page.fill("#jscss_code", html)
                                page.click("#s-lg-btn-save-jscss")
                                # NOTE must wait for success before moving on
                                page.wait_for_selector(
                                    "#s-lg-btn-save-jscss.btn-success"
                                )
                elif target == "header":
                    variant = item.name.split(".")[0].split("-")[-1]
                    if variant == "system":
                        page.goto("/libguides/lookfeel.php?action=0")
                        page.fill("#banner_html", html)
                        page.click("#banner_html + .btn-primary")
                        # TODO LibAnswers & LibCal
                    else:
                        for group in json.loads(os.environ.get("GROUPS"))["groups"]:
                            if variant == group["slug"]:
                                page.goto(
                                    f'/libguides/groups.php?action=2&group_id={group["id"]}'
                                )
                                page.fill("#banner_html", html)
                                page.click("#banner_html + .btn-primary")
                                # NOTE must wait for success before moving on
                                page.wait_for_selector("#banner_html + .btn-success")
                elif target == "footer":
                    variant = item.name.split(".")[0].split("-")[-1]
                    if variant == "system":
                        page.goto("/libguides/lookfeel.php?action=0")
                        page.click("#s-lg-footer_link")
                        page.fill("#footer_code", html)
                        page.click("#s-lg-btn-save-footer")
                        # NOTE LibAnswers uses the same system footer
                        page.click("#s-lib-app-anchor")
                        page.click("#s-lib-app-menu a:text('LibAnswers')")
                        page.click("#s-la-cmd-bar-collapse a:text('Admin')")
                        page.click("#s-la-cmd-bar-collapse a:text('System Settings')")
                        page.click(".nav-tabs a:text('Look & Feel')")
                        page.fill("#instfooterfield", html)
                        page.click("#instfooterbut")
                        # NOTE LibCal uses the same system footer
                        page.click("#s-la-app-anchor")
                        page.click("#s-la-app-menu a:text('LibCal')")
                        page.click("#s-lc-app-menu-adm a")  # Admin
                        page.click("#s-lc-app-menu-adm a:text('Look & Feel')")
                        page.fill("#instfooter", html)
                        page.click("#instfooter ~ button")
                    else:
                        for group in json.loads(os.environ.get("GROUPS"))["groups"]:
                            if variant == group["slug"]:
                                page.goto(
                                    f'/libguides/groups.php?action=2&group_id={group["id"]}'
                                )
                                page.click("#s-lg-footer_link")
                                page.fill("#footer_code", html)
                                page.click("#s-lg-btn-save-footer")
                                # NOTE must wait for success before moving on
                                page.wait_for_selector(
                                    "#s-lg-btn-save-footer.btn-success"
                                )
        except PlaywrightTimeoutError:
            page.close()
            sys.exit(f"PLAYWRIGHT_TIMEOUT: {item.name}")
