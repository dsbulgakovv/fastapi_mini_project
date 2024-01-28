FROM python:3.11

#RUN curl -sSL https://install.python-poetry.org | python3 -
#ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /app

COPY ./bot /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "app.py"]
