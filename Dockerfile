FROM python:3.8

RUN mkdir /build
WORKDIR /build
COPY requirements.txt /build/
RUN apt update && apt install -y ffmpeg && rm -rf /var/lib/apt/lists/*
RUN pip install numpy==1.23.3
RUN pip install -r requirements.txt
COPY . /build