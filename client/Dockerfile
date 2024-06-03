# syntax=docker/dockerfile:1

FROM python:3.10.12-slim

WORKDIR /EdgeBookingApp

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["python", "-m" , "run.py"]