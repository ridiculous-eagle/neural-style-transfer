import os, cv2, imutils, urllib, numpy, time, flask, markdown

flask_app = flask.Flask(__name__)

@flask_app.route('/')
def root():
    markdown_content = """
# NeuralStyleTransfer
Image style transfer service using trained model from torch, powered by **RidiculousEagle** Studio.
## /style_transfer
```html
model: the path of trained torch model, available models are:
    + eccv16
        - composition_vii
        - la_muse
        - starry_night
        - the_wave
    + instance_norm
        - candy
        - feathers
        - la_muse
        - mosaic
        - starry_night
        - the_scream
        - udnie
image: encoded URL of the image path
type: response type (jpg as default, png), optional
```
    """
    markdown_content = flask.Markup(markdown.markdown(markdown_content, extensions=['fenced_code']))
    return markdown_content
    
# url parameters are as follow:
# - model: path of torch model to be applied
# - type: image type, jpg(default) or png
# - image: path of image, encoded
@flask_app.route('/style_transfer')
def style_transfer():
    try:
        image_url = urllib.parse.unquote(flask.request.args.get('image'))
        model_path = f'models/{urllib.parse.unquote(flask.request.args.get("model"))}.t7'
        image_type = flask.request.args.get('type')
        if image_type is None or image_type not in ['jpg', 'png']:
            image_type = 'jpg'
    except Exception as ex:
        return f'parameter exception raised: {ex}', 400
    if os.path.exists(model_path):
        try:
            net = cv2.dnn.readNetFromTorch(model_path)
            image_input = numpy.asarray(bytearray(urllib.request.urlopen(image_url).read()), dtype='uint8')
            image_input = cv2.imdecode(image_input, cv2.IMREAD_COLOR)
            image_input = imutils.resize(image_input, width=600)
            (height, width) = image_input.shape[:2]
            blob = cv2.dnn.blobFromImage(image_input, 1, (width, height), (103.939, 116.779, 123.680), swapRB = False, crop = False)
            net.setInput(blob)
            start = time.time()
            image_output = net.forward()
            end = time.time()
            image_output = image_output.reshape((3, image_output.shape[2], image_output.shape[3]))
            image_output[0] += 103.939
            image_output[1] += 116.779
            image_output[2] += 123.680
            image_output = image_output.transpose(1, 2, 0)
            retval, buffer = cv2.imencode(f'.{image_type}', image_output)
            response = flask.make_response(buffer.tobytes())
            response.headers['Content-Type'] = f'image/{image_type}'
            return response
        except Exception as ex:
            return f'exception raised: {ex}', 500
    else:
        return f'model not found: {model_path}', 404