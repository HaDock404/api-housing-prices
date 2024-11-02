FROM python:3.10-slim

WORKDIR /app

COPY packages/requirements.txt .
RUN pip install -r requirements.txt

COPY model /app/model

WORKDIR /app/production

COPY . . 

EXPOSE 5000

CMD ["uvicorn", "production.api:app", "--host", "0.0.0.0", "--port", "5000"]