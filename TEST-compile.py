import json
import os
import subprocess


def main(
    file: "modified file from which to build artifacts",  # type: ignore
    groups: '{"groups":[{"slug":"foo","id":"999"},{…}]}',  # type: ignore
    github_commit: ("optional github commit path", "option", "g"),  # type: ignore
):
    print(f"🐞 file: {file}")
    # TODO optimize
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
                "TEST.scss",  # TODO
                "artifacts/TEST.css",  # TODO
            ]
        )
        print(os.listdir("artifacts"))
    elif file.endswith(".html") or file.endswith(".shtm"):
        target = file.split("-")[0]
        slugs = [g["slug"] for g in json.loads(groups)["groups"]]
        print(f"🐞 slugs: {slugs}")
        scopes = list(slugs).append("system")
        print(f"🐞 scopes: {scopes}")
        scope = (
            file.split(".")[0].split("-")[-1]
            if file.split(".")[0].split("-")[-1] in scopes
            else None
        )
        # avoid redundant artifact creation
        if os.path.isfile(f"artifacts/{target}--{scope}.html"):
            print(f"🐞 file exists: artifacts/{target}--{scope}.html")
            return
        html = "<!-- WARNING: GENERATED CODE *EDITS WILL BE OVERWRITTEN* -->\n"
        if github_commit:
            html += (
                f"<!-- see github.com/{github_commit[:len(github_commit) - 33]} -->\n\n"
            )
        if target == "template" or target == "head":
            with open(file) as f:
                html += f.read()
            with open(f'artifacts/{file.split("/")[-1]}', "w") as f:
                f.write(html)
            print(os.listdir("artifacts"))
        elif target == "header" or target == "footer":
            fileobject = open(f"{target}-wrapper.shtm")
            html += parse_nested_includes(fileobject, html, scope)
            fileobject.close()
            with open(f'artifacts/{file.split("/")[-1]}', "w") as f:
                f.write(html)
            print(os.listdir("artifacts"))

    def parse_nested_includes(fileobject, html, scope=None):
        if scope is None:
            for s in scopes:
                html += parse_nested_includes(fileobject, html, s)
        for line in fileobject:
            if line.strip().startswith("<!--#include"):
                included_file = line.split("'")[1]
                if included_file.split(".")[0].endswith("-GROUP"):
                    # open the GROUP/scope file and read its lines
                    fo = open(included_file.replace("GROUP", scope))
                    html += parse_nested_includes(fo, html, scope)
                    fo.close()
                else:
                    # open the file and read its lines
                    fo = open(included_file)
                    html += parse_nested_includes(fo, html, scope)
                    fo.close()
            else:
                html += line
        return html


if __name__ == "__main__":
    # fmt: off
    import plac; plac.call(main)
