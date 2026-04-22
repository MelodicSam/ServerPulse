FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY scripts ./scripts

ENV FLASK_APP=app.main
ENV PYTHONUNBUFFERED=1

EXPOSE 5000
CMD ["bash", "./scripts/start.sh"]
