# NeuralStyleTransfer

Image style transfer service using trained model from torch, powered by **RidiculousEagle** Studio.

## Requirements

- Flask
- gevent
- imutils
- numpy
- opencv-python

## Build Docker Image

`docker build -t neural-style-transfer`

## Run From Docker Image

`docker run -p [port]:5000 neural-style-transfer`

`docker run -d -p [port]:5000 neural-style-transfer`
