import json
import os

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def main(
    admin_base_url: "base url for admin access",  # type: ignore
    admin_username: "username for admin access",  # type: ignore
    admin_password: "password for admin access",  # type: ignore
    groups: '{"groups":[{"slug":"foo","id":"999"},{…}]}',  # type: ignore
):
    for item in os.scandir("artifacts"):
        with sync_playwright() as playwright:
            try:
                b = playwright.firefox.launch()
                p = b.new_page(base_url=admin_base_url, record_video_dir="artifacts")
                p.goto("/libapps/login.php")
                p.fill("#s-libapps-email", admin_username)
                p.fill("#s-libapps-password", admin_password)
                p.click("#s-libapps-login-button")
                p.click("#s-lib-app-anchor")
                p.click("#s-lib-app-menu a:text('LibGuides')")
                if item.name.endswith(".css") or item.name.endswith(".js"):
                    p.click("#s-lg-admin-command-bar a:text('Admin')")
                    p.click("#s-lg-admin-command-bar a:text('Look & Feel')")
                    p.click("#s-lib-admin-tabs a:text('Custom JS/CSS')")
                    p.click("#s-lg-include-files_link")
                    p.set_input_files("#include_file", item.path)
                elif item.name.endswith(".html"):
                    target = item.name.split("-")[0]
                    slugs = [g["slug"] for g in json.loads(groups)["groups"]]
                    slugs.append("system")
                    scopes = list(slugs)
                    scope = (
                        item.name.split(".")[0].split("-")[-1]
                        if item.name.split(".")[0].split("-")[-1] in scopes
                        else None
                    )
                    with open(item) as f:
                        html = f.read()
                    if target == "template":
                        p.click("#s-lg-admin-command-bar a:text('Admin')")
                        p.click("#s-lg-admin-command-bar a:text('Look & Feel')")
                        p.click("#s-lib-admin-tabs a:text('Page Layout')")
                        if item.name.split("-")[1] == "guide":
                            p.click("#s-lib-admin-tabs a:text('Guide')")
                            p.click("#s-lg-guide-templates_link")
                            p.click("#select2-chosen-2")
                            # NOTE template must already exist
                            # TODO account for template not found condition
                            p.fill("#s2id_autogen2_search", item.name.split(".")[0])
                            p.press("#s2id_autogen2_search", "Enter")
                            # NOTE template takes time to load after select
                            p.wait_for_load_state("networkidle")
                            p.fill("#template_code", html)
                            p.click("#btn-save-template")
                            # NOTE must wait for success before moving on
                            p.wait_for_selector("#btn-save-template.btn-success")
                        if item.name.split("-")[1] == "search":
                            p.click("#s-lib-admin-tabs a:text('Search')")
                            p.click("#s-lg-tpl_link")
                            p.click("#select2-chosen-3")
                            # NOTE template must already exist
                            # TODO account for template not found condition
                            p.fill("#s2id_autogen3_search", item.name.split(".")[0])
                            p.press("#s2id_autogen3_search", "Enter")
                            # NOTE template takes time to load after select
                            p.wait_for_load_state("networkidle")
                            p.fill("#template_code", html)
                            p.click("#btn-save-template")
                            # NOTE must wait for success before moving on
                            p.wait_for_selector("#btn-save-template.btn-success")
                    elif target == "head":
                        if scope == "system":
                            p.goto("/libguides/lookfeel.php?action=1")
                            p.fill("#jscss_code", html)
                            p.click("#s-lg-btn-save-jscss")
                            # NOTE must wait for success before moving on
                            p.wait_for_selector("#s-lg-btn-save-jscss.btn-success")
                        else:
                            for group in json.loads(groups)["groups"]:
                                if scope == group["slug"]:
                                    p.goto(
                                        f'/libguides/groups.php?action=3&group_id={group["id"]}'
                                    )
                                    p.fill("#jscss_code", html)
                                    p.click("#s-lg-btn-save-jscss")
                                    # NOTE must wait for success before moving on
                                    p.wait_for_selector(
                                        "#s-lg-btn-save-jscss.btn-success"
                                    )
                    elif target == "header":
                        if scope == "system":
                            p.goto("/libguides/lookfeel.php?action=0")
                            p.fill("#banner_html", html)
                            p.click("#banner_html + .btn-primary")
                            # NOTE must wait for success before moving on
                            p.wait_for_selector("#banner_html + .btn-success")
                        else:
                            for group in json.loads(groups)["groups"]:
                                if scope == group["slug"]:
                                    p.goto(
                                        f'/libguides/groups.php?action=2&group_id={group["id"]}'
                                    )
                                    p.fill("#banner_html", html)
                                    p.click("#banner_html + .btn-primary")
                                    # NOTE must wait for success before moving on
                                    p.wait_for_selector("#banner_html + .btn-success")
                    elif target == "footer":
                        if scope == "system":
                            p.goto("/libguides/lookfeel.php?action=0")
                            p.click("#s-lg-footer_link")
                            p.fill("#footer_code", html)
                            p.click("#s-lg-btn-save-footer")
                            # NOTE must wait for success before moving on
                            p.wait_for_selector("#s-lg-btn-save-footer.btn-success")
                        else:
                            for group in json.loads(groups)["groups"]:
                                if scope == group["slug"]:
                                    p.goto(
                                        f'/libguides/groups.php?action=2&group_id={group["id"]}'
                                    )
                                    p.click("#s-lg-footer_link")
                                    p.fill("#footer_code", html)
                                    p.click("#s-lg-btn-save-footer")
                                    # NOTE must wait for success before moving on
                                    p.wait_for_selector(
                                        "#s-lg-btn-save-footer.btn-success"
                                    )
                b.close()
            except PlaywrightTimeoutError as e:
                b.close()
                raise e


if __name__ == "__main__":
    # fmt: off
    import plac; plac.call(main)
