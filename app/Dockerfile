FROM python:3.12-slim

WORKDIR /app

COPY ./app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/src ./src

EXPOSE 8501

ENV API_URL="http://api:8080"
ENV TERMS_OF_SERVICE_URL="https://example.com/terms"

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
