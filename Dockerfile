FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
COPY requirements.txt requirements.lock ./
RUN python -m pip install --no-cache-dir -c requirements.lock -r requirements.txt
COPY simulation.py scheduler.py ./
USER 10001:10001
CMD ["python", "scheduler.py"]
