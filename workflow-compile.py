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
    def parse_nested_includes(fileobject, scope=None):
        html = ""
        print(f"🐞 parse_nested_includes html:", type(html))
        for line in fileobject:
            if line.strip().startswith("<!--#include"):
                print(f"🐞 line: {line.strip()}")
                included_file = line.split("'")[1]
                if included_file.split(".")[0].endswith("-GROUP"):
                    fo = open(included_file.replace("GROUP", scope))
                    print(f'🐞 open: {included_file.replace("GROUP", scope)}')
                    html += parse_nested_includes(fo, scope)
                    fo.close()
                else:
                    fo = open(included_file)
                    print(f"🐞 open: {included_file}")
                    # pass empty string when compiling inner html
                    html += parse_nested_includes(fo, scope)
                    fo.close()
            else:
                html += line
        return html

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
        print(os.listdir("artifacts"))
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
        if os.path.isfile(f'artifacts/{file.split("/")[-1]}') or os.path.isfile(f"artifacts/{target}--{scope}.html"):
            print(f"🐞 artifacts exist:", os.listdir("artifacts"))
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
            print(f"🐞 if template/head:", os.listdir("artifacts"))
        elif target == "header" or target == "footer":
            print(f"🐞 elif header/footer html:", html)
            fileobject = open(f"{target}-wrapper.shtm")
            if scope is None:
                for scope in scopes:
                    print(f"🐞 {scope} html:", html)
                    html += parse_nested_includes(fileobject, scope)
                    with open(f'artifacts/{target}--{scope}.html', "w") as f:
                        f.write(html)
            else:
                html += parse_nested_includes(fileobject, scope)
                with open(f'artifacts/{target}--{scope}.html', "w") as f:
                    f.write(html)
            fileobject.close()
            print(f"🐞 elif header/footer:", os.listdir("artifacts"))


if __name__ == "__main__":
    # fmt: off
    import plac; plac.call(main)
