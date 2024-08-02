FROM python:3.9

ADD requirements.txt /

RUN pip install -r /requirements.txt 

ADD service.py /
ADD send_requests.py /
ADD catalog_embeddings.npy /
ADD catalog.json /

ENV PYTHONUNBUFFERED=1

CMD ["python", "./service.py"]