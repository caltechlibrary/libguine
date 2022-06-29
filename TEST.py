import os
import subprocess

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def main(
    file: "modified file from which to build artifacts",  # type: ignore
    admin_base_url: "base url for admin access",  # type: ignore
    admin_username: "username for admin access",  # type: ignore
    admin_password: "password for admin access",  # type: ignore
):
    os.makedirs("artifacts", exist_ok=True)
    # html and shtm files may need includes processed
    if file.endswith(".html") or file.endswith(".shtm"):
        pass
        if file.split("-")[0] == "head":
            pass
        elif file.split("-")[0] == "template":
            pass
        elif file.split("-")[0] == "footer":
            pass
        elif file.split("-")[0] == "header":
            pass
        # TODO compile HTML
    # scss files may need compiling
    elif file.endswith(".scss"):
        compiled_css = "artifacts/TEST.css"
        result = subprocess.run(
            [
                "sass",
                "--no-charset",
                "--no-source-map",
                "TEST.scss",
                compiled_css,
            ]
        )
        print(result)
        try:
            with sync_playwright() as playwright:
                b = playwright.firefox.launch()
                p = b.new_page(base_url=admin_base_url)
                p.goto("/libguides")
                p.fill("#s-libapps-email", admin_username)
                p.fill("#s-libapps-password", admin_password)
                p.screenshot(full_page=True, path="artifacts/1.png")
                p.click("#s-libapps-login-button")
                p.screenshot(full_page=True, path="artifacts/2.png")
                # p.goto("/libguides/lookfeel.php?action=1")
                # p.screenshot(full_page=True, path="artifacts/lookfeel_action_1.png")
                p.click("#s-lg-admin-command-bar a:text('Admin')")
                p.screenshot(full_page=True, path="artifacts/3.png")
                p.click("#s-lg-admin-command-bar a:text('Look & Feel')")
                p.screenshot(full_page=True, path="artifacts/4.png")
                p.click("#s-lib-admin-tabs a:text('Custom JS/CSS')")
                p.screenshot(full_page=True, path="artifacts/5.png")
                p.click("#s-lg-include-files_link")
                p.screenshot(full_page=True, path="artifacts/6.png")
                p.set_input_files("#include_file", compiled_css)
                p.screenshot(full_page=True, path="artifacts/7.png")
                b.close()
        except PlaywrightTimeoutError as e:
            print(str(e))
            return


if __name__ == "__main__":
    # fmt: off
    import plac; plac.call(main)
