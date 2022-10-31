FROM python:3.7-alpine
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
WORKDIR /code/preview_api
ADD ./requirements.txt /code/preview_api/requirements.txt
RUN apk add --no-cache gcc musl-dev linux-headers py3-pip
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]