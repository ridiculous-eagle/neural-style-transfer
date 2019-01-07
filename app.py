import os, cv2, imutils, urllib, numpy, time, flask, logging, ssl

logger = logging.getLogger(__name__)
flask_app = flask.Flask(__name__)
ssl._create_default_https_context = ssl._create_unverified_context


def get_image(uri):
    """
    get image by local uri or remote url
    Parameters
    ----------
    uri: str
        local uri or remote url
    Returns
    -------
    asarray
        image data
    """
    if os.path.exists(uri):
        return cv2.imread(uri, cv2.IMREAD_UNCHANGED)
    else:
        with urllib.request.urlopen(uri) as stream:
            image = numpy.asarray(bytearray(stream.read()), dtype=numpy.uint8)
        return cv2.imdecode(image, cv2.IMREAD_UNCHANGED)


def overlay_images(back, fore, x, y):
    """
    overlay a image on another
    Parameters
    ----------
    back: asarray
        background image
    fore: asarray
        foreground image
    x: int
        horizonal offset
    y: int
        vertical offset
    Returns
    ----------
    None
    """
    rows, cols, channels = fore.shape    
    trans_indices = fore[...,3] != 0 # Where not transparent
    overlay_copy = back[y:y+rows, x:x+cols] 
    overlay_copy[trans_indices] = fore[trans_indices]
    back[y:y+rows, x:x+cols] = overlay_copy


def style_transfer(input, net, subtraction):
    """
    style transfer based on dnn model
    Parameters
    ----------
    input: asarray
        source image
    net: net
        neural network model
    subtraction: turple
    Returns
    ----------
    asarray
        transfered image
    """
    (height, width) = input.shape[:2]
    blob = cv2.dnn.blobFromImage(input, 1, (width, height), subtraction, swapRB = False, crop = False)
    net.setInput(blob)
    start = time.time()
    transfer_ret = net.forward()
    end = time.time()
    logger.info(f"dnn.forward cost: {end - start}")
    transfer_ret = transfer_ret.reshape((3, transfer_ret.shape[2], transfer_ret.shape[3]))
    transfer_ret[0] += subtraction[0]
    transfer_ret[1] += subtraction[1]
    transfer_ret[2] += subtraction[2]
    transfer_ret = transfer_ret.transpose(1, 2, 0)
    return transfer_ret


@flask_app.route('/')
def do():
    try:
        image_url = urllib.parse.unquote(flask.request.args.get('image'))
        model_path = f'models/{urllib.parse.unquote(flask.request.args.get("model"))}.t7'
        canvas_url = flask.request.args.get('canvas')
        if canvas_url is None:
            canvas_url = 'backgrounds/white.jpg'
        else:
            canvas_url = urllib.parse.unquote(canvas_url)
        canvas_width = flask.request.args.get('width')
        try:
            canvas_width = int(canvas_width)
        except:
            canvas_width = 800
        overlay_offset = flask.request.args.get('offset')
        try:
            overlay_offset = int(overlay_offset)
        except:
            overlay_offset = 100
    except Exception as ex:
        logger.error(ex)
        return f'parameter exception raised: {ex}', 400
    if os.path.exists(model_path):
        try:
            net = cv2.dnn.readNetFromTorch(model_path)
            canvas = get_image(canvas_url)
            canvas = cv2.cvtColor(canvas, cv2.COLOR_RGB2RGBA)
            canvas = imutils.resize(canvas, width = canvas_width)
            (height, width) = canvas.shape[:2]
            logger.info(f"canvas uri: { canvas_url }, width: { width }, height: { height }")
            overlay = get_image(image_url)
            overlay = imutils.resize(overlay, width = canvas_width - overlay_offset * 2)
            (image_height, image_width) = overlay.shape[:2]
            logger.info(f"overlay uri: { image_url }, width: { image_width}, height: { image_height }")
            overlay_images(canvas, overlay, int((width - image_width) / 2), int((height - image_height) / 2))
            canvas = cv2.cvtColor(canvas, cv2.COLOR_RGBA2RGB)
            image_output = style_transfer(canvas, net, (103.939, 116.779, 123.680))
            retval, buffer = cv2.imencode('.jpg', image_output)
            response = flask.make_response(buffer.tobytes())
            response.headers['Content-Type'] = 'image/jpg'
            return response
        except Exception as ex:
            logger.error(ex)
            return f'exception raised: {ex}', 500
    else:
        logger.error(ex)
        return f'model not found: {model_path}', 404