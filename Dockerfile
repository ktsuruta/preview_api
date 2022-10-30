FROM python:3.7-alpine
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
WORKDIR /code
ADD . /code/preview_api
RUN apk add --no-cache gcc musl-dev linux-headers py3-pip
WORKDIR /code/preview_api
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]