FROM python

RUN mkdir app
RUN mkdir data

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 5000

WORKDIR /app

CMD ["gunicorn", "--worker-class", "gevent", "--workers", "5", "--reload", "--bind", "0.0.0.0:5000", "wsgi:app"]