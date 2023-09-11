FROM python:3.10.6

ARG DOCKER_BUILD_ENVIRONMENT=production
ENV DOCKER_BUILD_ENVIRONMENT=${DOCKER_BUILD_ENVIRONMENT}

# Install core libs
RUN apt-get update -y
RUN apt-get install -y \
  apt-utils \
  netcat-traditional \
  redis-server

# Install deps
RUN pip install poetry>=1.3.2
RUN poetry config virtualenvs.create false
COPY poetry.lock /tmp/install/
COPY pyproject.toml /tmp/install/
WORKDIR /tmp/install
RUN poetry install --no-root

RUN mkdir -p /home/app
WORKDIR /home/app

# Create media folder
RUN mkdir -p /home/app/data/media

# Prepare app bin
COPY ./bin /home/app/bin
RUN chmod -R +xr /home/app/bin
ENV PATH="/home/app/bin:${PATH}"

COPY ./ /home/app/src
RUN chmod -R +xr /home/app/src

WORKDIR /home/app/src
ENV PYTHONPATH="/home/app/src:$PYTHONPATH"

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]