FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install pika
CMD [ "python", "producer.py" ]