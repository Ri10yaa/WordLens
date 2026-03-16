FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY pyproject.toml requirements.txt ./
RUN pip install -r requirements.txt && python -m spacy download en_core_web_sm

COPY src ./src

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
