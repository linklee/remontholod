import pip

packages = ["Flask"]


def install(package):
    # Debugging
    pip.main(["install", "--pre", "--upgrade", "--no-index",
            "--find-links=.", package, "--log-file", "log.txt", "-vv"])
    pip.main(["install", package])


def install_packages():
    for package in packages:
        install(package)

if __name__ == "__main__":
    install_packages()