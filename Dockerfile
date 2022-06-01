
FROM python:3.9

ENV PGUSER=
ENV PGPASSWORD=
ENV PGHOST=
ENV PGDATABASE=
ENV PGPORT=


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./src /code/app

EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]