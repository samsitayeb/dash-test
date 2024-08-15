FROM python:3.8-slim-buster

RUN mkdir wd
WORKDIR wd

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . ./

CMD ["python", "./app.py"]