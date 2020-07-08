## {{ cookiecutter.project_slug }}


![](https://img.shields.io/badge/designed%20for-{{ cookiecutter.project_slug }}-ff1544.svg)



####Need Install [docker](https://docs.docker.com/install/)


Start local:

    docker-compose up

    ----/ or /----
    {%- if cookiecutter.use_celery == 'y' %}
    docker-compose up -d celery_worker
    {%- endif %}
    {%- if cookiecutter.use_redis == 'y' %}
    docker-compose up -d redis
    {%- endif %}
    docker-compose up -d postgresql
    docker-compose up app

Shell:

    # python
    docker exec -it <your_conteiner_app> /bin/sh

    # postgresql
    docker exec -it <your_containet_db> bash
