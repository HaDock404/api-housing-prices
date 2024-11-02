FROM python:3.10-slim

WORKDIR /app

COPY packages/requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app/production

COPY . . 

EXPOSE 5000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]