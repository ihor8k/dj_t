import os
import shutil

TERMINATOR = '\x1b[0m'
WARNING = '\x1b[1;33m [WARNING]: '
INFO = '\x1b[1;33m [INFO]: '
HINT = '\x1b[3;33m'
SUCCESS = '\x1b[1;32m [SUCCESS]: '


def remove_celery_files():
    file_names = [os.path.join('config', 'celery_app.py')]
    for file_name in file_names:
        os.remove(file_name)


def remove_drf_files_folders():
    dirs = ['apps/accounts/api']
    for path_dir in dirs:
        shutil.rmtree(path_dir, ignore_errors=True)

    file_names = ['config/urls_api_v1.py',
                  'helpers/drf.py']
    for file_name in file_names:
        os.remove(file_name)


def main():
    if '{{ cookiecutter.use_celery }}'.lower() == 'n':
        remove_celery_files()
    
    if '{{ cookiecutter.use_drf }}'.lower() == 'n':
        remove_drf_files_folders()

    print(SUCCESS + 'Project initialized, keep up the good work!' + TERMINATOR)


if __name__ == '__main__':
    main()
