FROM python:3.11

#RUN curl -sSL https://install.python-poetry.org | python3 -
#ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /bot

COPY ./bot /bot/
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
