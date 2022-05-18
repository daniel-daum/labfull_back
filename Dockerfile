
FROM python:3.9

ENV PGUSER=postgres
ENV PGPASSWORD=postgres
ENV PGHOST=localhost
ENV PGDATABASE=development
ENV PGPORT=5432


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./src /code/app

EXPOSE 80000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]