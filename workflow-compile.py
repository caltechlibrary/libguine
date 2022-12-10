import json
import os
import shutil
import subprocess

from pathlib import Path


def main(
    file: "modified file from which to build artifacts",  # type: ignore
    libguides_groups: '{"groups":[{"slug":"foo","id":"999"},{…}]}',  # type: ignore
    github_commit: ("optional github commit path", "option", "g"),  # type: ignore
):
    print(f"🐞 file: {file}")

    if file.endswith(".scss"):
        # NOTE primary scss files do not have named parent directories
        extent = Path(file).parent.name if Path(file).parent.name else Path(file).stem
        if extent == "common":
            for extent in ["custom", "libanswers", "libguides"]:
                compile_css(extent, github_commit)
        else:
            compile_css(extent, github_commit)
    elif file.endswith(".js"):
        extent = Path(file).stem
        # NOTE avoid redundant artifact creation
        if Path(f"artifacts/{extent}.js").is_file():
            print(f"🐞 file exists: artifacts/{extent}.js")
            return
        shutil.copyfile(f"{extent}.js", f"artifacts/{extent}.js")
        with open(f"artifacts/{extent}.js", "r") as f:
            js = f.read()
        with open(f"artifacts/{extent}.js", "w") as f:
            if github_commit:
                f.write(
                    f"// see https://github.com/{github_commit[:len(github_commit) - 33]} //\n\n"
                )
            f.write(js)
    elif file.startswith("widget--"):
        # avoid redundant artifact creation
        if os.path.isfile(f"artifacts/{file}"):
            print(f"🐞 file exists: artifacts/{file}")
            return
        shutil.copyfile(file, f"artifacts/{file}")
        with open(f"artifacts/{file}", "r") as f:
            widget = f.read()
        with open(f"artifacts/{file}", "w") as f:
            f.write(
                f"<!-- see https://github.com/{github_commit[:len(github_commit) - 33]} -->\n\n"
            )
            f.write(widget)
    elif file.endswith(".html") or file.endswith(".shtm"):
        component = file.split("-")[0]
        html = "<!-- WARNING: GENERATED CODE *EDITS WILL BE OVERWRITTEN* -->\n"
        if github_commit:
            html += f"<!-- see https://github.com/{github_commit[:len(github_commit) - 33]} -->\n\n"
        if component == "template" or component == "head":
            # NOTE use the file as is with prepended comments
            with open(file) as f:
                html += f.read()
            with open(f'artifacts/{file.split("/")[-1]}', "w") as f:
                f.write(html)
        elif component == "header" or component == "footer":
            # NOTE libguides_groups is set in a GitHub Actions secret
            slugs = [g["slug"] for g in json.loads(libguides_groups)["groups"]]
            slugs.append("system")
            variants = list(slugs)
            variant = (
                file.split(".")[0].split("-")[-1]
                if file.split(".")[0].split("-")[-1] in variants
                else None
            )
            # NOTE avoid redundant artifact creation
            if os.path.isfile(f'artifacts/{file.split("/")[-1]}') or os.path.isfile(
                f"artifacts/{component}--{variant}.html"
            ):
                print(f"🐞 artifacts exist:", os.listdir("artifacts"))
                return
            wrapper = open(f"{component}-wrapper.shtm")
            if variant:
                html += parse_nested_includes(wrapper, variant)
                with open(f"artifacts/{component}--{variant}.html", "w") as f:
                    f.write(html)
            else:
                # NOTE header-wrapper.shtm triggers this condition, for example
                for variant in variants:
                    print(f"🐞 variant: {variant}")
                    # reset output by copying html content into it
                    output = str(html)
                    output += parse_nested_includes(wrapper, variant)
                    with open(f"artifacts/{component}--{variant}.html", "w") as f:
                        f.write(output)
            wrapper.close()
        print(f"🐞 artifacts:", os.listdir("artifacts"))


def compile_css(extent, github_commit):
    # NOTE avoid redundant artifact creation
    if Path(f"artifacts/{extent}.css").is_file():
        print(f"⚠️ file exists: artifacts/{extent}.css")
        return
    # NOTE requires `sass` command
    subprocess.run(
        [
            "sass",
            "--no-charset",
            "--no-source-map",
            f"{extent}.scss",
            f"artifacts/{extent}.css",
        ],
        check=True,
    )
    with open(f"artifacts/{extent}.css", "r") as f:
        css = f.read()
    with open(f"artifacts/{extent}.css", "w") as f:
        if github_commit:
            f.write(
                f"/* see https://github.com/{github_commit[:len(github_commit) - 33]} */\n\n"
            )
        f.write(css)


def parse_nested_includes(wrapper, variant=None):
    html = ""
    wrapper.seek(0)
    for line in wrapper:
        if line.strip().startswith("<!--#include"):
            included_file = line.split("'")[1]
            if included_file.split(".")[0].endswith("-GROUP"):
                fo = open(included_file.replace("GROUP", variant))
                html += parse_nested_includes(fo, variant)
                fo.close()
            else:
                fo = open(included_file)
                html += parse_nested_includes(fo, variant)
                fo.close()
        else:
            html += line
    return html


if __name__ == "__main__":
    # fmt: off
    import plac; plac.call(main)
