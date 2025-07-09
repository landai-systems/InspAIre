FROM python:3.11-slim

WORKDIR /app

COPY apps/api/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/api /app
COPY services /app/services

RUN mkdir -p /app/uploads

ENV PYTHONPATH="/app:/app/services"

CMD ["python", "run.py"]
