import json
import os
import subprocess


def main(
    file: "modified file from which to build artifacts",  # type: ignore
    groups: '{"groups":[{"slug":"foo","id":"999"},{…}]}',  # type: ignore
    github_commit: ("optional github commit path", "option", "g"),  # type: ignore
):
    print(f"🐞 file: {file}")

    if file.endswith(".scss"):
        # avoid redundant artifact creation
        if os.path.isfile(f"artifacts/custom.css"):
            print("🐞 file exists: artifacts/custom.css")
            return
        # NOTE requires `sass` command
        subprocess.run(
            [
                "sass",
                "--no-charset",
                "--no-source-map",
                "custom.scss",
                "artifacts/custom.css",
            ]
        )
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
                    html += parse_nested_includes(fileobject, scope)
                    print(f"🐞 html: {html}")
                    with open(f"artifacts/{target}--{scope}.html", "w") as f:
                        f.write(html)
            else:
                html += parse_nested_includes(fileobject, scope)
                with open(f"artifacts/{target}--{scope}.html", "w") as f:
                    f.write(html)
            fileobject.close()
        print(f"🐞 artifacts:", os.listdir("artifacts"))


def parse_nested_includes(fileobject, scope=None):
    html = ""
    for line in fileobject:
        if line.strip().startswith("<!--#include"):
            included_file = line.split("'")[1]
            print(f"🐞 included_file: {included_file}")
            if included_file.split(".")[0].endswith("-GROUP"):
                print(f"🐞 scope (endswith-GROUP): {scope}")
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
