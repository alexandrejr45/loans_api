FROM python:3.13.2-slim as builder

RUN pip install poetry==2.1.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /usr/loans_api/app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

FROM python:3.13.2-slim as runtime

ENV VIRTUAL_ENV=/usr/loans_api/app/.venv \
    PATH="/usr/loans_api/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY app/ /usr/loans_api/app

WORKDIR /usr/loans_api/app


#FROM runner AS development
#
#WORKDIR /app/src
#ENTRYPOINT [ "/app/src/entrypoint.sh" ]
#
#FROM runner AS production
#
## Set user and group
#ARG user=django
#ARG group=django
#ARG uid=1000
#ARG gid=1000
#RUN groupadd -g ${gid} ${group}
#RUN useradd -u ${uid} -g ${group} -s /bin/sh -m ${user}
#
## Switch to user
#RUN chown -R ${uid}:${gid} /app
#RUN chown -R ${uid}:${gid} /db
#
#USER ${uid}:${gid}
#
#WORKDIR /app/src
#ENTRYPOINT [ "/app/src/entrypoint.sh" ]
