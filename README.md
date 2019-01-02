# NeuralStyleTransfer

Image style transfer service using trained model from torch, powered by **RidiculousEagle** Studio.

## Requirements

- Flask
- gevent
- imutils
- numpy
- opencv-python

## Build Docker Image

```bash
docker build -t neural-style-transfer
```

## Run From Docker Image

```bash
docker run -p [port]:5000 neural-style-transfer
```

```bash
docker run -d -p [port]:5000 neural-style-transfer
```

## Parameters

- model: relative path of torch trained model
- image: url of source image
- type: output format: jpg or png, optional parameter, using jpg as default

## Example

```http
GET http://[host]:[port]/style_transfer?model=eccv16/starry_night&image=https%3a%2f%2fupload.wikimedia.org%2fwikipedia%2fcommons%2fthumb%2fb%2fb9%2fSaffron_finch_%2528Sicalis_flaveola%2529_male.JPG%2f1200px-Saffron_finch_%2528Sicalis_flaveola%2529_male.JPG
```

