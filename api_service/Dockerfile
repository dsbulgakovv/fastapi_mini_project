FROM python:3.11-slim

WORKDIR /api

COPY ./api_service /api/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555"]

#EXPOSE 5555
