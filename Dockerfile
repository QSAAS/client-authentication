FROM python:3.8

RUN apt-get update && apt-get install -y --no-install-recommends \
  libpng-dev \
  libjpeg-dev \
  libfreetype6-dev \
  libpq-dev \
  libssl-dev \
  swig \
  pkg-config

RUN mkdir /app

WORKDIR /app

#COPY pyproject.toml /app/pyproject.toml
#COPY poetry.lock /app/poetry.lock
#COPY poetry.toml /app/poetry.toml
COPY . .
RUN pip install poetry

RUN python -m venv .venv && poetry install --no-root

#COPY . .
# add staticfiles dir to run on gitlab runner
RUN mkdir -p ./staticfiles
#touch will make empty file, just to avoid crashing environ
RUN touch ./.env
RUN cd /app && \
  mkdir -p static && \
#  DJANGO_SETTINGS_MODULE=config.prod \
  DJANGO_SECRET_KEY=whateversecretkey \
  DJANGO_ALLOWED_HOSTS=* \
  DJANGO_CORS_ORIGIN_REGEX_WHITELIST=* \
  DJANGO_CSRF_TRUSTED_ORIGINS=* \
  poetry run python manage.py collectstatic --noinput


EXPOSE 5000

#ENTRYPOINT [ "/docker-entrypoint.sh" ]
CMD [ "/app/.venv/bin/gunicorn", "--worker-class=uvicorn.workers.UvicornWorker", "asgi:application", "-b=0.0.0.0:5000"]
