FROM python

RUN mkdir app
RUN mkdir data

RUN apt-get -y update
RUN apt-get install -y software-properties-common
RUN apt-get install -y ffmpeg

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

CMD ["flask", "rq", "worker"]