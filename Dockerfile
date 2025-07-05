FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create volume for persistent data
RUN mkdir -p /app/data
VOLUME /app/data

CMD ["python", "-u", "src/bot/scalper.py"]
