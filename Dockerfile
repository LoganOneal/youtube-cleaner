FROM python

RUN mkdir app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 5000

WORKDIR /app

CMD ["flask", "run", "--host=0.0.0.0"]