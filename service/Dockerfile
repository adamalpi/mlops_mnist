FROM python:3.8

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
ENV PATH "$PATH:/root/.local/bin/"

RUN mkdir /service
WORKDIR /service
ADD . /service/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev

EXPOSE 9090

CMD ["python", "app.py"]

# docker build -t inference-service .
# docker run --rm --name=inference-service -p 9090:9090 inference-service

# to run in debug mode
# docker run --rm --name=inference-service -p 9090:9090 -e FLASK_ENV="development" inference-service
