FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
#, "--reload" can be added at the end
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


#docker build -t fastapi .
#docker image ls
#docker compose
