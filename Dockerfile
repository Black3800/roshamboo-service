FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY app/ .
COPY roshamboo-final-model.pt /
CMD ["python", "./main.py"]