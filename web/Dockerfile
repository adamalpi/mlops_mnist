FROM python:3.8

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
ENV PATH "$PATH:/root/.local/bin/"

RUN mkdir /service
WORKDIR /service
ADD . /service/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]

# docker build -t web-service:latest .
# docker run --rm --name=web-service -p 8501:8501 web-service