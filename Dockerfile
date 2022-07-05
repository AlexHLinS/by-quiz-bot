FROM python:3.10

WORKDIR /db_backend

COPY ./requirements.txt /db_backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /db_backend/requirements.txt

COPY . /db_backend

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]