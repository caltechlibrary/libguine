import json
import os
import shutil
import subprocess

from pathlib import Path


def main(
    file: "modified file from which to build artifacts",  # type: ignore
    groups: '{"groups":[{"slug":"foo","id":"999"},{…}]}',  # type: ignore
    github_commit: ("optional github commit path", "option", "g"),  # type: ignore
):
    print(f"🐞 file: {file}")

    if file.endswith(".scss"):
        # NOTE primary scss files do not have named parent directories
        extent = Path(file).parent.name if Path(file).parent.name else Path(file).stem
        if extent == "common":
            # TODO extend list with additional extents as needed
            for extent in ["libanswers"]:
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
        target = file.split("-")[0]
        slugs = [g["slug"] for g in json.loads(groups)["groups"]]
        slugs.append("system")
        scopes = list(slugs)
        scope = (
            file.split(".")[0].split("-")[-1]
            if file.split(".")[0].split("-")[-1] in scopes
            else None
        )
        # avoid redundant artifact creation
        if os.path.isfile(f'artifacts/{file.split("/")[-1]}') or os.path.isfile(
            f"artifacts/{target}--{scope}.html"
        ):
            print(f"🐞 artifacts exist:", os.listdir("artifacts"))
            return
        html = "<!-- WARNING: GENERATED CODE *EDITS WILL BE OVERWRITTEN* -->\n"
        if github_commit:
            html += f"<!-- see https://github.com/{github_commit[:len(github_commit) - 33]} -->\n\n"
        if target == "template" or target == "head":
            with open(file) as f:
                html += f.read()
            with open(f'artifacts/{file.split("/")[-1]}', "w") as f:
                f.write(html)
        elif target == "header" or target == "footer":
            fileobject = open(f"{target}-wrapper.shtm")
            if scope is None:
                for scope in scopes:
                    print(f"🐞 scope: {scope}")
                    # reset output by copying html content into it
                    output = str(html)
                    output += parse_nested_includes(fileobject, scope)
                    with open(f"artifacts/{target}--{scope}.html", "w") as f:
                        f.write(output)
            else:
                html += parse_nested_includes(fileobject, scope)
                with open(f"artifacts/{target}--{scope}.html", "w") as f:
                    f.write(html)
            fileobject.close()
        print(f"🐞 artifacts:", os.listdir("artifacts"))


def compile_css(extent, github_commit):
    # NOTE avoid redundant artifact creation
    if Path(f"artifacts/{extent}.css").is_file():
        print(f"🐞 file exists: artifacts/{extent}.css")
        return
    # NOTE requires `sass` command
    subprocess.run(
        [
            "sass",
            "--no-charset",
            "--no-source-map",
            f"{extent}.scss",
            f"artifacts/{extent}.css",
        ]
    )
    with open(f"artifacts/{extent}.css", "r") as f:
        css = f.read()
    with open(f"artifacts/{extent}.css", "w") as f:
        f.write(
            f"/* see https://github.com/{github_commit[:len(github_commit) - 33]} */\n\n"
        )
        f.write(css)


def parse_nested_includes(fileobject, scope=None):
    html = ""
    fileobject.seek(0)
    for line in fileobject:
        if line.strip().startswith("<!--#include"):
            included_file = line.split("'")[1]
            if included_file.split(".")[0].endswith("-GROUP"):
                fo = open(included_file.replace("GROUP", scope))
                html += parse_nested_includes(fo, scope)
                fo.close()
            else:
                fo = open(included_file)
                html += parse_nested_includes(fo, scope)
                fo.close()
        else:
            html += line
    return html


if __name__ == "__main__":
    # fmt: off
    import plac; plac.call(main)
