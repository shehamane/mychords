FROM python:3.8

RUN mkdir /build
WORKDIR /build
COPY requirements.txt /build/
RUN pip install numpy==1.23.3
RUN pip install -r requirements.txt
COPY . /build