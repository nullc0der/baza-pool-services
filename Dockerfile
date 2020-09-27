FROM python:3.7
LABEL maintainer Prasanta Kakati <prasantakakati@baza.foundation>
RUN apt-get update && \
    apt-get install --yes build-essential postgresql-client \
    libpq-dev curl
RUN mkdir /baza-pool-services
WORKDIR /baza-pool-services
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
COPY pyproject.toml poetry.lock /baza-pool-services/
RUN . $HOME/.poetry/env && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev
COPY . /baza-pool-services
CMD [ "sh", "start.sh" ]