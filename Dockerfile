FROM python:3.9.1

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

# System deps:
RUN pip install "poetry"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY ./poetry.lock ./pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry -V\
  && poetry install --no-interaction --no-ansi --no-dev

COPY . /code/

RUN touch ebay_alerts/settings/.env

ENV SECRET_KEY "default"
RUN python manage.py collectstatic
# Run the image as a non-root user
RUN adduser --disabled-password --gecos '' myuser
USER myuser

