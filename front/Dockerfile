FROM python:3-alpine
LABEL maintainer="Laissez Faire"

RUN pip install --upgrade pip
RUN pip install pytelegrambotapi

WORKDIR /app

COPY cartoonizer-front.py cartoonizer-front.py

CMD ["python", "cartoonizer-front.py"]