import os
import subprocess


def main(
    file: "modified file from which to build artifacts",  # type: ignore
):
    os.mkdir("artifacts")
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
        result = subprocess.run(
            "sass", "--no-charset", "--no-source-map", "TEST.scss", "artifacts/TEST.css"
        )
        print(result)
    # TODO upload artifacts


if __name__ == "__main__":
    # fmt: off
    import plac; plac.call(main)
