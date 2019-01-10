FROM python:3

WORKDIR /app

COPY . /app

RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com -r requirements.txt

EXPOSE 21050

ENV NAME NeuralStyleTransfer
ENV PYTHONUNBUFFERED 1
ENV SERVE_PORT 21050
ENV SERVE_WORKERS 10
ENV SERVE_WORKER_THREADS 12

#CMD [ "python3", "-u", "server.py"]
CMD ["sh", "-c", "gunicorn -k gevent -w $SERVE_WORKERS --threads $SERVE_WORKER_THREADS -b 0.0.0.0:$SERVE_PORT wsgi"]