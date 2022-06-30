import json
import os
import subprocess

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def main(
    file: "modified file from which to build artifacts",  # type: ignore
    admin_base_url: "base url for admin access",  # type: ignore
    admin_username: "username for admin access",  # type: ignore
    admin_password: "password for admin access",  # type: ignore
    groups: "json representation of group slugs and id numbers",  # type: ignore
    github_commit: ("optional github commit path", "option", "g"),  # type: ignore
):
    os.makedirs("artifacts", exist_ok=True)
    try:
        with sync_playwright() as playwright:
            b = playwright.firefox.launch()
            p = b.new_page(base_url=admin_base_url, record_video_dir="artifacts")
            p.goto("/libapps/login.php")
            p.fill("#s-libapps-email", admin_username)
            p.fill("#s-libapps-password", admin_password)
            p.click("#s-libapps-login-button")
            p.click("#s-lib-app-anchor")
            p.click("#s-lib-app-menu a:text('LibGuides')")
            # html and shtm files may need includes processed
            if file.endswith(".html") or file.endswith(".shtm"):
                if file.split("-")[0] == "head":
                    head_html = (
                        "<!-- WARNING: GENERATED CODE *EDITS WILL BE OVERWRITTEN* -->\n"
                    )
                    if github_commit:
                        head_html += f"<!-- see github.com/{github_commit[:len(github_commit) - 33]} -->\n\n"
                    with open(file, "r") as f:
                        head_html += f.read()
                    if file.split(".")[0].split("-")[-1] == "system":
                        p.goto("/libguides/lookfeel.php?action=1")
                        p.fill("#jscss_code", head_html)
                        p.click("#s-lg-btn-save-jscss")
                        # NOTE must wait for success before moving on
                        p.wait_for_selector("#s-lg-btn-save-jscss.btn-success")
                    else:
                        for group in json.loads(groups)["groups"]:
                            print(group)
                            if file.split(".")[0].split("-")[-1] == group.slug:
                                p.goto(
                                    f"/libguides/groups.php?action=3&group_id={group.id}"
                                )
                                p.fill("#jscss_code", head_html)
                                p.click("#s-lg-btn-save-jscss")
                                # NOTE must wait for success before moving on
                                p.wait_for_selector("#s-lg-btn-save-jscss.btn-success")
                elif file.split("-")[0] == "template":
                    template_html = (
                        "<!-- WARNING: GENERATED CODE *EDITS WILL BE OVERWRITTEN* -->\n"
                    )
                    if github_commit:
                        template_html += f"<!-- see github.com/{github_commit[:len(github_commit) - 33]} -->\n\n"
                    with open(file, "r") as f:
                        template_html += f.read()
                    p.click("#s-lg-admin-command-bar a:text('Admin')")
                    p.click("#s-lg-admin-command-bar a:text('Look & Feel')")
                    p.click("#s-lib-admin-tabs a:text('Page Layout')")
                    if file.split("-")[1] == "guide":
                        p.click("#s-lib-admin-tabs a:text('Guide')")
                        p.click("#s-lg-guide-templates_link")
                        p.click("#select2-chosen-2")
                        # NOTE template must already exist
                        # TODO account for template not found condition
                        p.fill("#s2id_autogen2_search", file.split(".")[0])
                        p.press("#s2id_autogen2_search", "Enter")
                        # NOTE template takes time to load after select
                        p.wait_for_load_state("networkidle")
                        p.fill("#template_code", template_html)
                        p.click("#btn-save-template")
                        # NOTE must wait for success before moving on
                        p.wait_for_selector("#btn-save-template.btn-success")
                    if file.split("-")[1] == "search":
                        p.click("#s-lib-admin-tabs a:text('Search')")
                        p.click("#s-lg-tpl_link")
                        p.click("#select2-chosen-3")
                        # NOTE template must already exist
                        # TODO account for template not found condition
                        p.fill("#s2id_autogen3_search", file.split(".")[0])
                        p.press("#s2id_autogen3_search", "Enter")
                        # NOTE template takes time to load after select
                        p.wait_for_load_state("networkidle")
                        p.fill("#template_code", template_html)
                        p.click("#btn-save-template")
                        # NOTE must wait for success before moving on
                        p.wait_for_selector("#btn-save-template.btn-success")
                elif file.split("-")[0] == "footer":
                    pass
                elif file.split("-")[0] == "header":
                    pass
                # TODO compile HTML
            # scss files may need compiling
            elif file.endswith(".scss"):
                compiled_css = "artifacts/TEST.css"
                subprocess.run(
                    [
                        "sass",
                        "--no-charset",
                        "--no-source-map",
                        "TEST.scss",
                        compiled_css,
                    ]
                )
                p.click("#s-lg-admin-command-bar a:text('Admin')")
                p.click("#s-lg-admin-command-bar a:text('Look & Feel')")
                p.click("#s-lib-admin-tabs a:text('Custom JS/CSS')")
                p.click("#s-lg-include-files_link")
                p.set_input_files("#include_file", compiled_css)
            b.close()
    except PlaywrightTimeoutError as e:
        print(str(e))
        return


if __name__ == "__main__":
    # fmt: off
    import plac; plac.call(main)
