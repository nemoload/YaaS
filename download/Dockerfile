FROM python:3-alpine3.8

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENV FLASK_APP download

EXPOSE 80

ENTRYPOINT [ "flask", "run" , "--host", "0.0.0.0","-p", "80" ]
