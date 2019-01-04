FROM python:3

WORKDIR /app

COPY . /app

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

ENV NAME NeuralStyleTransfer
ENV PYTHONUNBUFFERED 1

CMD [ "python3", "-u", "server.py"]