FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN usr/local/bin/python -m pip install --upgrade pip

WORKDIR /nk_pr

COPY requirements.txt /nk_pr/
RUN pip install -r requirements.txt

COPY . /nk_pr/