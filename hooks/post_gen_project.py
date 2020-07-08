import os


TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "


def remove_celery_files():
    file_names = [os.path.join("config", "celery_app.py")]
    for file_name in file_names:
        os.remove(file_name)


def main():
    if "{{ cookiecutter.use_celery }}".lower() == "n":
        remove_celery_files()

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
