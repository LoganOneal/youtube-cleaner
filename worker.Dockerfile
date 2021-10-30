FROM python

RUN mkdir app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

CMD ["flask", "rq", "worker"]