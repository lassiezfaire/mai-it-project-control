FROM python:3.10.13-bookworm
LABEL maintainer="Laissez Faire"

RUN pip install --upgrade pip
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install more-itertools
RUN pip install tqdm
RUN pip install gradio
RUN pip install numpy
RUN pip install -U scikit-image
RUN pip install -U albumentations

RUN pip install flask
RUN pip install waitress

EXPOSE 5000

WORKDIR /app

RUN mkdir -p /var/cartoonizer/uploads

COPY . .

CMD ["python", "cartoonizer-back.py"]