import os
import subprocess

from playwright.sync_api import sync_playwright


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
        with sync_playwright() as playwright:
            b = playwright.firefox.launch()
            p = b.new_page(base_url=admin_base_url)
            p.goto("/libguides")
            p.fill("#s-libapps-email", admin_username)
            p.fill("#s-libapps-password", admin_password)
            p.click("#s-libapps-login-button")
            p.goto("/libguides/lookfeel.php?action=1")
            p.click("#s-lg-include-files_link")
            p.set_input_files("#include_file", compiled_css)
            b.close()


if __name__ == "__main__":
    # fmt: off
    import plac; plac.call(main)
